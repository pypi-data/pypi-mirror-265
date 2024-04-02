from typing import Optional
from .base import PureMLEvalBase

class UnBiasedModel(PureMLEvalBase):
    def __init__(self, model_name: str | None = None, *args, **kwargs):
        model_name = "original" if model_name is None else model_name
        super().__init__(model_name, *args, **kwargs)

    def load_model(self):
        try:
            from Dbias.bias_classification import classifier
        except ImportError as e:
            print("Run `pip install Dbias")
        return classifier

    def _call(self, text):
        return self.model(text)