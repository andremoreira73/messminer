
import operator
import pandas as pd

from pydantic import BaseModel, Field, create_model
from typing import (List, Dict, Any, Optional, TypedDict, Literal, Annotated)

# State class ensures that the nodes have access to the same information
# note that we will not track the messages that are passed to the LLMs as part of the state - not necessary in this workflow!
# This is the information that, one way or another, all LLMs will access in bits and pieces

## Structured responses

# First, we define bottom up how the LLM structured output should look like - note that this will form the basis
# of a future dynamic class for the node 3's structured output
class FieldDefinition(BaseModel):
    # This is like a bottom, piece by piece definition of what a pydantic model needs for validation
    name: str = Field(..., description="The field/column name (cleaned, valid Python identifier)")
    original_name: str = Field(..., description="Original column name from CSV, if available")
    field_type: Literal["str", "int", "float", "bool"] = Field(..., description="Python type")
    description: str = Field(..., description="What this field represents")
    optional: bool = Field(default=False, description="Whether the field can be None")

class SingleCSVStructure(BaseModel):
    # This is the structure, as a whole, for a singular CSV
    sheet_name: Optional[str] = Field(None, description="Name of the source sheet")
    fields: list[FieldDefinition] = Field(..., description="List of field definitions for the table")

class SingleCSVClean(TypedDict):
    # This is the cleaned dataframe, including its sheet name
    # We don't need to use pydantic here, as this will not be part of a structured output
    sheet_name: str
    data_frame: pd.DataFrame

## States

# We create a "private" state for a single csv processing
# Needed for the map-reduce via Send 
class SingleCSVState(TypedDict):
    user_background: str
    sheet_name: str
    sheet_value: str
    csv_structure: SingleCSVStructure


class OverallState(TypedDict):
    user_background: str
    file_name: str
    # Each sheet in the file is extracted as a csv, put in this dict with "sheet_name":"extracted_csv"
    sheets_as_csv: dict  
    
    # The list of csv structures will be built by agents working in parallel (one per extracted csv), therefore it needs to allow appending;
    # Annotated type with operator.add ensures that new messages are appended to the existing list rather than replacing it.
    # See: https://docs.langchain.com/oss/python/langgraph/quickstart#2-define-state
    csv_structure: Annotated[List[SingleCSVStructure], operator.add]
    cleaned_csv: Annotated[List[SingleCSVClean], operator.add]