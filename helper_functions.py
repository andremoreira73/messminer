## Helper functions for the Notebook

import pandas as pd
from io import StringIO

from pydantic import create_model, Field

from classes import SingleCSVStructure, OverallState


##############################################################
def build_model_from_structure(structure: SingleCSVStructure):
    """
    Dynamically create a Pydantic model from a CSV structure definition.

    Args:
        structure: SingleCSVStructure containing field definitions

    Returns:
        Pydantic model class with fields matching the structure
    """
    type_map = {"str": str, "int": int, "float": float, "bool": bool}
    
    fields = {}
    for f in structure.fields:
        py_type = type_map[f.field_type]
        if f.optional:
            py_type = py_type | None
        fields[f.name] = (py_type, Field(..., description=f.description, json_schema_extra={"original_name": f.original_name}))
    
    return create_model("DynamicModel", **fields)


########################################################
def load_excel_as_csv(file_path: str, consolidate_sheets: bool) -> dict[str, str]:
    """
    Load an Excel file and convert each sheet to CSV text format.

    Args:
        file_path: Path to the Excel file
        consolidate_sheets: boolean, check if user wants a consolidated final table

    Returns:
        Dictionary mapping sheet names to their CSV string representations
    """
    # Read all sheets from the Excel file
    excel_file = pd.ExcelFile(file_path)

    sheets_as_csv = {}
    sheets_as_csv_consolidated = []

    for sheet_name in excel_file.sheet_names:
        # Read the sheet
        #df = pd.read_excel(file_path, sheet_name=sheet_name)
        df = excel_file.parse(sheet_name)

        # Convert to CSV string (not DataFrame)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_string = csv_buffer.getvalue()

        if consolidate_sheets:
            # Since we will be passing this as text to an LLM, it is OK if the columns do not match,
            # simply append one after the other
            sheets_as_csv_consolidated.append(csv_string)
        else:
            sheets_as_csv[sheet_name] = csv_string

    # Check if user wants all sheets to be treated "as one" and get one final table
    result = {"consolidated table": "\n".join(sheets_as_csv_consolidated)} if consolidate_sheets else sheets_as_csv

    return result



##############################################################################################################
def save_cleaned_data(graph_result, file_path: str):
    """
    Save cleaned DataFrames to an Excel file with multiple sheets.

    Args:
        graph_result: Graph output containing 'cleaned_csv' list of DataFrames
        file_path: Output Excel file path
    """
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for cleaned in graph_result['cleaned_csv']:
            cleaned['data_frame'].to_excel(writer, sheet_name=cleaned['sheet_name'], index=False)

