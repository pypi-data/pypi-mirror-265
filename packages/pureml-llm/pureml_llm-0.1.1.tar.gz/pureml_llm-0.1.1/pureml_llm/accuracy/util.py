# import importlib
# import json
# import logging
# import re
# import sys
# from functools import lru_cache
# from typing import Any, Dict, List, Literal, Optional




# # Detect pytorch device
# @lru_cache(maxsize=None)  # Unbounded cache
# def device():
#     torch = lazy_load_dep("torch")
#     if torch.cuda.is_available():
#         return torch.device("cuda:0")
#     elif torch.backends.mps.is_available():
#         return torch.device("mps")

#     return torch.device("cpu")




# def lazy_load_dep(import_name: str, package_name: Optional[str] = None):
#     """Helper function to lazily load optional dependencies. If the dependency is not
#     present, the function will raise an error _when used_.

#     NOTE: This wrapper adds a warning message at import time.
#     """

#     if package_name is None:
#         package_name = import_name

#     spec = importlib.util.find_spec(import_name)
#     if spec is None:
#         # LOGGER.warning(
#         #     f"Optional feature dependent on missing package: {import_name} was initialized.\n"
#         #     f"Use `pip install {package_name}` to install the package if running locally."
#         # )
#         print(f"Optional feature dependent on missing package: {import_name} was initialized.\n")

#     return importlib.import_module(import_name)


# def calculate_risk_score(score: float, threshold: float) -> float:
#     if score > threshold:
#         return 1.0

#     risk_score = round(abs(score - threshold) / threshold, 1)
#     # Ensure risk score is between 0 and 1
#     return min(max(risk_score, 0), 1)


# def chunk_text(text: str, chunk_size: int) -> List[str]:
#     text = text.strip()
#     return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]



# def split_text_by_sentences(text: str) -> List[str]:
#     nltk = lazy_load_dep("nltk")

#     try:
#         nltk.data.find("tokenizers/punkt")
#     except LookupError:
#         nltk.download("punkt")

#     return nltk.sent_tokenize(text.strip())