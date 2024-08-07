from __future__ import annotations

from typing import Union

import torch
import faiss
import numpy as np
import pandas as pd
from PIL import Image
from api.utils import *
import open_clip
from open_clip import create_model_from_pretrained, get_tokenizer, create_model_and_transforms

def custom_score(results, top_k):
    """
    Custom scoring function to rank images based on multiple criteria.

    Args:
        results (list of dict): List of results where each result is a dictionary
                                containing 'video_name', 'keyframe_id', and 'score'.
        top_k (int): Number of top results to return.

    Returns:
        list of dict: Top K results based on custom scoring.
    """

    WEIGHT_FAISS_SCORE = 0.6
    WEIGHT_SAME_VIDEO = 0.3

    # Convert results to numpy arrays for easier processing
    scores = np.array([res['score'] for res in results], dtype=float)
    keyframe_ids = np.array([res['keyframe_id'] for res in results], dtype=float)
    video_names = np.array([res['video_name'] for res in results])

    # Normalize FAISS scores to range [0, 1]
    faiss_scores_normalized = (scores - scores.min()) / (scores.max() - scores.min())


    # Calculate same video scores
    same_video_matrix = (video_names[:, None] == video_names[None, :]).astype(float)
    same_video_scores = same_video_matrix.sum(axis=1) - 1  # subtract 1 to exclude self-match

    # Normalize same video scores to range [0, 1]
    same_video_scores_normalized = (same_video_scores - same_video_scores.min()) / (
        same_video_scores.max() - same_video_scores.min())

    # Calculate final scores based on weights
    final_scores = (WEIGHT_FAISS_SCORE * faiss_scores_normalized +
                    WEIGHT_SAME_VIDEO * same_video_scores_normalized)

    # Combine results with final scores
    combined_results = [{
        'video_name': res['video_name'],
        'keyframe_id': int(res['keyframe_id']),
        'faiss_score': float(res['score']),  # Convert to Python float
        'final_score': float(final_scores[i])  # Convert to Python float
    } for i, res in enumerate(results)]

    # Sort results based on final scores in descending order
    sorted_results = sorted(combined_results, key=lambda x: x['final_score'], reverse=True)

    # Return top K results
    return sorted_results[:top_k]

# my search engine 

class TextEmbedding():
    def __init__(self,model_name,pretrain):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model,_, self.preprocess = create_model_from_pretrained(model_name, pretrained=pretrain,device=self.device)
        self.model.eval()
    def __call__(self, text: str,model_name) -> np.ndarray:
        tokenizer = open_clip.get_tokenizer(model_name)
        text = tokenizer([text]).to(self.device)


        with torch.no_grad(), torch.cuda.amp.autocast():
            text_features = self.model.encode_text(text)[0]
            text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features.detach().cpu().numpy()



# use this class if you using a openclip libary model
class searchForOpenClip:
    """Object that performs semantic search on images and text

    Parameters
    ----------
    model_id : str
        open clip model 
    pretrain :str 
        open clip pretrain
    index : faiss.Index, optional
        Faiss index with embeddings to search, by default None
    """
    def __init__(self, model_id: str, pretrain: str , index: faiss.Index=None, db: list=[]) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        
        self.model,_, self.preprocess = create_model_and_transforms(model_id, pretrained=pretrain,device=self.device)
        self.model.eval()
        self.model_name = model_id
        self.index = index
        self.database = db
        
    

    def process(self, batch: list[Union[Image.Image, str]]) -> np.array:
        """Process a batch of images or text to extract their embeddings

        Parameters
        ----------
        batch : Union[list[Image.Image], list[str]]
            Batch containing images or text

        Returns
        -------
        np.array
            Resulting batch embeddings
        """
        self.model.to(self.device)
        mode = self._infer_type(batch)
        if mode=="visual":
            processed_images = self.processor(images=batch, return_tensors="pt").to(self.device)
            return self.model.get_image_features(**processed_images).detach().cpu().numpy()
            #image_input = self.preprocess(image).unsqueeze(0).to(self.device)

            #with torch.no_grad(), torch.cuda.amp.autocast():
              #image_features = self.model.encode_image(image_input)[0]
              #image_features /= image_features.norm(dim=-1, keepdim=True)
        elif mode=="text":
           
            # tokenizer = get_tokenizer(self.model_name)
            # text = tokenizer(batch).to(self.device)
           

            # with torch.no_grad(), torch.cuda.amp.autocast():
            #     text_features = self.model.encode_text(text)
            #     #print(text_feature.shape)
            #     text_features /= text_features.norm(dim=-1, keepdim=True)

            #     # text_feature = proj_model.query_proj(text_feature)

            #     # text_feature = F.normalize(text_feature, dim=-1)

            # return text_features.detach().cpu().numpy()

            tokenizer = get_tokenizer(self.model_name)
            text = tokenizer(batch).to(self.device)


            with torch.no_grad(), torch.cuda.amp.autocast():
                text_features = self.model.encode_text(text)[0]
                text_features /= text_features.norm(dim=-1, keepdim=True)
                text_features = text_features.unsqueeze(0)
            return text_features.detach().cpu().numpy()

    

    def __call__(self, query: list[Union[Image.Image, str]], k: int=5) -> list[str]:
        """Perform a semantic search on a batch of images or text

        Parameters
        ----------
        query : Union[list[Image.Image], list[str]]
            THe input query used to perform the search
        k : int, optional
            Number of items return from query, by default 5

        Returns
        -------
        np.array
            An array containing the indexes of the k most similar items
        """
        # Query embedding
        # if not isinstance(query, list):
        #     query = [query]
        # query_emb = self.process(query)
        # query_emb /= np.linalg.norm(query_emb)
        # # Getting Similarities
        # #I: index


        # measure = self.index.search(query_emb, k)
        # #tuple of two arrays distance , index

        # measure  = np.reshape(np.array(measure), newshape=(2, k)).T
        # # sort the result
        # sorted_indices = np.argsort(measure[:, 0])
        # measure  = measure[sorted_indices]

        # '''Trả về top K kết quả'''
        # search_result = []
        # for instance in measure:
        #     distance, ins_id = instance
        #     ins_id = int(ins_id)
        #     video_name, idx = self.database[ins_id][0], self.database[ins_id][1]

        #     search_result.append({"video_name": video_name,
        #                           "keyframe_id": idx,
        #                           "score": distance})


        ##### MY CUSTOM SEARCH ENGINE

        if not isinstance(query, list):
             query = [query]
        
        text_query = split_paragraph_into_sentences(query[0])
    
        # Embed each query
        text_feat_arr = np.vstack([self.process(t) for t in text_query])

        # Normalize the embeddings
        text_feat_arr = text_feat_arr / np.linalg.norm(text_feat_arr, axis=1, keepdims=True)

        # Perform FAISS search for all queries in a batch
        distances, indices = self.index.search(text_feat_arr, k)

        # Flatten the distances and indices arrays
        distances = distances.flatten()
        indices = indices.flatten()

        # Collect the results into structured numpy arrays
        video_names = np.array([self.database[idx][0] for idx in indices])
        keyframe_ids = np.array([self.database[idx][1] for idx in indices])

        # Create a structured array to hold the results
        dtype = [('video_name', 'U50'), ('keyframe_id', 'int32'), ('score', 'float64')]
        results_array = np.zeros(len(distances), dtype=dtype)
        results_array['video_name'] = video_names
        results_array['keyframe_id'] = keyframe_ids
        results_array['score'] = distances.astype('float64') 

        # Calculate mean scores in a vectorized way
        unique_keys, unique_indices, unique_counts = np.unique(
            results_array[['video_name', 'keyframe_id']], return_inverse=True, return_counts=True
        )
        sum_scores = np.bincount(unique_indices, weights=results_array['score'])
        mean_scores = sum_scores / unique_counts

        # Create a list of results with mean scores
        updated_search_result = []
        for i, key in enumerate(unique_keys):
            video_name, keyframe_id = key
            updated_search_result.append({
                "video_name": video_name,
                "keyframe_id": int(keyframe_id),
                "score": float(mean_scores[i])
            })

        # Apply custom scoring to the aggregated results
        final_result = custom_score(updated_search_result, top_k= k)
        return final_result



        ### FUSED SEARCH ENGINE 

        # if not isinstance(query, list):
        #      query = [query]
        
        # text_query = query[0].split(',')
        
     
        # text_feat_arr = np.vstack([self.process(t) for t in text_query])

        # search_result = fused_query_search(text_feat_arr, self.database, k)

        # return search_result
    
    @staticmethod
    def _infer_type(x: list[Union[Image.Image, str]]) -> str:
        """Infers the type of the input batch

        Parameters
        ----------
        x : Union[list[Image.Image], list[str]]
            Input batch

        Returns
        -------
        str
            Type of the input batch
        """
        return "visual" if isinstance(x[0], Image.Image) else "text"


class SemanticSearcher:
    """Object that performs semantic search on images and text

    Parameters
    ----------
    model_id : str
        HuggingFace model id for MultiModal model
    index : faiss.Index, optional
        Faiss index with embeddings to search, by default None
    """

    #def__init__(self, model_id: str, pretrain: str, index: faiss.Index=None, db: list=[])-> None:
        #self.model,_, self.preprocess = open_clip.create_model_and_transforms(self.model_id, pretrained=self.pretrain,device=self.device)
    

    def __init__(self, model_id: str, index: faiss.Index=None, db: list=[]) -> None:
        self.model, self.processor = load_model(model_id)
        self.index = index
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.database = db


    def process(self, batch: list[Union[Image.Image, str]]) -> np.array:
        """Process a batch of images or text to extract their embeddings

        Parameters
        ----------
        batch : Union[list[Image.Image], list[str]]
            Batch containing images or text

        Returns
        -------
        np.array
            Resulting batch embeddings
        """
        self.model.to(self.device)
        mode = self._infer_type(batch)
        if mode=="visual":
            processed_images = self.processor(images=batch, return_tensors="pt").to(self.device)
            return self.model.get_image_features(**processed_images).detach().cpu().numpy()
            #image_input = self.preprocess(image).unsqueeze(0).to(self.device)

            #with torch.no_grad(), torch.cuda.amp.autocast():
              #image_features = self.model.encode_image(image_input)[0]
              #image_features /= image_features.norm(dim=-1, keepdim=True)
        elif mode=="text":
            #text_tokens= open_clip.tokenize().to(device)
            #with torch.no_grad():
            # text_features=  model.encode_text(text_tokens).float()
            #text_features /= text_features.norm(dim=-1, keepdim=True)
            processed_text = self.processor(text=batch, return_tensors="pt", padding=True).to(self.device)
            return self.model.get_text_features(**processed_text).detach().cpu().numpy()

    def __call__(self, query: list[Union[Image.Image, str]], k: int=5) -> list[str]:
        """Perform a semantic search on a batch of images or text

        Parameters
        ----------
        query : Union[list[Image.Image], list[str]]
            THe input query used to perform the search
        k : int, optional
            Number of items return from query, by default 5

        Returns
        -------
        np.array
            An array containing the indexes of the k most similar items
        """
        # Query embedding
        if not isinstance(query, list):
            query = [query]
        query_emb = self.process(query)
        query_emb /= np.linalg.norm(query_emb)
        # Getting Similarities
        #I: index

        _, I = self.index.search(query_emb, k)
        I = I.tolist()

        measure = self.index.search(query_emb, k)
        #tuple of two arrays distance , index

        measure  = np.reshape(np.array(measure), newshape=(2, k)).T
        # sort the result
        sorted_indices = np.argsort(measure[:, 0])
        measure  = measure[sorted_indices]

        '''Trả về top K kết quả'''
        search_result = []
        for instance in measure:
            distance, ins_id = instance
            ins_id = int(ins_id)
            video_name, idx = self.database[ins_id][0], self.database[ins_id][1]

            search_result.append({"video_name": video_name,
                                  "keyframe_id": idx,
                                  "score": distance})
        return search_result

    @staticmethod
    def _infer_type(x: list[Union[Image.Image, str]]) -> str:
        """Infers the type of the input batch

        Parameters
        ----------
        x : Union[list[Image.Image], list[str]]
            Input batch

        Returns
        -------
        str
            Type of the input batch
        """
        return "visual" if isinstance(x[0], Image.Image) else "text"