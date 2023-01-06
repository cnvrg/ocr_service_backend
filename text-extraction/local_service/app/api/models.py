""" define pydantic data models """
from pydantic import BaseModel
from typing import Optional, List, Dict

class InferenceResults(BaseModel):
    json_extract_results: Optional[Dict[str, List[str]]]

class InferenceIn(BaseModel):
    id: int = None
    remote_files: List[str]

class InferenceOut(BaseModel):
    info: InferenceIn
    results: InferenceResults