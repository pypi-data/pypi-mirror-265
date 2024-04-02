from .progess_bar import tqdm_wrapper
from .stats import compute_stats
from typing import Any
from pureml_llm.metric_base import MetricBase


class Flesch_Reading_Ease(MetricBase):
    name: Any = 'flesch_reading_ease'
    input_type: Any = 'text'
    output_type: Any = None
    kwargs: Any = {}


    def parse_data(self,data):
        return data
    

    def compute(self,references,predictions):
        
        """
        Calculates the readability of generated outputs using the Flesch Reading
            Ease Score. This metric takes on float values between (-∞, 121.22], but
            typically ranges between 0 and 100, where higher scores mean the text is
            easier to read.

            The score is based on the number of sentences, words, and syllables in the
            text. See "How to Write Plain English" by Rudolf Franz Flesch for more
            details.

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
                scores = [206.835 - 1.015 * (stat.num_words / stat.num_sentences) - 84.6 *(stat.num_syllables / stat.num_words) for stat in output_stats]
                scores = scores[0]
                return {self.name: scores}
            except Exception as e:
                print(e)


    def risk(self,score):
        threshold = 45
        return { self.name : 'pass'} if score[self.name] >= threshold else {self.name : 'fail'}
