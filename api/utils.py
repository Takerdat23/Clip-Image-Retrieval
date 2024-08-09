from __future__ import annotations

import requests
from io import BytesIO
from typing import Union
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
import open_clip
import numpy as np
import nltk
nltk.download('punkt')

def split_paragraph_into_sentences(paragraph):
    sentences = nltk.sent_tokenize(paragraph)
    return sentences

def load_model(model_id: str) -> tuple[CLIPModel, CLIPProcessor]:
    model = CLIPModel.from_pretrained(model_id)
    processor = CLIPProcessor.from_pretrained(model_id)
    return model, processor

def load_model_open(model_id: str, pretrain: str) -> tuple[CLIPModel, CLIPProcessor]:
    model,_, processor = open_clip.create_model_and_transforms(model_id, pretrained=pretrain)
    return model, processor

def fetch_image(url: str) -> tuple[str, Image.Image]:
    """Fetch image from url

    Parameters
    ----------
    url : str
        url of the image

    Returns
    -------
    tuple[str, Image.Image]
        tuple (url, image) where image is PIL image object and url is the url of the image
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return url, Image.open(BytesIO(response.content))
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something Else: {err}")
    return url, None

def index_to_url(index: list[int], url_table: pd.DataFrame) -> list[str]:
    """Converts a list of indices to a list of urls

    Parameters
    ----------
    index : list[int]
        List of indices
    url_table : pd.DataFrame
        DataFrame containing the urls

    Returns
    -------
    list[str]
        List of urls
    """
    return url_table.iloc[index].url.tolist()

class ImageBatchGenerator:
    """
    A generator class that get's as arguments a list of URLs and batch size and generates batches of PIL images
    that are obtained through GET requests to the URLs.

    Parameters
    ----------
    urls : list[str]
        List of URLs to fetch images from
    batch_size : int
        The size of the batches to be generated
    """
    def __init__(self, urls: list[str], batch_size: int=32) -> None:
        self.urls = urls
        self.batch_size = batch_size
        self.executor = ThreadPoolExecutor()
        self.futures = self.executor.map(fetch_image, self.urls)
    
    def __len__(self) -> int:
        return (len(self.urls) + self.batch_size - 1) // self.batch_size

    def __iter__(self) -> ImageBatchGenerator:
        return self

    def __next__(self) -> dict[str, Union[str, Image.Image]]:
        images = []
        urls = []
        for future in self.futures:
            url, image = future
            if image is not None:
                images.append(image)
                urls.append(url)
            if len(images) == self.batch_size:
                break
        if len(images) == 0:
            self.executor.shutdown()
            raise StopIteration
        return {"images": images, "urls": urls}
    


def cumargmax(a):
    m = np.maximum.accumulate(a)
    x = np.arange(a.shape[0])
    x[1:] *= m[:-1] < m[1:]
    np.maximum.accumulate(x, axis=0, out=x)
    return x

def get_best_matched_pair(pairwise_distance):
  # pairwise_distance: (#queries, #frame)

  num_query, num_frame = pairwise_distance.shape

  score = np.zeros(num_frame)
  trace = np.zeros_like(pairwise_distance, dtype="int")

  for i in range(num_query):
    trace[i] = cumargmax(score)
    score = np.maximum.accumulate(score) + pairwise_distance[i]

  best_score = np.max(score)

  final_trace = [np.argmax(score)]

  for t in trace[1:][::-1]:
    final_trace.append(t[final_trace[-1]])

  return best_score, final_trace[::-1]


def fused_query_search(query_arr, db, topk=10):
    measure = []
    for ins_id, instance in enumerate(db):
        video_name, feat_arr = instance

        if feat_arr.shape[0] == 0:
            continue

        # Calculate pairwise distances
        pairwise_distance = np.exp(query_arr @ feat_arr.T)

        # Fuse two query distances
        distance = np.log(pairwise_distance.mean(0))

        for i in range(len(distance)):
            measure.append((ins_id, video_name, [i+1], distance[i]))

    # Sort results by distance in descending order
    measure = sorted(measure, key=lambda x: x[-1], reverse=True)

    # Prepare top K results
    search_result = []
    for instance in measure[:topk]:
        ins_id, video_name, matched_ids, distance = instance

        for i in matched_ids:
            search_result.append({
                "video_name": video_name,
                "keyframe_id": i,
                "score": float(distance)  # Convert to Python float
            })

    return search_result



