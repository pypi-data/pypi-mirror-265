from .toxicity.toxicity_from_prespective import ToxicityAPI
from .toxicity.insult import ToxicityAPIInsult
from .toxicity.severe_toxicity import ToxicityAPISEVERE_TOXICITY
from .toxicity.profanity import ToxicityAPIPROFANITY
from .toxicity.identity_attack import ToxicityAPIIDENTITY_ATTACK
from typing import Any
from pureml.utils.logger import get_logger
logger = get_logger('pureml_llm.toxicity_metrics_result.py')

class Toxicity:
    def __init__(self,metrics):
        self.task_type : Any = 'Toxicity'
        self.api_key: Any = None
        self.text: Any = None

        self.metrics: Any = [
            ToxicityAPI(),
            ToxicityAPIInsult(),
            ToxicityAPISEVERE_TOXICITY(),
            ToxicityAPIPROFANITY(),
            ToxicityAPIIDENTITY_ATTACK()
        ]
        self.metrics: Any = metrics

        self.scores:Any = {}  # Change this to a dict
        self.risk_score:Any = {}

    def compute(self,predictions,api_key:str,metrics,references:str = None):
        self.metrics = metrics
        for m in self.metrics:
            try:
                logger.info(f"Computing {m} in Toxicity")
                # Extend self.scores with the list of dictionaries returned by m.compute(...)
                self.scores.update(m.compute(api_key=api_key, text=predictions))
            except Exception as e:
                print(e)
                logger.error(f"Error in Computing {m} in Toxicity. {e}")
        #print(self.scores)
        return self.scores

    def risk(self):
        print(self.scores)
        for m in self.metrics:
            # Extend self.risk_score with the list of dictionaries returned by m.risk(...)
            self.risk_score.update(m.risk(self.scores))  # Assuming m.risk(...) returns a list of dictionaries
        return self.risk_score
