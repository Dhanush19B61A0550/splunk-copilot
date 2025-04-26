import os
import requests

# Replace with your Terrace Copilot API URL if it's different
# OpenAI API URL
API_URL = "https://api.openai.com/v1/completions"

# Insert your OpenAI API key here (BE CAREFUL with hardcoding keys in production)
API_KEY = "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"

def read_file(file_path):
    """Reads content from a file."""
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    """Writes content to a file."""
    with open(file_path, 'w') as file:
        file.write(content)

def ask_openai(file_name, content):
    """Sends the file content to OpenAI for suggestions."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "text-davinci-003",  # You can change the model if needed
        "prompt": f"Suggest improvements for the following configuration file: {file_name}\n\n{content}",
        "max_tokens": 1000  # Adjust token count as needed
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json().get('choices', [{}])[0].get('text', content)
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return content

# List of configuration files you want to improve
files = ['inputs.conf', 'outputs.conf']
changes_made = False

for file in files:
    content = read_file(file)
    improved_content = ask_openai(file, content)
    
    # Check if changes are suggested and update the file
    if improved_content.strip() != content.strip():
        write_file(file, improved_content)
        changes_made = True

# Log changes if any were made
if changes_made:
    with open('changes_detected.txt', 'w') as f:
        f.write("Changes made to config files.\n")