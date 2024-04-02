from .hallicunation.hallicunation_hugging_face import HallucinationMetric
from typing import Any
from pureml.utils.logger import get_logger
logger = get_logger('pureml_llm.hallicunation_metrics_result.py')

class Hallicunation:
    def __init__(self,metrics):
        self.task_type: Any = 'Hallucination'
        self.references: Any = None
        self.predictions: Any = None


        self.metrics: Any = [
            HallucinationMetric()
        ]
        self.metrics: Any = metrics
        self.scores: Any = { }

        self.risk_score: Any = { }

    def compute(self,references,predictions,metrics):
            self.metrics = metrics
            for m in self.metrics:
                try:
                    logger.info(f"Computing {m} in Hallucination")
                    self.scores.update(m.compute(references, predictions))
                except Exception as e:
                    print(e)
                    logger.error(f"Error in Computing {m} in Hallucination. {e}")
            #print(self.scores.keys( ))
            #print(self.scores)
            return self.scores
    
    def risk(self):
        for m in self.metrics:
                self.risk_score.update(m.risk(self.scores))

        return self.risk_score




