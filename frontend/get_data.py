import gdown 
import zipfile
import os
url = "https://drive.google.com/drive/folders/1koM9SmKtDS85hozN4h_-cs_JYyCYAzcQ"

gdown.download_folder(url,  quiet=False,   remaining_ok= True )


