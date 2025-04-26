import os

CONFIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'configs')
FILES = ['inputs.conf', 'outputs.conf']

def validate_config(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if "=" not in line and line.strip() and not line.startswith("["):
            raise Exception(f"Syntax error in {file_path}: {line}")

    print(f"{file_path} is valid!")

def main():
    for file_name in FILES:
        file_path = os.path.join(CONFIG_DIR, file_name)
        validate_config(file_path)

if __name__ == "__main__":
    main()
