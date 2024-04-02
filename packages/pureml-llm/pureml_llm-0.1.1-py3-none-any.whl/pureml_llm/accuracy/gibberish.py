# from enum import Enum
# from typing import List, Optional, Union, Any
# from pureml_llm.metric_base import MetricBase

# from .model import Model
# from .transformers_helpers import get_tokenizer_and_model_for_classification, pipeline
# from .util import calculate_risk_score, split_text_by_sentences

# DEFAULT_MODEL = Model(
#     path="madhurjindal/autonlp-Gibberish-Detector-492513457",
#     onnx_path="madhurjindal/autonlp-Gibberish-Detector-492513457",
#     onnx_subfolder="onnx",
#     pipeline_kwargs={"truncation": True},
# )


# class MatchType(Enum):
#     SENTENCE = "sentence"
#     FULL = "full"

#     def get_inputs(self, prompt: str) -> List[str]:
#         if self == MatchType.SENTENCE:
#             return split_text_by_sentences(prompt)

#         return [prompt]


# class Gibberish(MetricBase):
#     name: str = "gibberish"
#     input_type: str = "text"
#     output_type: Any = None
#     kwargs: Any = {}
#     """
#     A scanner that detects gibberish text.
#     """

#     def parse_data(self, data):
#         return data

#     def compute(self, references,predictions,model = None, use_onnx = False,match_type= MatchType.FULL):
#         print(f"This is being executed. {self.name}")
#         if isinstance(match_type, str):
#             match_type = MatchType(match_type)

#         match_type = match_type

#         if model is None:
#             model = DEFAULT_MODEL

#         tf_tokenizer, tf_model = get_tokenizer_and_model_for_classification(
#             model=model,
#             use_onnx=use_onnx,
#         )

#         classifier = pipeline(
#             task="text-classification",
#             model=tf_model,
#             tokenizer=tf_tokenizer,
#             **model.pipeline_kwargs,
#         )

#         if len(references) == 0 and len(references) > 1:
#             return {self.name: 0}
        
#         highest_score = 0.0
#         results_all = classifier(match_type.get_inputs(references))
#         print(f"Results in Gibberish: {results_all}")
#         for result in results_all:
#             score = round(
#                 1 - result["score"] if result["label"] == "clean" else result["score"],
#                 2,
#             )
#             if score > highest_score:
#                 highest_score = score    

#         return {self.name: highest_score}

#     def risk(self, score):
#         pass