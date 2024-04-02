from pureml_llm.metric_base import MetricBase
import numpy as np
from typing import Any
import faiss
import tqdm
from mauve import compute_mauve



class  Mauve(MetricBase):
    name:Any = 'Mauve'
    input_text:Any = 'text'
    output_type:Any = 'text'
    kwargs:Any = {}


    def parse_data(self,data):
        return data 
    

    def compute(self,references,predictions):
        """
        Calculates MAUVE scores between two lists of generated text and reference text.
        Args:
            predictions: list of generated text to score. Each predictions
                should be a string with tokens separated by spaces.
            references: list of reference for each prediction. Each
                reference should be a string with tokens separated by spaces.
        Optional Args:
            num_buckets: the size of the histogram to quantize P and Q. Options: 'auto' (default) or an integer
            pca_max_data: the number data points to use for PCA dimensionality reduction prior to clustering. If -1, use all the data. Default -1
            kmeans_explained_var: amount of variance of the data to keep in dimensionality reduction by PCA. Default 0.9
            kmeans_num_redo: number of times to redo k-means clustering (the best objective is kept). Default 5
            kmeans_max_iter: maximum number of k-means iterations. Default 500
            featurize_model_name: name of the model from which features are obtained. Default 'gpt2-large' Use one of ['gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl'].
            device_id: Device for featurization. Supply a GPU id (e.g. 0 or 3) to use GPU. If no GPU with this id is found, use CPU
            max_text_length: maximum number of tokens to consider. Default 1024
            divergence_curve_discretization_size: Number of points to consider on the divergence curve. Default 25
            mauve_scaling_factor: "c" from the paper. Default 5.
            verbose: If True (default), print running time updates
            seed: random seed to initialize k-means cluster assignments.
        Returns:
            mauve: MAUVE score, a number between 0 and 1. Larger values indicate that P and Q are closer,
            frontier_integral: Frontier Integral, a number between 0 and 1. Smaller values indicate that P and Q are closer,
            divergence_curve: a numpy.ndarray of shape (m, 2); plot it with matplotlib to view the divergence curve,
            p_hist: a discrete distribution, which is a quantized version of the text distribution p_text,
            q_hist: same as above, but with q_text.

        """

        if (len(references) != 0) and (len(predictions) != 0):
            try:
                output = compute_mauve(references, predictions)
                #print(output)
                return {self.name: output.mauve}
            except Exception as e:
                print(e)


    def risk(self,score):
        threshold = 0.8
        return { self.name : 'pass'} if score[self.name] >= threshold else {self.name : 'fail'}