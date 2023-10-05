from __future__ import annotations

import base64
import requests

import streamlit as st
import pandas as pd 
import os
from PIL import Image
import app

def fetch_image_bytes(url: str) -> bytes:
    """This function fetches image bytes from url.

    Parameters
    ----------
    url : str
        URL of the image

    Returns
    -------
    bytes
        Fetched image bytes
    """
    return requests.get(url).content

def send_request(query: str, k: int, model_choice: str) -> list[str]:
    """Send request to backend and return list of image URLs."""
    try:
        url = "http://localhost:8000/search"
        payload = {"query": [query], "k": k, "model": model_choice}
        response = requests.post(url, json=payload)
    except:
        url = "http://backend-api:8000/search"
        payload = {"query": [query], "k": k, "model": model_choice}
        response = requests.post(url, json=payload)
    return response.json()

def encode_image(image_bytes: bytes) -> str:
    """Encode image to base64."""
    encoded_string = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/png;base64,{encoded_string}"


def get_images(image_folder: str):
    """get all the images in a single image folder """
    images = []
    image_names = []
    IMAGE_KEYFRAME_PATH = "/mlcv/Databases/HCM_AIC23/ "  # Đường dẫn đến thư mục chứa keyframes
    
 
    if int(image_folder[1:3])<=10:
        video_folder=os.path.join(IMAGE_KEYFRAME_PATH,'data-batch-1','keyframes',image_folder)
    elif 10 < int(image_folder[1:3]) <=20: 
        video_folder=os.path.join(IMAGE_KEYFRAME_PATH,'data-batch-2','keyframes',image_folder)
    elif 20 < int(image_folder[1:3]) <=36: 
        video_folder=os.path.join(IMAGE_KEYFRAME_PATH,'data-batch-3','keyframes',image_folder)
        
    for image_file in os.listdir(video_folder):

        image_path = os.path.join(video_folder,image_file)
        image = Image.open(image_path)

        image_names.append( image_folder + " "+ image_file )
        images.append(image)

        
        # keyframe_id= int(keyframe_id)
        
        # if os.path.exists(video_folder):
        #     image_files = sorted(os.listdir(video_folder))


        #     if keyframe_id < len(image_files):

        #         image_file = image_files[keyframe_id]
        #         image_path = os.path.join(video_folder, image_file)
          
        #         image = Image.open(image_path)

        #         image_names.append( video_name + " "+ image_file)
        #         images.append(image)
        #     else:
        #         print(f"Keyframe id {keyframe_id} is out of range for video {video_name}.")

    return images, image_names



def start_sidebar() -> tuple[str, int, str]:
    with st.sidebar.container():
        c1, c2 = st.columns(2)
        mode = c1.radio("Query Mode", ["Text", "Image"])
        k = c2.slider("Number of Images", min_value=1, max_value= 100, step=1, value=20)

        model_choice = st.selectbox("Select a model:", ["ViT-B/32", "ViT-L/14", "ViT-L/14@336px","ViT-g-14",  "ViT-bigG-14" ])


        if mode == "Text":
            query = st.text_input("Query", value="", placeholder="enter your query")
        else:
            query = None
            uploaded_image = st.file_uploader("Query", type=["png", "jpg", "jpeg"])
            if uploaded_image:
                query = encode_image(uploaded_image.read())
                st.image(uploaded_image, use_column_width=True, caption="Query Image")
        st.title("Check the whole keyframes folder")
        text_folder = st.text_input("Video folder", value="", placeholder="e.g L01_V006")
        
        if st.button("Check folder"): 
            images_List ,image_names    =   get_images(text_folder )
   


    
            num_columns = 3  # Number of columns in the grid
            col_count = len(images_List)


            # Loop through the image_paths and display each image in a column
            for i in range(0, col_count, num_columns):
                columns = st.columns(num_columns)  # Create columns for the grid

                for j in range(num_columns):
                    idx = i + j
                    if idx < col_count:
                        with columns[j]:  # Use columns[j] to display images in each column
                            st.image(images_List[idx], use_column_width=True, caption=image_names[idx])




        

        st.title("FOR COMPETITION PURPOSE")
        

        c3, c4 = st.columns(2)
        video_folder= c3.text_input("Video folder", value="", placeholder="e.g L01_V006")
     
        image_file = c4.text_input("Image file", value="", placeholder="e.g  258")


        if st.button("Submit"): 
            response =  get_result(video_folder,int(image_file)  )
            st.json(response)
        return query, k, model_choice
def get_edited_result(query, model_choice, k = 100, image_file = "", video_folder= ""): 
    """Refined search using the clicked image.

    Parameters
    ----------
    query : str
        the query
    model_choice : str 
        the clip model we want to use 
    k : _type_
        Number of images to return

    Returns
    -------
    csv href link to download 
    """
    img_result = send_request(query, k, model_choice)
   
    video_names=[]
    frame_idxs=[]
 
    for result in img_result['search_result']:
      video_name,frame_idx=map_keyframe(result['video_name'],result['keyframe_id'])
      video_names.append(video_name)
      frame_idxs.append(frame_idx)
    

    frame_id = int(image_file)
    print(frame_id)

    #Lay 5 hinh ke tu idx 
    keyframe_dir = "./KeyFrames"


       
   
    
    for i in range(5): 
        Vid_id = video_folder[:3]
        video_folder_name = "keyframes_"+ Vid_id+ "/"+ video_folder
        video_folder = os.path.join(keyframe_dir, video_folder_name)
        if ((frame_id + i)> len(os.listdir(video_folder)) ): 
            break
        video_name,frame_idx=map_keyframe(video_folder ,frame_id + i)

        video_names[i]=video_name
        frame_idxs[i]= frame_idx





    dic={'vd_name':video_names,'fr_id':frame_idxs}
    df=pd.DataFrame(dic)

    csv = df.to_csv( index = None, header=False , sep=" ").encode('utf-8')

    st.download_button(
            "Press to Download",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
            )


def get_session_id(account: str , password: str): 
    """Send request to REST to get the session id."""
    
    url = "https://eventretrieval.one/api/v1/login"
    payload = {"username": account, "password": password}
    response = requests.post(url, json=payload)
    return response.json()
    
    

def get_result(VIDEO_ID: str , FRAME_ID: str ):
    SUBMIT_URL = "https://eventretrieval.one"  # Replace with your actual SUBMIT_URL
    item, frame = map_keyframe(VIDEO_ID, int(FRAME_ID))
    
    session =  get_session_id("eloaic", "Rahphe8h")["sessionId"]  # Replace with your session value
    frame= str(frame)

    URL = f"{SUBMIT_URL}/api/v1/submit?item={item}&frame={frame}&session={session}"

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Check for any HTTP errors
        message = response.json()
        st.json(message) 
    except requests.exceptions.RequestException as error:
        st.write("Error: request exception")
    

    return response.json()




def refined_search(url: str, k) -> list[str]:
    """Refined search using the clicked image.

    Parameters
    ----------
    url : str
        URL of the clicked image
    k : _type_
        Number of images to return

    Returns
    -------
    list[str]
        List of image URLs most similar to the clicked image
    """
    query = fetch_image_bytes(url)
    query = encode_image(query)
    img_urls = send_request(query, k)
    return img_urls



def generate_csv(query, model_choice, k =100):
    img_result = send_request(query, k, model_choice)
  
    video_names=[]
    frame_idxs=[]
 
    for result in img_result['search_result']:
      video_name,frame_idx=map_keyframe(result['video_name'],result['keyframe_id'])
      video_names.append(video_name)
      frame_idxs.append(frame_idx)
    dic={'vd_name':video_names,'fr_id':frame_idxs}
    df=pd.DataFrame(dic)

    csv = df.to_csv( index = None, header=False , sep=" ").encode('utf-8')

    st.download_button(
            "Press to Download",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
            )



def map_keyframe(video_name,key_frame_id):
  PATH_TO_FILE_MAP='./map-keyframes/'
  df=pd.read_csv(PATH_TO_FILE_MAP+video_name+'.csv')
  
  return video_name ,df.frame_idx[key_frame_id-1]

