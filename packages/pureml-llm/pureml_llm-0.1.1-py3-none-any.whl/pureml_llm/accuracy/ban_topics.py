# from typing import Optional, Sequence, Any 
# from .model import Model
# from .transformers_helpers import get_tokenizer_and_model_for_classification, pipeline
# from pureml_llm.metric_base import MetricBase


# # This model was trained on a mixture of 33 datasets and 389 classes reformatted in the universal NLI format.
# # The model is English only. You can also use it for multilingual zeroshot classification by first machine translating texts to English.
# MODEL_LARGE = Model(
#     path="MoritzLaurer/deberta-v3-large-zeroshot-v1.1-all-33",
#     onnx_path="MoritzLaurer/deberta-v3-large-zeroshot-v1.1-all-33",
#     onnx_subfolder="onnx",
#     pipeline_kwargs={
#         "max_length": 512,
#         "truncation": True,
#     },
# )

# # This is essentially the same as its larger sister MoritzLaurer/deberta-v3-large-zeroshot-v1.1-all-33 only that it's smaller.
# # Use it if you need more speed. The model is English-only.
# MODEL_BASE = Model(
#     path="MoritzLaurer/deberta-v3-base-zeroshot-v1.1-all-33",
#     onnx_path="MoritzLaurer/deberta-v3-base-zeroshot-v1.1-all-33",
#     onnx_subfolder="onnx",
#     pipeline_kwargs={
#         "max_length": 512,
#         "truncation": True,
#     },
# )

# # Same as above, just smaller/faster.
# MODEL_XSMALL = Model(
#     path="MoritzLaurer/deberta-v3-xsmall-zeroshot-v1.1-all-33",
#     onnx_path="MoritzLaurer/deberta-v3-xsmall-zeroshot-v1.1-all-33",
#     onnx_subfolder="onnx",
#     pipeline_kwargs={
#         "max_length": 512,
#         "truncation": True,
#     },
# )


# class BanTopics(MetricBase):
#     name: str = "ban_topics"
#     input_type: str = "text"
#     output_type: Any = None
#     kwargs: Any = {}

#     """
#     BanTopics class is used to ban certain topics from the prompt.

#     It uses a HuggingFace model to perform zero-shot classification.
#     """

#     def parse_data(self, data):
#         return data

#     def compute(self, references, predictions,model = None,use_onnx = False):
#         print(f"This is being executed. {self.name}")
#         topics = ["politics"]
#         #topics = ["politics", "economy", "entertainment", "environment"]
#         if model is None:
#             model = MODEL_BASE
        
#         tf_tokenizer, tf_model = get_tokenizer_and_model_for_classification(
#             model=model,
#             use_onnx=use_onnx,
#         )

#         classifier = pipeline(
#             task="zero-shot-classification",
#             model=tf_model,
#             tokenizer=tf_tokenizer,
#             **model.pipeline_kwargs,)



#         if len(references) == 0:
#             return {self.name: 0}


#         output_model = classifier(references, topics, multi_label=False)
#         print(f"output_model: {output_model}")
#         label_score = dict(zip(output_model["labels"], output_model["scores"]))
#         print(f"Label Scores: {label_score}")
#         max_score = round(max(output_model["scores"]) if output_model["scores"] else 0, 2)
        
#         print(f"Label Scores: {label_score}")
#         print(f"Max Score: {max_score}")

#         return {self.name: max_score}

#     def risk(self, score):
#         pass
