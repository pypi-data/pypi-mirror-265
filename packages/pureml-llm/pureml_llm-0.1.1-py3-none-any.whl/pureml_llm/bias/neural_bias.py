from typing import Optional
from pureml_llm.model.unbias_model import UnBiasedModel

def neural_bias_score(text: str, model: Optional[str] = None) -> float:
        try:
            from pureml_llm.model.unbias_model import UnBiasedModel
            # scorer = UnBiasedModel(model_name=model)
            # return scorer(text)
        except Exception as e:
            print(f"Unable to load UnBiasedModel.\n{e}")
        scorer = UnBiasedModel(model_name=model)
        return scorer(text)