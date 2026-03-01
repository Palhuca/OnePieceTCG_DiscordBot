from numba.core.annotations.pretty_annotate import Annotate
from pydantic import BaseModel
from typing import List
import operator

from typing_extensions import Annotated


class QueryResult(BaseModel):
    type: str = None
    content: str = None

class QueryList(BaseModel):
    type: str = None
    queries: list[str]
class QueryStructure(BaseModel):
    inputs: list[QueryList]

class ReportState(BaseModel):
    queries: List[QueryList] = []
    final_response: str = None
    user_input: str = None
    queries_results: Annotated[List[QueryResult], operator.add]

