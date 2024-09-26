import re
import csv
import json
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Define patterns for IP addresses, file paths, URLs, emails, telephone numbers, and sensitive information
ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'
windows_file_path_pattern = r'([a-zA-Z]:\\(?:[^\\\/:*?"<>|\r\n]+\\)*[^\\\/:*?"<>|\r\n]+\.[a-zA-Z]+)'
unix_file_path_pattern = r'(/(?:[^/ ]+/)*[^/ ]+\.[a-zA-Z]+)'
url_pattern = r'(https?|ftp):\/\/[^\s\/$.?#].[^\s]*'
email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
phone_pattern = r'(\+?\d{1,2}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'

# Sensitive information patterns (capture the actual value)
password_pattern = r'(?i)(password|pwd|pass)[\s:=]+([^\s,]+)'
username_pattern = r'(?i)(user|username|uname)[\s:=]+([^\s,]+)'
ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b|\b\d{9}\b'
credit_card_pattern = r'\b(?:\d[ -]*?){13,16}\b'

# Define replacement strings
ip_replacement = 'x.x.x.x'
windows_file_path_replacement = r'drive:\\path\\to\\file.extension'
unix_file_path_replacement = r'/path/to/file.extension'
url_replacement = 'protocol://subdomain.domain.tld:port/directory'
email_replacement = '[REDACTED-EMAIL]'
phone_replacement = '[REDACTED-PHONE]'

# Sensitive data replacement strings
password_replacement = r'\1: [REDACTED-PASSWORD]'
username_replacement = r'\1: [REDACTED-USERNAME]'
ssn_replacement = '[REDACTED-SSN]'
credit_card_replacement = '[REDACTED-CREDIT-CARD]'

# Function to apply regex replacements to a given string
def replace_patterns(text):
    # Replace Windows file paths first
    text = re.sub(windows_file_path_pattern, windows_file_path_replacement, text)
    # Replace Unix file paths
    text = re.sub(unix_file_path_pattern, unix_file_path_replacement, text)
    # Replace IP addresses
    text = re.sub(ip_pattern, ip_replacement, text)
    # Replace URLs
    text = re.sub(url_pattern, url_replacement, text)
    # Replace emails
    text = re.sub(email_pattern, email_replacement, text)
    # Replace telephone numbers
    text = re.sub(phone_pattern, phone_replacement, text)
    # Replace sensitive information
    text = re.sub(password_pattern, password_replacement, text)
    text = re.sub(username_pattern, username_replacement, text)
    text = re.sub(ssn_pattern, ssn_replacement, text)
    text = re.sub(credit_card_pattern, credit_card_replacement, text)
    return text

# Function to handle CSV files
def process_csv(file_path):
    result = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            processed_row = [replace_patterns(cell) for cell in row]
            result.append(processed_row)
    # Save the result back to the file
    output = "\n".join([",".join(row) for row in result])
    return output

# Function to handle JSON files
def process_json(file_path):
    def traverse_and_replace(data):
        if isinstance(data, dict):
            return {key: traverse_and_replace(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [traverse_and_replace(item) for item in data]
        elif isinstance(data, str):
            return replace_patterns(data)
        else:
            return data
    
    with open(file_path, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        processed_data = traverse_and_replace(data)

    return json.dumps(processed_data, indent=4)

# Function to handle XML files
def process_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    def traverse_xml(element):
        if element.text:
            element.text = replace_patterns(element.text)
        for child in element:
            traverse_xml(child)

    traverse_xml(root)
    return ET.tostring(root, encoding='unicode')

# Function to handle different file types (txt, csv, json, xml)
def process_file_content(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        return process_csv(file_path)
    elif ext == ".json":
        return process_json(file_path)
    elif ext == ".xml":
        return process_xml(file_path)
    else:
        with open(file_path, 'r', encoding='utf-8') as infile:
            content = infile.read()
            return replace_patterns(content)

# Function to browse and select a file
def browse_file():
    file_path = filedialog.askopenfilename(
        title="Select a File", 
        filetypes=[("All files", "*.*"), ("Text files", "*.txt"), ("CSV files", "*.csv"), 
                   ("JSON files", "*.json"), ("XML files", "*.xml")]
    )
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

# Function to process the selected file
def process_file():
    input_file = entry_file_path.get()
    if not input_file:
        messagebox.showerror("Error", "Please select a file.")
        return
    
    # Choose a save location for the output file
    output_file = filedialog.asksaveasfilename(defaultextension=".txt", 
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                               title="Save the modified file as")
    if not output_file:
        return

    try:
        # Process the input file and save output
        processed_content = process_file_content(input_file)
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(processed_content)

        messagebox.showinfo("Success", f"Replacements completed. The modified file is saved as {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("MaskIt")

# Create and place GUI components
label_file_path = tk.Label(root, text="Select a File:")
label_file_path.grid(row=0, column=0, padx=10, pady=10)

entry_file_path = tk.Entry(root, width=50)
entry_file_path.grid(row=0, column=1, padx=10, pady=10)

button_browse = tk.Button(root, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2, padx=10, pady=10)

button_process = tk.Button(root, text="Process", command=process_file)
button_process.grid(row=1, column=1, padx=10, pady=10)

# Run the main loop
root.mainloop()
