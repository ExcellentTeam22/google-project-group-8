from dataclasses import dataclass
from typing import List

@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int
# methods that you need to define by yourself


def get_best_k_completions(prefix: str) -> List[AutoCompleteData]:
    pass


