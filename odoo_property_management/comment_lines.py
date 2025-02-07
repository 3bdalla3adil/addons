import os
import re

def comment_lines_in_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if '#should not be in production' in line:
                line = '# ' + line
            file.write(line)

def walk_directory_and_comment(directory='.'):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                comment_lines_in_file(os.path.join(root, file))

def increment_version(version):
    major, minor = map(int, version.split('.'))
    minor += 1
    return f"{major}.{minor}"

def update_version_in_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    version_pattern = re.compile(r"'version': '(\d+\.\d+)'")
    match = version_pattern.search(content)
    if match:
        current_version = match.group(1)
        new_version = increment_version(current_version)
        updated_content = version_pattern.sub(f"'version': '{new_version}'", content)

        with open(file_path, 'w') as file:
            file.write(updated_content)
        print(f"Updated version from {current_version} to {new_version}")
    else:
        print("Version pattern not found in the file")

if __name__ == "__main__":
    walk_directory_and_comment()
    update_version_in_file('__manifest__.py')