# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MessMiner is an intelligent data cleaning tool that uses LLMs to transform messy Excel files into clean, structured tables. It uses a three-node LangGraph workflow to analyze, structure, and extract data from Excel files that contain mixed content, empty rows, scattered headers, and formatting artifacts.

**Key Technology:** LangGraph agent orchestration with Google Gemini models, Pydantic for structured outputs, and parallel processing via map-reduce patterns.

## Core Architecture

### Three-Node Workflow

1. **Node 1: Uploader** (`node_upload_and_organize` in MessMiner.ipynb)
   - Loads Excel files and converts each sheet to CSV text format
   - Stores in `OverallState.sheets_as_csv` dictionary

2. **Node 2: Examiner** (`examine_single_csv_node` in MessMiner.ipynb)
   - Analyzes CSV structure using LLM with structured output
   - Processes sheets in parallel using LangGraph's `Send` pattern
   - Returns `SingleCSVStructure` with field definitions (name, type, description)
   - Results appended to `OverallState.csv_structure` list

3. **Node 3: Extractor** (`extract_single_csv_node` in MessMiner.ipynb)
   - Dynamically builds Pydantic models from examiner's field definitions
   - Extracts and validates data using structured LLM output
   - Processes sheets in parallel
   - Produces cleaned pandas DataFrames in `OverallState.cleaned_csv` list

### State Management

- **OverallState**: Tracks entire workflow (user context, file name, sheets as CSV, structures, cleaned data)
- **SingleCSVState**: Used for parallel sheet processing (contains user context, sheet name/value, structure)
- State fields with `Annotated[List[T], operator.add]` support parallel appending from multiple nodes

### Key Files

- **MessMiner.ipynb**: Main workflow implementation, node definitions, graph compilation, examples
- **classes.py**: Pydantic models (`FieldDefinition`, `SingleCSVStructure`, `SingleCSVClean`) and state classes
- **helper_functions.py**: Utilities for dynamic model creation, Excel loading, saving cleaned data
- **prompts.py**: System prompt templates for examiner and extractor nodes

## Development Commands

### Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment variables (copy .env.example to .env and add API keys)
cp .env.example .env
# Edit .env to add: GOOGLE_API_KEY, LANGCHAIN_API_KEY
```

### Running the Workflow

The workflow is executed in Jupyter notebook (`MessMiner.ipynb`):

```python
# Start Jupyter
jupyter notebook MessMiner.ipynb

# Key cells to run in order:
# 1. Imports and setup
# 2. Configure model (choose between gemini-2.5-pro or gemini-2.5-flash)
# 3. Set observability options (LangSmith tracing)
# 4. Define nodes and compile graph
# 5. Set input_file, output_file, and user_context
# 6. Run: graph_result = Mine_this_mess.invoke(initial_state)
# 7. Save: save_cleaned_data(graph_result, output_file)
```

### Model Configuration

Choose models based on data complexity:

```python
# For challenging/complex messy data
model_config_examiner = {
    "model": "google_genai:gemini-2.5-pro",
    "temperature": 1,
    "thinking_budget": -1
}

# For simpler data or faster processing
model_config_examiner = {
    "model": "google_genai:gemini-2.5-flash",
    "temperature": 1,
    "thinking_budget": -1
}
```

### Observability

LangSmith tracing is controlled via environment variables in the notebook:

```python
os.environ["LANGCHAIN_TRACING_V2"] = "true"  # Set to "false" to disable
os.environ["LANGCHAIN_PROJECT"] = "MessMiner_v2"  # Project name in LangSmith
```

## Code Patterns and Conventions

### Parallel Processing with LangGraph Send

Both examiner and extractor nodes use conditional edges that return `Send` patterns to process multiple sheets in parallel:

```python
def examine_in_parallel_node(state: OverallState):
    return [Send("node_2_examiner",
                 {"user_background": user_background,
                  "sheet_name": sheet_name,
                  "sheet_value": sheet_value})
            for sheet_name, sheet_value in state["sheets_as_csv"].items()]
```

### Dynamic Pydantic Model Creation

The extractor dynamically creates Pydantic models at runtime based on examiner results:

```python
# In helper_functions.py
def build_model_from_structure(structure: SingleCSVStructure):
    type_map = {"str": str, "int": int, "float": float, "bool": bool}
    fields = {}
    for f in structure.fields:
        py_type = type_map[f.field_type]
        if f.optional:
            py_type = py_type | None
        fields[f.name] = (py_type, Field(..., description=f.description))
    return create_model("DynamicModel", **fields)
```

### Structured LLM Output

All LLM calls use `.with_structured_output()` to ensure Pydantic-validated responses:

```python
llm = init_chat_model(**model_config_examiner)
structured_llm = llm.with_structured_output(SingleCSVStructure)
response = structured_llm.invoke(message_for_llm)
```

### User Context

The `user_background` field in state accepts free-form context to guide the cleaning process. Examples:

```python
user_context = "The file contains agricultural data with empty rows; I need a clean, contiguous table"
user_context = "Technical data in German - translate to English and clean"
```

## Testing Strategy

The notebook includes inline testing sections after each node definition to verify:
- Node return types match expected state structure
- LLM responses follow Pydantic schema
- State updates append correctly to lists

When modifying nodes, run these test cells before executing the full graph.

## Example Files

- **Example_0.xlsx**: Agricultural data with empty rows (straightforward)
- **Example_1.xlsx**: Technical/price data in German (translation required)
- **Example_2.xlsx**: Trial management software output (complex restructuring)

## Requirements

- Python 3.11
- LangChain 0.3.26+, LangGraph 0.4.7+
- Google Gemini API access (API key in .env)
- Optional: LangSmith API key for observability

## Development Notes

- The notebook uses `%autoreload 2` to auto-reload code from .py files during development
- Nodes are tested individually before graph compilation
- State classes use TypedDict for static typing and runtime validation
- All LLM interactions are traceable via LangSmith when enabled
