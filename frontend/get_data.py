import os
import gdown
import zipfile

# Define the Google Drive file IDs and corresponding file names
files = [
    {"id": "1RNeFdbDFKyGDk40AaGkuT11G7M_A9NSu", "name": "Keyframes_L01.zip"},
    {"id": "1tUEmgd7_53u7qvIZXwaVmuKr-Fk_6H29", "name": "Keyframes_L02.zip"},
    {"id": "1SH_6A652mwvoM74FeB1f61kf9JY6c9mF", "name": "Keyframes_L03.zip"},
    {"id": "1oPOG-KgRdzquDwzKtn6yyFGXX8tj599x", "name": "Keyframes_L04.zip"},
    {"id": "1cYCVp_MJ_VlT8BpBXP7DDWvuxhNO4OPl", "name": "Keyframes_L05.zip"},
    {"id": "1LV5zUqON1_7w2f0xyIIiccf54Vtu1eji", "name": "Keyframes_L06.zip"},
    {"id": "1Coey6rqh6Ktvn5_rRqc1pHyWfiS1R-bF", "name": "Keyframes_L07.zip"},
    {"id": "11fIsRUta8kWzyDeGxjaRLD3MIR4kott-", "name": "Keyframes_L08.zip"},
    {"id": "15nnPlpfHLwcqYWF80nRpuh2q4MfGa1dZ", "name": "Keyframes_L09.zip"},
    {"id": "1aSbYBHXoQtiGrubWqzNHnMYmYqZUDZ7P", "name": "Keyframes_L10.zip"},
    {"id": "1szB2rJHWAFx2QpgPwEbMpNTuu25GjnZW", "name": "Keyframes_L11.zip"},
    {"id": "1LvbRl0wbjnitZKBzdu_I7diKuDtSFXCp", "name": "Keyframes_L12.zip"},
    {"id": "1s2ZYyeewrE4H7Z1RvEwMaPJ-8OpT5hQe", "name": "Keyframes_L13.zip"},
    {"id": "1L6bgjbkRbBoehj3MzN9TGUg9tU1Azhvw", "name": "Keyframes_L14.zip"},
    {"id": "15VhZYT904eSimRjzEFbTTy_m6Hpa5ajl", "name": "Keyframes_L15.zip"},
    {"id": "1SPVDHbEKBY9DmyZYTAyVRqiKciJLbdWe", "name": "Keyframes_L16.zip"},
    {"id": "1I4hwVBgoaLm1FRA5rv0QG6nGoXl2xVvy", "name": "Keyframes_L17.zip"},
    {"id": "1Uwp-uhTE3jHXeEawXjqqkCLl9uVYlKOF", "name": "Keyframes_L18.zip"},
    {"id": "1F_x5ezQAgX7Ljny7DKZL4Xy5rmrGXf9e", "name": "Keyframes_L19.zip"},
    {"id": "1MjznJF-O3WTu9WDEZGJWwXulvXiwwKzv", "name": "Keyframes_L20.zip"},
    {"id": "1Vwwv2QcBbOEHlQPaX8kDVl5cHr6gJMTu", "name": "Keyframes_L21.zip"},
    {"id": "1F1XyBgsOLLPGwplR9TtVk_XOH2ltdFBl", "name": "Keyframes_L22.zip"},
    {"id": "1lr8ErPalHsGQn1O_2Rp7jwOt4AIV5ZDr", "name": "Keyframes_L23.zip"},
    {"id": "1dWfd3wT7uCoBrQzsTL5P9T5mxFa_e4xN", "name": "Keyframes_L24.zip"},
    {"id": "1AuF9TmcDqqQtttLd2EnKU59KKzHdm3Zq", "name": "Keyframes_L25.zip"},
    {"id": "1QlahIF5PHdpwFWbl1xiD8cR4AImp32nb", "name": "Keyframes_L26.zip"},
    {"id": "1HsLKLYujoxFiF3o35npk-0tiP37ULbKF", "name": "Keyframes_L27.zip"},
    {"id": "1K4UbFdX5yuP-A38j2eogCUiID-CbmvKX", "name": "Keyframes_L28.zip"},
    {"id": "1E_TniwPx4pG9btZiWAOUhtGtQ4eu0XT8", "name": "Keyframes_L29.zip"},
    {"id": "1gdISAOANZeX2DE7lkitrpL9KE-WbQpZG", "name": "Keyframes_L30.zip"},
    {"id": "1dzu_fAdqAykAZxtw355VbEj1iDUOXyWv", "name": "Keyframes_L31.zip"},
    {"id": "1gk18qAY-T3LCiSe9vLksTLlFHRzaOnQ3", "name": "Keyframes_L32.zip"},
    {"id": "1O4PRwUFsjXpiU49_X0RYivaFaj986gZL", "name": "Keyframes_L33.zip"},
    {"id": "1eRXHcaiUxkw4wTIMoXJRa1bvJfY2kQ_N", "name": "Keyframes_L34.zip"},
    {"id": "12XZwjyac9DNjd59KGNwSAW2NPGR7DTdb", "name": "Keyframes_L35.zip"},
    {"id": "16f9UPAvMAT4TXACxNyDPjwrVAb5ijdAG", "name": "Keyframes_L36.zip"},
    
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
