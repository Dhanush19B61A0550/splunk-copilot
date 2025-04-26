def validate_config(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if "=" not in line and line.strip() and not line.startswith("["):
            raise Exception(f"Syntax error in {file_path}: {line}")

    print(f"{file_path} is valid!")

for file in ['inputs.conf', 'outputs.conf']:
    validate_config(file)
