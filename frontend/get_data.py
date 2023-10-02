import os
import gdown
import zipfile

# Define the Google Drive file IDs and corresponding file names
files = [
    {"id": "1RNeFdbDFKyGDk40AaGkuT11G7M_A9NSu", "name": "Keyframes_L01.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L03.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L04.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L05.zip"},
    {"id": "1LV5zUqON1_7w2f0xyIIiccf54Vtu1eji", "name": "Keyframes_L06.zip"},
    {"id": "1Coey6rqh6Ktvn5_rRqc1pHyWfiS1R-bF", "name": "Keyframes_L07.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L08.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L09.zip"},
    {"id": "1aSbYBHXoQtiGrubWqzNHnMYmYqZUDZ7P", "name": "Keyframes_L10.zip"},
    
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
        new_folder_name = file_name[:-4]
        zip_ref.extractall(destination_folder)
        extracted_folder_name = zip_ref.namelist()[0].split('/')[0]
        os.rename(os.path.join(destination_folder, extracted_folder_name), os.path.join(destination_folder, new_folder_name) )

    print(f"Removing downloaded file: {file_name}")
    os.remove(file_name)

print("Files downloaded and extracted to", destination_folder)
