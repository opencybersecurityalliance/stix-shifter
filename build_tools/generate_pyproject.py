"""
generate_pyproject.py

Small utility to generate a pyproject.toml from a template and a set of explicit values.

Usage:
    from build_tools.generate_pyproject import generate_pyproject_from_values

    generate_pyproject_from_values(
        template_path="build_templates/pyproject.template.toml",
        target_dir="/_temp/stix_shifter_modules_33sckmld39",
        package_name="stix_shifter_modules",
        version="8.0.2",
        description="My package description",
        authors="IBM",
        license_text="Apache-2.0",
        dependencies_block=["requests>=2.28", "pyyaml"],
        packages_include=["stix_shifter_utils", "stix_shifter_utils.submodule"],
        entry_points={
            "console_scripts": ["stix-shifter-utils=stix_shifter_utils.scripts:main"],
            "myplugin.hooks": ["hook1=some.module:func"]
        },
    )
"""

import shutil
from string import Template
from pathlib import Path
from typing import Optional, Iterable

from .logging_setup import get_logger


DEFAULT_README_PATH = "docs/README.md"
PACKAGE_ROOT = Path(__file__).resolve().parent  # build_tools/
PROJECT_ROOT = PACKAGE_ROOT.parent              # project/
TEMPLATES_DIR = PROJECT_ROOT / "build_templates"


logger = get_logger("generate_pyproject")


# ------------------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------------------


def _toml_escape(s: str) -> str:
    """
    Minimal escaping for TOML double-quoted string values.
    For complex cases you may want a real TOML writer, but this suffices for
    the simple metadata fields we fill.
    """
    if s is None:
        return ""
    return s.replace('\\', '\\\\').replace('"', '\\"')


def _build_dependencies_block(deps: Iterable[str]) -> str:
    """
    Create the lines inside the dependencies array, each line quoted and trailing comma.
    Returns empty string if deps is empty.
    """
    if not deps:
        return ""
    lines = []
    for d in sorted({d.strip() for d in deps if d and d.strip()}):
        lines.append(f'    "{_toml_escape(d)}",')
    return "\n".join(lines)


def _build_authors_block(author: Optional[str], author_email: Optional[str]) -> str:
    """
    Build the inline table for one author: { name = "IBM", email = "placeholder@ibm.com" }
    Returns empty string if neither are provided.
    """
    if not author and not author_email:
        return ""
    parts = []
    if author:
        parts.append(f'name = "{_toml_escape(author)}"')
    if author_email:
        parts.append(f'email = "{_toml_escape(author_email)}"')
    return "{ " + ", ".join(parts) + " }"


def _build_packages_include(packages_list: Iterable[str]) -> str:
    """
    Convert a list of package dotted names into TOML include list entries.
    Each package in the input list becomes a separate entry.
    Example:
        Input: ["stix_shifter_utils", "stix_shifter_utils.async_template"]
        Output: '"stix_shifter_utils", "stix_shifter_utils.async_template"'
    """
    if not packages_list:
        return '""'

    # remove empty strings and strip whitespace
    cleaned = sorted({p.strip() for p in packages_list if p and p.strip()})

    # Escape for TOML and wrap in quotes
    items = [f'"{_toml_escape(p)}"' for p in cleaned]

    return ", ".join(items)


def _build_scripts_block(entry_points: Optional[dict]) -> str:
    """
    Convert console_scripts into a [project.scripts] TOML block.
    Returns empty string when no console_scripts are present.
    """
    if not entry_points:
        return ""
    cs = entry_points.get("console_scripts", []) or []
    if not cs:
        return ""
    lines = ["", "[project.scripts]"]
    for item in cs:
        if "=" in item:
            name, target = item.split("=", 1)
            lines.append(f'{name.strip()} = "{_toml_escape(target.strip())}"')
    return "\n".join(lines)


def _build_other_entry_point_groups(entry_points: Optional[dict[str, list[str]]]) -> str:
    """
    Convert non-console_scripts entry_points into PEP 621 entry-points sections:
    e.g.
    [project.entry-points."stix_shifter.hooks"]
    hook1 = "module:callable"
    """
    if not entry_points:
        return ""
    blocks = []
    for group, items in (entry_points.items() if isinstance(entry_points, dict) else []):
        if group == "console_scripts":
            continue
        if not items:
            continue
        blocks.append(f'\n[project.entry-points."{_toml_escape(group)}"]')
        for item in items:
            if "=" in item:
                key, target = item.split("=", 1)
                blocks.append(f'{key.strip()} = "{_toml_escape(target.strip())}"')
    return "\n".join(blocks)


def _build_readme_block(target_dir: str) -> str:
    """
    Ensure README.md exists in the target directory, else copy default README. 
    Return a string suitable for pyproject.toml `[project].readme` field:
        { file = "README.md", content-type = "text/markdown" }
    """

    target_readme_path = Path(target_dir) / "README.md"

    # Copy default README if README.md doesn't already exist
    if not target_readme_path.exists():
        shutil.copy(DEFAULT_README_PATH, target_readme_path)

    # NOTE: setup tools may want us to implement content-type context at some point in the future
    # return {"file": "README.md", "content-type": "text/markdown"}
    return "README.md"


# ------------------------------------------------------------------------------
# Driver function for pyproject generator
# ------------------------------------------------------------------------------


def generate_pyproject_from_values(
    *,
    template_path: str,
    target_dir: str,
    package_name: str,
    version: str,
    description: str = "",
    author: Optional[str] = None,
    author_email: Optional[str] = None,
    license_text: str = "Apache-2.0",
    dependencies: Optional[list[str]] = None,
    packages_list: Optional[list[str]] = None,
    entry_points: Optional[dict[str, list[str]]] = None,
) -> str:
    """
    Render the pyproject.toml from a template file.

    Parameters
    - template_path: path to the template file (string.Template style placeholders).
    - target_dir: directory where pyproject.toml will be written.
    - package_name, version, description: core fields.
    - author, author_email, license_text: metadata
    - dependencies: iterable of dependency strings (e.g. ["requests>=2.28"])
    - packages_list: a list of package dotted names that helps build [tool.setuptools.packages.find] include.
    - entry_points: A mapping of entry-point groups

    Returns: str path to the written pyproject.toml
    """
    tpl_text = Path(template_path).read_text(encoding="utf-8")
    tpl = Template(tpl_text)

    deps_block = _build_dependencies_block(dependencies or [])
    authors_block = _build_authors_block(author, author_email)
    packages_include = _build_packages_include(packages_list or [])
    scripts_block = _build_scripts_block(entry_points or {})
    other_entry_points = _build_other_entry_point_groups(entry_points or {})

    readme_metadata = _build_readme_block(target_dir)

    subs = {
        "package_name": _toml_escape(package_name),
        "version": _toml_escape(version),
        "description": _toml_escape(description or ""),
        "readme_file": readme_metadata,
        "authors_block": authors_block,
        "license_text": _toml_escape(license_text),
        "dependencies_block": deps_block,
        "packages_include": packages_include,
        "project_scripts_block": scripts_block,
        "other_entry_points": other_entry_points,
    }

    out = tpl.safe_substitute(subs)

    pyproject_path = Path(target_dir) / "pyproject.toml"
    pyproject_path.write_text(out, encoding="utf-8")
    return str(pyproject_path)


# --- Convenience small CLI for quick local testing ---------------------------


if __name__ == "__main__":
    # minimal smoke test to write into ./tmp-pyproject-test
    example_dir = "tmp-pyproject-test"
    Path(example_dir).mkdir(parents=True, exist_ok=True)

    # Use the template next to this file (adjust path when running)
    default_tpl = TEMPLATES_DIR / "pyproject.template.toml"
    if not default_tpl.exists():
        logger.critical("Template not found at %s", default_tpl)
    else:
        p = generate_pyproject_from_values(
            template_path=str(default_tpl),
            target_dir=example_dir,
            package_name="stix_shifter_modules_foobar",
            version="0.0.1",
            description="Test package generated pyproject",
            author="IBM",
            author_email="",
            license_text="Apache-2.0",
            dependencies=["requests>=2.28", "pyyaml"],
            packages_list=["stix_shifter_utils", "stix_shifter_utils.sub"],
            entry_points={"console_scripts": ["stix-shifter-utils=stix_shifter_utils.scripts:main"]},
        )
        logger.info("Wrote", p)
