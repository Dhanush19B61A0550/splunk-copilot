import os
import requests

API_URL = "https://api.openai.com/v1/completions"
API_KEY = os.getenv("OPENAI_API_KEY")  # Securely access from environment

CONFIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'configs')
FILES = ['inputs.conf', 'outputs.conf']
CHANGES_LOG = os.path.join(os.path.dirname(__file__), '..', 'changes_detected.txt')
SUGGESTIONS_DIR = os.path.join(os.path.dirname(__file__), '..', 'suggestions')

# Create suggestions directory if not exists
os.makedirs(SUGGESTIONS_DIR, exist_ok=True)

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def ask_openai(file_name, content):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo-instruct",  # updated model
        "prompt": f"Suggest improvements for the following configuration file: {file_name}\n\n{content}",
        "max_tokens": 1000
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get('choices', [{}])[0].get('text', content)
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return content

def main():
    changes_made = False
    for file_name in FILES:
        file_path = os.path.join(CONFIG_DIR, file_name)
        content = read_file(file_path)
        improved_content = ask_openai(file_name, content)
        
        if improved_content.strip() != content.strip():
            # Save improved version separately
            suggestion_file = os.path.join(SUGGESTIONS_DIR, f"suggested_{file_name}")
            write_file(suggestion_file, improved_content)
            print(f"Suggestions for {file_name} written to {suggestion_file}")
            changes_made = True
        else:
            print(f"No suggestions for {file_name}")

    if changes_made:
        with open(CHANGES_LOG, 'w') as f:
            f.write("Suggestions generated for config files.\n")

if __name__ == "__main__":
    main()
