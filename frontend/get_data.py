import os
import gdown
import zipfile

# Define the Google Drive file IDs and corresponding file names
files = [
    {"id": "12hctgrrQYMlyvSNns5bnVrPWZMEb4R3-", "name": "Keyframes_L01.zip"},
    {"id": "1508hX9NVeYWNZK2RrmxY3qP3IUoLO9GT", "name": "Keyframes_L02.zip"},
    {"id": "1Gmp6cnLZ6VDUW8pl0mVDYP358S6Gpi3j", "name": "Keyframes_L03.zip"},
    {"id": "1OUEQpTK9CmcYYJPoqgv_tZm4Rx3uf9X1", "name": "Keyframes_L04.zip"},
    {"id": "1zSis2xLjHc8joo1adQxK53Fo5hNc-X_u", "name": "Keyframes_L05.zip"},
    {"id": "1fpx2YlMPcUGXqRhi7ZRBrFVmyclzUM71", "name": "Keyframes_L06.zip"},
    {"id": "18WHGzQnzpyabXvaalgkihnfthTN8mAUx", "name": "Keyframes_L07.zip"},
    {"id": "1bXj8c5yKyEWr0JHggdYkr7XoZ4wxmjzP", "name": "Keyframes_L08.zip"},
    {"id": "1WAwxA9iwam8DSzPJVI9t1Iv8-Hvf0n-t", "name": "Keyframes_L09.zip"},
    {"id": "1Yl8obDEPfLK6KWoczWIRSGW_rJr4648U", "name": "Keyframes_L10.zip"},
    {"id": "1E4S1dK6BX14A2sBWaLxluW5jLznX6sQ6", "name": "Keyframes_L11.zip"},
    {"id": "1q3KiEMv77Q7WZE3ITkLdHi3-26lRuXvg", "name": "Keyframes_L12.zip"},
    {"id": "19zhceuE-O0jlnTSU59drjyuAuHRN4lvl", "name": "Keyframes_L13.zip"},
    {"id": "1iU2do3z7cn2wxKdwypOXvgJSECARBHT_", "name": "Keyframes_L14.zip"},
    {"id": "1Xp2Ak1ahkrb_k8pyAUZeCwCCKSGeo9z0", "name": "Keyframes_L15.zip"},
    {"id": "1mLwz-ywLH5I3suKC9NhZNxzPJT1rksfU", "name": "Keyframes_L16.zip"},
    {"id": "17RePFZmYZl5flWAlbUe6cbi_tWXNEl0h", "name": "Keyframes_L17.zip"},
    {"id": "1vv3uhN0cYnf-F3aQ4XyqFC0NCniijEyr", "name": "Keyframes_L18.zip"},
    {"id": "1tTR1rruBzaI8A_olqvShSVaMlHlo3rVa", "name": "Keyframes_L19.zip"},
    {"id": "1ZNLxS51YyQMn-V_XCy8E9y64wsStDOii", "name": "Keyframes_L20.zip"},
    {"id": "17LVwJ3csXK16kBuut8N1tAe7zBICi9NN", "name": "Keyframes_L21.zip"},
    {"id": "15pkhUXishmbNTXE_4N_Tj5K_4eSvkRwB", "name": "Keyframes_L22.zip"},
    {"id": "17vuwggwJxHD_hu42GwnzLEU6Itpqk9OO", "name": "Keyframes_L23.zip"},
    {"id": "16_VwqaPQyqYhzrc2R8kqUkZ-9LvIKW9S", "name": "Keyframes_L24.zip"},
    {"id": "15wtlxmau6d4-nuV6AaBo_ie1MU3u5xnL", "name": "Keyframes_L25.zip"},
    {"id": "13o5CwOf1BtpSYqtlqDl4-4gaksuvocDt", "name": "Keyframes_L26.zip"},
    {"id": "1obKQjnSz6YETOCisok321QfKz3Lbbjma", "name": "Keyframes_L27.zip"},
    {"id": "1ziS5a5urWtytQKN4xwXwikGXePHEDv1b", "name": "Keyframes_L28.zip"},
    {"id": "1W_TiZMfXT5lr7Lv9rIKgInWvyiQF1sT7", "name": "Keyframes_L29.zip"},
    {"id": "1M-xCBhS9-cack-4KJbGoRWNOTiqbVqNU", "name": "Keyframes_L30.zip"},
    {"id": "1FMKu3lZk2YOvYzmQul6w38LIeVUoDZhs", "name": "Keyframes_L31.zip"},
    {"id": "1q86QWViZKMh6QtHsEir0-9Cbyz1gmylU", "name": "Keyframes_L32.zip"},
    {"id": "133i2TMBRgqFPMjspq7556EB7ZB4lWe2D", "name": "Keyframes_L33.zip"},
    {"id": "1jtItpehDWg-jaI2DY4kODdpLkEvfl3DZ", "name": "Keyframes_L34.zip"},
    {"id": "1QXfF7-J0lw0BWus83Ys2uyL9p3wSer1P", "name": "Keyframes_L35.zip"},
    {"id": "1O7NiXLnbvavt15WDFz31YFbwpdaYQ-ch", "name": "Keyframes_L36.zip"},
    
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
    gdown.download(f"https://drive.google.com/uc?id={file_id}&export=download&confirm=t", output=file_name, quiet=False)

    print(f"Unzipping file: {file_name}")
    with zipfile.ZipFile(file_name, "r") as zip_ref:
        new_folder_name = file_name[:-4]
        zip_ref.extractall(destination_folder)
        extracted_folder_name = zip_ref.namelist()[0].split('/')[0]
        os.rename(os.path.join(destination_folder, extracted_folder_name), os.path.join(destination_folder, new_folder_name) )

    print(f"Removing downloaded file: {file_name}")
    os.remove(file_name)

print("Files downloaded and extracted to", destination_folder)
