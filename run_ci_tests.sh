#!/bin/bash
# Replicate GitHub Actions CI workflow locally
# Usage:
#   ./run_ci_tests.sh              # Test with current Python version (fast)
#   ./run_ci_tests.sh --all-versions  # Test with Python 3.10, 3.11, 3.12 (comprehensive)

set -e  # Exit on error

# Parse arguments
ALL_VERSIONS=false
if [[ "$1" == "--all-versions" ]]; then
    ALL_VERSIONS=true
fi

# Python versions to test (matches GitHub Actions matrix)
PYTHON_VERSIONS=("3.10" "3.11" "3.12")

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to run CI tests for a specific Python version
run_tests_for_version() {
    local python_cmd=$1
    local version_label=$2
    local venv_path=$3

    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}Testing with Python ${version_label}${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""

    # Create and activate virtual environment if specified
    if [[ -n "$venv_path" ]]; then
        echo "🔧 Creating virtual environment: ${venv_path}"
        $python_cmd -m venv "$venv_path"
        source "${venv_path}/bin/activate"
        echo "✓ Activated ${venv_path}"
        echo ""
    fi

    echo "🔧 Generating requirements..."
    $python_cmd generate_requirements.py

    echo ""
    echo "📦 Installing dependencies..."
    pip install --upgrade pip setuptools wheel
    pip install -r requirements-dev.txt

    echo ""
    echo "🔍 Linting: Checking for syntax errors (critical)..."
    pip install --upgrade flake8
    flake8 . --count --select=E901,E999,F821,F822,F823 --show-source --statistics \
        --exclude='virtualenv,venv,.venv,build,dist,.git,.pytest_cache,__pycache__,virtualenv_ci_*'

    echo ""
    echo "⚠️  Linting: Checking for style warnings..."
    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics \
        --exclude='virtualenv,venv,.venv,build,dist,.git,.pytest_cache,__pycache__,virtualenv_ci_*'

    echo ""
    echo "🧪 Running all tests with pytest..."
    pip install pytest
    pytest -vv

    # Deactivate virtual environment if we created one
    if [[ -n "$venv_path" ]]; then
        deactivate
        echo ""
        echo -e "${GREEN}✓ Python ${version_label} tests completed successfully${NC}"
    fi

    echo ""
}

# Function to check if a Python version is available
check_python_version() {
    local version=$1
    if command -v python${version} &> /dev/null; then
        return 0
    elif pyenv versions --bare | grep -q "^${version}"; then
        return 0
    else
        return 1
    fi
}

# Function to get Python command for a version
get_python_command() {
    local version=$1
    if command -v python${version} &> /dev/null; then
        echo "python${version}"
    elif pyenv versions --bare | grep -q "^${version}"; then
        # Use pyenv to get the full version (e.g., 3.10.14)
        local full_version=$(pyenv versions --bare | grep "^${version}" | head -1)
        echo "$(pyenv root)/versions/${full_version}/bin/python"
    else
        echo ""
    fi
}

# Main execution
if [[ "$ALL_VERSIONS" == true ]]; then
    echo -e "${YELLOW}Running CI tests for all Python versions (3.10, 3.11, 3.12)${NC}"
    echo -e "${YELLOW}This will take several minutes...${NC}"
    echo ""

    # Check which versions are available
    AVAILABLE_VERSIONS=()
    MISSING_VERSIONS=()

    for version in "${PYTHON_VERSIONS[@]}"; do
        if check_python_version "$version"; then
            AVAILABLE_VERSIONS+=("$version")
        else
            MISSING_VERSIONS+=("$version")
        fi
    done

    # Warn about missing versions
    if [[ ${#MISSING_VERSIONS[@]} -gt 0 ]]; then
        echo -e "${YELLOW}⚠️  Warning: The following Python versions are not installed:${NC}"
        for version in "${MISSING_VERSIONS[@]}"; do
            echo -e "${YELLOW}   - Python ${version}${NC}"
        done
        echo -e "${YELLOW}   Install with: pyenv install ${MISSING_VERSIONS[0]}${NC}"
        echo ""
    fi

    # Exit if no versions available
    if [[ ${#AVAILABLE_VERSIONS[@]} -eq 0 ]]; then
        echo -e "${RED}Error: No Python versions available for testing${NC}"
        exit 1
    fi

    # Run tests for each available version
    FAILED_VERSIONS=()
    for version in "${AVAILABLE_VERSIONS[@]}"; do
        python_cmd=$(get_python_command "$version")
        venv_path="virtualenv_ci_${version}"

        if run_tests_for_version "$python_cmd" "$version" "$venv_path"; then
            echo -e "${GREEN}✓ Python ${version} passed${NC}"
        else
            echo -e "${RED}✗ Python ${version} failed${NC}"
            FAILED_VERSIONS+=("$version")
        fi

        # Clean up virtual environment
        rm -rf "$venv_path"
        echo ""
    done

    # Final summary
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}Test Summary${NC}"
    echo -e "${BLUE}================================${NC}"
    echo "Tested versions: ${#AVAILABLE_VERSIONS[@]}"
    echo "Passed: $((${#AVAILABLE_VERSIONS[@]} - ${#FAILED_VERSIONS[@]}))"
    echo "Failed: ${#FAILED_VERSIONS[@]}"

    if [[ ${#FAILED_VERSIONS[@]} -gt 0 ]]; then
        echo -e "${RED}Failed versions: ${FAILED_VERSIONS[*]}${NC}"
        exit 1
    else
        echo -e "${GREEN}✅ All Python versions passed!${NC}"
    fi

else
    # Single version mode - use current Python
    echo -e "${YELLOW}Running CI tests with current Python version${NC}"
    echo -e "${YELLOW}Use --all-versions flag to test against Python 3.10, 3.11, 3.12${NC}"
    echo ""

    current_version=$(python --version | cut -d' ' -f2)
    run_tests_for_version "python" "$current_version" ""

    echo -e "${GREEN}✅ All CI checks passed!${NC}"
fi
