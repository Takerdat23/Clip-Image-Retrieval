import os
import gdown
import zipfile

# Define the Google Drive file IDs and corresponding file names
files = [
    {"id": "1RNeFdbDFKyGDk40AaGkuT11G7M_A9NSu", "name": "Keyframes_L01.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
]

# Define the destination folder for unzipping
destination_folder = "./KeyFrames"

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Loop through the files and download and unzip them
for file_info in files:
    file_id = file_info["id"]
    file_name = file_info["name"]

    print(f"Downloading file: {file_name}")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output=file_name, quiet=False)

    print(f"Unzipping file: {file_name}")
    with zipfile.ZipFile(file_name, "r") as zip_ref:
        zip_ref.extractall(destination_folder)

    print(f"Removing downloaded file: {file_name}")
    os.remove(file_name)

print("Files downloaded and extracted to", destination_folder)
