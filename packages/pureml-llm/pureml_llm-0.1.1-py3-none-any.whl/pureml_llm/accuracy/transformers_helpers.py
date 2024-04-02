# import importlib
# from functools import lru_cache
# from typing import Literal, Union, get_args

# from transformers import (
#     PreTrainedModel,
#     PreTrainedTokenizer,
#     PreTrainedTokenizerFast,
#     TFPreTrainedModel,
# )

# from .model import Model
# from .util import device, lazy_load_dep



# def get_tokenizer(model: Model, **kwargs):
#     """
#     This function loads a tokenizer given a model identifier and caches it.
#     Subsequent calls with the same model_identifier will return the cached tokenizer.

#     Args:
#         model (Model): The model to load the tokenizer for.
#     """
#     transformers = lazy_load_dep("transformers")
#     tokenizer = transformers.AutoTokenizer.from_pretrained(model.path, **kwargs)
#     return tokenizer


# @lru_cache(maxsize=None)  # Unbounded cache
# def is_onnx_supported() -> bool:
#     is_supported = importlib.util.find_spec("optimum.onnxruntime") is not None
#     if not is_supported:
#         print(f"Please install Optimum")

#     return is_supported


# def _ort_model_for_sequence_classification(
#     model: Model,
# ):
#     if device().type == "cuda":
#         optimum_onnxruntime = lazy_load_dep("optimum.onnxruntime", "optimum[onnxruntime-gpu]")
#         tf_model = optimum_onnxruntime.ORTModelForSequenceClassification.from_pretrained(
#             model.onnx_path or model.path,
#             export=model.onnx_path is None,
#             file_name=model.onnx_filename,
#             provider="CUDAExecutionProvider",
#             use_io_binding=True,
#             subfolder=model.onnx_subfolder,
#             **model.kwargs,
#         )


#         return tf_model

#     optimum_onnxruntime = lazy_load_dep("optimum.onnxruntime", "optimum[onnxruntime]")
#     tf_model = optimum_onnxruntime.ORTModelForSequenceClassification.from_pretrained(
#         model.onnx_path or model.path,
#         export=model.onnx_path is None,
#         file_name=model.onnx_filename,
#         subfolder=model.onnx_subfolder,
#         **model.kwargs,
#     )

#     return tf_model


# def get_tokenizer_and_model_for_classification(
#     model: Model,
#     use_onnx: bool = False,
# ):
#     """
#     This function loads a tokenizer and model given a model identifier and caches them.
#     Subsequent calls with the same model_identifier will return the cached tokenizer.

#     Args:
#         model (str): The model identifier to load the tokenizer and model for.
#         use_onnx (bool): Whether to use the ONNX version of the model. Defaults to False.
#     """
#     tf_tokenizer = get_tokenizer(model, **model.kwargs)
#     transformers = lazy_load_dep("transformers")

#     if use_onnx and is_onnx_supported() is False:

#         use_onnx = False

#     if use_onnx is False:
#         tf_model = transformers.AutoModelForSequenceClassification.from_pretrained(
#             model.path, subfolder=model.subfolder, **model.kwargs
#         )

#         return tf_tokenizer, tf_model

#     # Hack for some models
#     tf_tokenizer.model_input_names = ["input_ids", "attention_mask"]

#     tf_model = _ort_model_for_sequence_classification(model)

#     return tf_tokenizer, tf_model


# ClassificationTask = Literal["text-classification", "zero-shot-classification"]


# def pipeline(
#     task: str,
#     model: Union[PreTrainedModel, TFPreTrainedModel],
#     tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
#     **kwargs,
# ):

#     if kwargs.get("max_length", None) is None:
#         kwargs["max_length"] = tokenizer.model_max_length

#     transformers = lazy_load_dep("transformers")
#     return transformers.pipeline(
#         task,
#         model=model,
#         tokenizer=tokenizer,
#         device=device(),
#         batch_size=1,
#         **kwargs,
#     )