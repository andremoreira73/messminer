## Helper functions for the Notebook

import pandas as pd
from io import StringIO

from pydantic import create_model, Field

from prompts import examiner_prompt_template
from classes import SingleCSVStructure



########################################################
def load_excel_as_csv(file_path: str) -> dict[str, str]:
    """
    Load an Excel file and convert each sheet to CSV text format.

    Args:
        file_path: Path to the Excel file

    Returns:
        Dictionary mapping sheet names to their CSV string representations
    """
    # Read all sheets from the Excel file
    excel_file = pd.ExcelFile(file_path)

    sheets_as_csv = {}

    for sheet_name in excel_file.sheet_names:
        # Read the sheet
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # Convert to CSV string (not DataFrame)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_string = csv_buffer.getvalue()

        sheets_as_csv[sheet_name] = csv_string

    return sheets_as_csv


############################################################
def prepare_examiner_prompt(background_by_user: str) -> str:
    """
    Prepares an extra piece of text for the LLM in case the user provided some background
    """

    if background_by_user:
        background = f"Besides the csv data, the user also provided this background information: {str(background_by_user)}"
    else:
        background = ""

    examiner_prompt = examiner_prompt_template.format(background=background)

    return examiner_prompt


##############################################################
def build_model_from_structure(structure: SingleCSVStructure):

    type_map = {"str": str, "int": int, "float": float, "bool": bool}
    
    fields = {}
    for f in structure.fields:
        py_type = type_map[f.field_type]
        if f.optional:
            py_type = py_type | None
        fields[f.name] = (py_type, Field(..., description=f.description, json_schema_extra={"original_name": f.original_name}))
    
    return create_model("DynamicModel", **fields)