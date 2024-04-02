# from typing import Optional, Any
# from .model import Model
# from .transformers_helpers import get_tokenizer, is_onnx_supported
# from .util import device, lazy_load_dep
# from pureml_llm.metric_base import MetricBase
# import torch
# import numpy as np

# MODEL_EN_BGE_BASE = Model(
#     path="BAAI/bge-base-en-v1.5",
#     onnx_path="neuralmagic/bge-base-en-v1.5-quant",  # Quantized and converted to ONNX version of BGE base
# )
# MODEL_EN_BGE_LARGE = Model(
#     path="BAAI/bge-large-en-v1.5",
#     onnx_path="neuralmagic/bge-large-en-v1.5-quant",  # Quantized and converted to ONNX version of BGE large
# )
# MODEL_EN_BGE_SMALL = Model(
#     path="BAAI/bge-small-en-v1.5",
#     onnx_path="neuralmagic/bge-small-en-v1.5-quant",  # Quantized and converted to ONNX version of BGE small
# )
# # Assume MODEL constants are defined elsewhere in your code

# class Relevance(MetricBase):  # Inherit from BaseModel and MetricBase
#     name: Any = "relevance"
#     input_type: str = "text"
#     output_type: Any = None
#     threshold: float = 0.5
#     model: Model
#     tokenizer: Any = None  # Added tokenizer as an attribute
#     pooling_method: str = "cls"
#     normalize_embeddings: bool = True

#     def __init__(
#         self,
#         *,
#         threshold: float = 0.5,
#         model: Optional[Model] = None,
#         use_onnx: bool = False
#     ):
#         super().__init__()  # Initialize Pydantic BaseModel

#         if model is None:
#             model = MODEL_EN_BGE_BASE

#         self.threshold = threshold
#         self.model = model

#         if use_onnx and is_onnx_supported() is False:
#             use_onnx = False

#         if use_onnx:
#             optimum_onnxruntime = lazy_load_dep(
#                 "optimum.onnxruntime",
#                 "optimum[onnxruntime-gpu]" if device().type == "cuda" else "optimum[onnxruntime]",
#             )
#             self.model = optimum_onnxruntime.ORTModelForFeatureExtraction.from_pretrained(
#                 model.onnx_path,
#                 export=False,
#                 subfolder=model.onnx_subfolder,
#                 provider="CUDAExecutionProvider"
#                 if device().type == "cuda"
#                 else "CPUExecutionProvider",
#                 use_io_binding=True if device().type == "cuda" else False,
#                 **model.kwargs,
#             )
#         else:
#             transformers = lazy_load_dep("transformers")
#             self.model = transformers.AutoModel.from_pretrained(
#                 model.path, subfolder=model.subfolder, **model.kwargs
#             ).to(device())
#             self.model.eval()

#         self.tokenizer = get_tokenizer(model)

#     # The rest of the methods remain unchanged

#     def pooling(self, last_hidden_state: torch.Tensor, attention_mask: torch.Tensor = None):
#         if self.pooling_method == "cls":
#             return last_hidden_state[:, 0]
#         elif self.pooling_method == "mean":
#             s = torch.sum(last_hidden_state * attention_mask.unsqueeze(-1).float(), dim=1)
#             d = attention_mask.sum(dim=1, keepdim=True).float()
#             return s / d

#     @torch.no_grad()
#     def encode(self, sentence: str, max_length: int = 512) -> np.ndarray:
#         inputs = self.tokenizer(
#             [sentence],
#             padding=True,
#             truncation=True,
#             return_tensors="pt",
#             max_length=max_length,
#         ).to(device())
#         last_hidden_state = self.model(**inputs, return_dict=True).last_hidden_state
#         embeddings = self.pooling(last_hidden_state, inputs["attention_mask"])
#         if self.normalize_embeddings:
#             embeddings = torch.nn.functional.normalize(embeddings, dim=-1)
#         embeddings = embeddings.cpu().numpy()

#         return embeddings[0]

#     def parse_data(self,data):
#         return data

#     def compute(self, references: str, predictions: str, model = None, use_onnx = False):

#         print(f"This is being executed. {self.name}")
#         # if model is None:
#         #     model = MODEL_EN_BGE_BASE

#         # pooling_method = "cls"
#         # normalize_embeddings = True

        
#         # if use_onnx:
#         #     optimum_onnxruntime = lazy_load_dep(
#         #         "optimum.onnxruntime",
#         #         "optimum[onnxruntime-gpu]" if device().type == "cuda" else "optimum[onnxruntime]",
#         #     )
#         #     model = optimum_onnxruntime.ORTModelForFeatureExtraction.from_pretrained(
#         #         model.onnx_path,
#         #         export=False,
#         #         subfolder=model.onnx_subfolder,
#         #         provider="CUDAExecutionProvider"
#         #         if device().type == "cuda"
#         #         else "CPUExecutionProvider",
#         #         use_io_binding=True if device().type == "cuda" else False,
#         #         **model.kwargs,
#         #     )
#         # else:
#         #     transformers = lazy_load_dep("transformers")
#         #     model = transformers.AutoModel.from_pretrained(
#         #         model.path, subfolder=model.subfolder, **model.kwargs
#         #     ).to(device())
#         #     model.eval()

#         # tokenizer = get_tokenizer(model)
        
#         prompt_embedding = self.encode(references)
#         output_embedding = self.encode(predictions)
#         similarity = prompt_embedding @ output_embedding.T

#         return {
#             self.name: similarity
#         }
    
#     def risk(self,score):
#         pass