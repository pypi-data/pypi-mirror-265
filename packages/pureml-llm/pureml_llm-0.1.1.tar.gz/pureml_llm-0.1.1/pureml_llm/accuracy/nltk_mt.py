from pureml_llm.metric_base import MetricBase
from typing import Any 
import nltk 

try:
    nltk.data.find('perluniprops')
except LookupError:
    nltk.download('perluniprops') 

from nltk.tokenize.nist import NISTTokenizer
from nltk.translate.nist_score import corpus_nist, sentence_nist


class NltkMT(MetricBase):
    name:Any = 'nltk_mt'
    input_type: Any = 'text'
    output_type:Any = 'text'
    kwargs: Any = {}


    def parse_data(self,data):
        return data 
    

    def compute(self,references,predictions):

        """
            DARPA commissioned NIST to develop an MT evaluation facility based on the BLEU
            score. The official script used by NIST to compute BLEU and NIST score is
            mteval-14.pl. The main differences are:

            - BLEU uses geometric mean of the ngram precisions, NIST uses arithmetic mean.
            - NIST has a different brevity penalty
            - NIST score from mteval-14.pl has a self-contained tokenizer (in the Hugging Face implementation we rely on NLTK's
            implementation of the NIST-specific tokenizer)
            

             Computes NIST score of translated segments against one or more references.
        Args:
                predictions: predictions to score (list of str)
                references: potentially multiple references for each prediction (list of str or list of list of str)
                n: highest n-gram order
                lowercase: whether to lowercase the data (only applicable if 'western_lang' is True)
                western_lang: whether the current language is a Western language, which will enable some specific tokenization
            rules with respect to, e.g., punctuation

        Returns:
                'nist_mt': nist_mt score

        """
        try:
            tokenizer = NISTTokenizer()

            # Account for single reference cases: references always need to have one more dimension than predictions
            if isinstance(references[0], str):
                references = [[ref] for ref in references]

            predictions = [
                tokenizer.tokenize(pred)
                for pred in predictions
            ]
            references = [
                [
                    tokenizer.tokenize(ref)
                    for ref in ref_sentences
                ]
                for ref_sentences in references
            ]
            result = corpus_nist(list_of_references=references, hypotheses=predictions)
            return {self.name: result}
    
        except Exception as e:
            print(f"Error: {e}")
            
    
    def risk(self,scores):
        threshold = 0.8
        return {self.name: "pass" if scores[self.name] > threshold else "fail"}