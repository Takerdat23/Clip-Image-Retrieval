from __future__ import annotations

import base64
import requests

import streamlit as st
import pandas as pd 
import os

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

def start_sidebar() -> tuple[str, int, str]:
    with st.sidebar.container():
        c1, c2 = st.columns(2)
        mode = c1.radio("Query Mode", ["Text", "Image"])
        k = c2.slider("Number of Images", min_value=1, max_value=20, step=1, value=10)

        model_choice = st.selectbox("Select a model:", ["ViT-B/32", "ViT-L/14", "ViT-L/14@336px","ViT-H-14-laion2B-s32B-b79K", "ViT-bigG-14-laion2B-39B-b160k" ])


        if mode == "Text":
            query = st.text_input("Query", value="", placeholder="enter your query")
        else:
            query = None
            uploaded_image = st.file_uploader("Query", type=["png", "jpg", "jpeg"])
            if uploaded_image:
                query = encode_image(uploaded_image.read())
                st.image(uploaded_image, use_column_width=True, caption="Query Image")

        

        st.title("FOR COMPETITION PURPOSE")

        # Add a text box for Video folder
        c3 ,c4 = st.columns(2)
        video_folder = c3.text_input("Video folder", value="", placeholder="e.g L01_V006")

        # Add a text box for Image file
        image_file = c4.text_input("Image file", value="", placeholder="e.g 001")

        if st.button("Get edited CSV"): 
            st.write("Downloading CSV...")
            download_link = get_edited_result(query, model_choice, 100, image_file, video_folder)
            st.markdown(download_link, unsafe_allow_html=True)




        # Add a button
        if st.button("Print CSV"):
            st.write("Downloading CSV...")
            download_link = generate_csv(query, model_choice, 100)
            st.markdown(download_link, unsafe_allow_html=True)

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
        keyframeDir = "keyframes_"+ keyframeDir
        video_folder = os.path.join(keyframe_dir, video_folder)
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
  
  return video_name+',',df.frame_idx[key_frame_id-1]

