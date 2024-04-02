from .accuracy.rouge_precision import RougeScorePrecision
from .accuracy.rouge_recall import RougeScoreRecall
from .accuracy.rouge_fmeasure import RougeScoreFmeasure
from .accuracy.quasi_exact_match import QuasiExactMatch
from .accuracy.f1 import F1
from .accuracy.rr_10 import RR10
from .accuracy.bert_score_precision import BertScorePrecision
from .accuracy.bert_score_recall import BertScoreRecall
from .accuracy.bert_score_f1 import BertScoreF1
from .accuracy.fluency import Fluency
from .accuracy.sentiment import Sentiment
from .accuracy.flesch_reading_ease import Flesch_Reading_Ease
from .accuracy.flesch_kincaid_grade import Flesch_Kincaid_Grade
#from .accuracy.ai_disclaimer_similarity import AI_Disclaimer_Similarity
from .accuracy.character import Character
from .accuracy.wer import WER
from .accuracy.ter import TERMetric
from .accuracy.charcut_mt import Charcut
from .accuracy.chrf import Chrf
from .accuracy.google_bleu import GoogleBLUE
from .accuracy.mauve_score import Mauve
from .accuracy.meteor import Meteor
from .accuracy.nltk_mt import NltkMT
# from .accuracy.ban_topics import BanTopics
# from .accuracy.gibberish import Gibberish
# from .accuracy.relevance import Relevance
from typing import Any
from pureml.utils.logger import get_logger
logger = get_logger('pureml_llm.accuracy_metrics_result.py')

class Accuracy:
    def __init__(self,metrics):
        self.task_type:Any = 'Accuracy'
        self.references:Any = None
        self.predictions:Any = None


        self.metrics:Any = [
            RougeScorePrecision(),
            RougeScoreRecall(),
            RougeScoreFmeasure(),
            #QuasiExactMatch(),
            #F1(),
            #RR10(),
            #BertScorePrecision(),
            #BertScoreRecall(),
            #BertScoreF1(),
            #Fluency(),
            #Sentiment()
            #Flesch_Reading_Ease(),
            #Flesch_Kincaid_Grade()
            #AI_Disclaimer_Similarity(),
            #Character(),
            #WER(),
            #TERMetric(),
            #Charcut(),
            #Chrf(),
            #GoogleBLUE(),
            #Mauve(),
            #Meteor(),
            #NltkMT()
        ]

        self.metrics:Any = metrics

        self.scores:Any = { }

        self.risk_score:Any = { }

    def compute(self,references,predictions,metrics):
            self.metrics = metrics
            for m in self.metrics:
                try:
                    logger.info(f"Computing {m} in Accuracy")
                    self.scores.update(m.compute(references, predictions))
                    
                except Exception as e:
                    print(e)
                    logger.error(f"Error in Computing {m} in Accuracy. {e}")
            return self.scores
    
    def risk(self):
        for m in self.metrics:
                try:
                    self.risk_score.update(m.risk(self.scores))
                except Exception as e:
                    print(e)
                    
        return self.risk_score




