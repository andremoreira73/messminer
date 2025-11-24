# The Mess Miner

Agents that turn nightmare Excel sheets into organized tables

**Author:** Andre Moreira, November 2025
**Version:** 0.1.0-beta

How often do you have that Excel file with exactly the data you need, but in a format you cannot really use? The data is scattered across sheets and files, or mixed with charts, formulas and merged cells. But it still has the data you **really** need.

## The agent workflow that cleans your data

Mess Miner is an intelligent data cleaning tool that uses Large Language Models (LLMs) to understand and restructure messy data sources. Instead of manually writing complex parsing logic for each data format, Mess Miner analyzes the structure of your data and intelligently extracts it into clean, structured tables.

### Key Features

- **Intelligent Structure Detection**: Uses LLMs to analyze and understand data organization
- **Parallel Processing**: Handles multiple sheets/data sources simultaneously using map-reduce patterns
- **Context-Aware**: Accepts user background information to guide the cleaning process
- **Flexible**: Works Excel files without custom parsing code
- **Observable**: Optional integration with LangSmith for workflow monitoring and debugging
- **Validated Output**: Uses Pydantic for structured response parsing and data validation

### How It Works

Mess Miner uses a three-node graph workflow:

![Mess Miner Workflow](MessMiner_workflow.png)

### Workflow Nodes

1. **Node 1: Uploader**

   - Loads Excel files
   - Converts each sheet to CSV format (text)
   - Organizes data for processing

2. **Node 2: Examiner**

   - Analyzes CSV data structure
   - Identifies relevant columns and data organization
   - Creates field definitions (name, type, description)
   - Processes sheets in parallel (uses LangGraph's Send pattern)

3. **Node 3: Extractor**
   - Dynamically builds Pydantic models based on examiner results
   - Extracts data according to identified structure
   - Cleans data (removes empty rows, validates types)
   - Generates clean pandas DataFrames that can be saved as cleaned Excel file
   - Processes sheets in parallel

## Installation

1. Clone this repository:

```bash
git clone https://github.com/andremoreira73/messminer.git
cd messminer
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env and add your API keys:
# - GOOGLE_API_KEY (for Gemini)
# - LANGCHAIN_API_KEY (for LangSmith)
```

### Claude

I left CLAUDE.md out of .gitignore, so if you happen to use Claude Code (or any other AI tools that use it) you can just jump in, no need to burn tokens with /init

## Usage

### Basic Usage

1. Open `MessMiner.ipynb` in Jupyter
2. Executing the cells under the sections

- Imports
- Observability
- Node 1: uploader
- Node 2: examiner
- Node 3: extractor
- Putting it all together: the Graph

(note that there are "testing areas" under the different sections - these are optional, good for learning / testing)

3. Go to the section _User inputs_ and configure:

```python
input_file = 'Example_0.xlsx'
output_file = 'Example_0_output.xlsx'

# if you want all sheets into one consolidated, organized table, set it to True;
# otherwise, the workflow will treat each sheet separately
consolidate_sheets = False

# Optional: Provide context to guide the cleaning
user_context = """The file contains agricultural data that is almost
correctly structured, but has empty rows. I need a clean, contiguous table."""
```

3. Run the workflow (cell under _User Inputs_):

```python
initial_state = {
    "user_background": str(user_context),
    "file_name": input_file,
    "sheets_as_csv": {}
}
graph_result = Mine_this_mess.invoke(initial_state)
```

4. Save the cleaned output:

```python
save_cleaned_data(graph_result, output_file)
```

### Model Configuration

Choose between Gemini Pro (more capable) or Flash (faster) models:

```python
# For challenging/complex data
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

If you prefer to use other models, add their configuration parameters here
(see documentation here https://docs.langchain.com/oss/python/integrations/chat)
and add the respective API keys to the .env file

## Project Structure

```
.
├── MessMiner.ipynb          # Main notebook with workflow and examples
├── classes.py               # Pydantic models and state definitions
├── helper_functions.py      # Utility functions
├── prompts.py              # LLM prompt templates
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── Example_*.xlsx         # Sample input files
└── Example_*_output.xlsx  # Sample output files
```

## Examples

The repository includes three anonymized example files demonstrating different use cases:

- **Example_0.xlsx**: Agricultural data with empty rows
- **Example_1.xlsx**: Technical/price data in German
- **Example_2.xlsx**: Trial management software output

## Agent Workflow State Management

### OverallState

Tracks the entire workflow state:

- `user_background`: Context information provided by the user
- `file_name`: Input file path
- `sheets_as_csv`: Dictionary of sheet names to CSV strings
- `csv_structure`: List of identified structures
- `cleaned_csv`: List of cleaned DataFrames

### SingleCSVState

Used for parallel processing of individual sheets:

- `user_background`: Shared context
- `sheet_name`: Current sheet identifier
- `sheet_value`: CSV data as string
- `csv_structure`: Structure definition for this sheet

## Technology Stack

- **Python**: 3.11
- **LangGraph**: Agent orchestration and workflow management
- **LangSmith**: Observability and tracing
- **LLMs**: Google Gemini (2.5 Pro, 2.5 Flash)
- **Pydantic**: Structured response parsing and validation
- **Development**: Claude Code for brainstorming and code assistance

**Observability**: LangSmith integration is enabled by default. Configure in the notebook:

```python
os.environ["LANGSMITH_ENDPOINT"] = "https://eu.api.smith.langchain.com"
os.environ["LANGCHAIN_TRACING_V2"] = "true"  # set to "false" if you do not want tracing
os.environ["LANGCHAIN_PROJECT"] = "MessMiner_v2"
```

## License

MIT License © 2025 Andre Moreira - See LICENSE file for details

## Citation

If you use Mess Miner, please cite:

```
Mess Miner
Author: Andre Moreira
November 2025
```

## To Dos

Mess Miner is currently a demo, not production-ready. Future improvement ideas:

**Production Hardening**

- Robust error handling
- Token usage monitoring and caps
- Sheet processing limits
- User-friendly interface

**Schema Reuse**

- Consolidate multiple sheets using the same structure
- Save and reuse examined schemas to skip Node 2 in future runs
- Store inferred schemas alongside cleaned tables

**Format Extensions**

- Support PowerPoint and Word files (yes, people store data there)

**Community Tool Vision**

- Django web application with containerized deployment
- Users bring their own LLM and API keys
- Self-hosted or cloud-based options

## Contributing

Contributions are welcome! Fork the repository, experiment with improvements, and submit pull requests for features, bug fixes, or documentation enhancements.

**Note on Maintenance**: This project is maintained on a best-effort basis. Pull requests are reviewed as time permits, so response times may vary. The codebase is open for you to adapt and extend for your own use cases.

## Support, Feedback

Reach out to a.moreira@lyfx.ai
