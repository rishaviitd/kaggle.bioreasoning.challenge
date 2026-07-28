import difflib
from typing import Tuple

def compare_prompts(prompt_old: str, prompt_new: str) -> Tuple[float, str]:
    """
    Compares two prompt strings to evaluate the magnitude of mutations.
    
    Returns:
        similarity (float): A ratio between 0.0 (completely different) and 1.0 (identical)
        diff_str (str): A unified diff string showing exactly what lines were added/removed
    """
    # 1. Calculate quantitative similarity ratio
    matcher = difflib.SequenceMatcher(None, prompt_old, prompt_new)
    similarity = matcher.ratio()
    
    # 2. Generate unified text diff
    old_lines = prompt_old.splitlines(keepends=True)
    new_lines = prompt_new.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        old_lines, 
        new_lines, 
        fromfile='Old Prompt', 
        tofile='New Mutated Prompt',
        n=2 # Keep 2 lines of context around changes
    )
    diff_str = "".join(diff)
    
    return similarity, diff_str
