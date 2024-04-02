from .progess_bar import tqdm_wrapper
from .stats import compute_stats
from typing import Any
from pureml_llm.metric_base import MetricBase


class Flesch_Kincaid_Grade(MetricBase):
    name : Any = 'flesch_kincaid_grade'
    input_type : Any = 'text'
    output_type : Any = None
    kwargs : Any = {}


    def parse_data(self,data):
        return data
    

    def compute(self,references,predictions):

        """
        Calculates the readability of generated outputs using the Flesch-Kincaid
        Grade Level metric. This metric takes on float values between [-3.40, ∞),
        but typically ranges between 0 and 12 (corresponding to U.S. grade levels),
        where lower scores mean the text is easier to read.

        Like the Flesch Reading Ease Score, this metric is based on the number of
        sentences, words, and syllables in the text.
        
        Args:
            references (str): The reference text. (also called prompt to LLMs)
            predictions (str): The predicted text. (also called as output of LLMs)
        
            predictions are only used in the computation of readability and references are not used.
        
        Returns:
            dict : A dictionary containing the readability as key and it's respective score as value.
        
        """
        if predictions is None:
            raise ValueError("Predictions cannot be None")

        if predictions is not None:
            try: 
                output_stats = [
                compute_stats(output)
                for output in tqdm_wrapper(predictions, desc='Computing stats')]
                scores = [
                0.39 * (stat.num_words / stat.num_sentences) + 11.8 *
                (stat.num_syllables / stat.num_words) - 15.59 for stat in output_stats]
                scores =  scores[0]
                return {self.name: scores}
            except Exception as e:
                print(e)

    def risk(self,score):
        threshold = 18
        return { self.name : 'pass'} if score[self.name] >= threshold else {self.name : 'fail'}