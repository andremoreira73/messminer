## Helper functions for the Notebook

import pandas as pd
from io import StringIO

from pydantic import create_model, Field

from classes import SingleCSVStructure, OverallState


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



##############################################################################################################
def save_cleaned_data(graph_result, file_path: str):
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for cleaned in graph_result['cleaned_csv']:
            cleaned['data_frame'].to_excel(writer, sheet_name=cleaned['sheet_name'], index=False)

