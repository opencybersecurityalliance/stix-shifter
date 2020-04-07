import os

src_folders = ["stix_shifter_utils", "stix_shifter", "stix_shifter_modules"]
install_requires = set()
requirements_files = []
for src_folder in src_folders:
    for r, d, f in os.walk(src_folder):
        for file in f:
            if 'requirements.txt'==file and not os.path.isfile(os.path.join(r, 'SKIP.ME')):
                requirements_files.append(os.path.join(r, file))
print('requirements_files: %s' % requirements_files)
for requirements_file in requirements_files:
    with open(requirements_file) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    lines = list(filter(lambda s: len(s)>0, lines))
    install_requires.update(lines)
install_requires = list(install_requires)
install_requires.sort()
print('install_requires: %s' % install_requires)

with open('requirements.txt', 'w') as out_file:
    for item in install_requires:
        out_file.write(item)
        out_file.write('\n')
