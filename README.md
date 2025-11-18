# MessMiner

An AI-powered agent workflow that mines and structures data from messy sources, transforming unstructured or poorly formatted data into clean, analyzable tables.

**Author:** Andre Moreira, November 2025
**Version:** 0.1.0-beta

## What is MessMiner?

MessMiner is an intelligent data cleaning tool that uses Large Language Models (LLMs) to understand and restructure messy data sources. Instead of manually writing complex parsing logic for each data format, MessMiner analyzes the structure of your data and intelligently extracts it into clean, structured tables.

### Key Features

- **Intelligent Structure Detection**: Uses LLMs to analyze and understand data organization
- **Parallel Processing**: Handles multiple sheets/data sources simultaneously using map-reduce patterns
- **Context-Aware**: Accepts user background information to guide the cleaning process
- **Flexible**: Works with various data formats and structures without custom parsing code
- **Observable**: Integration with LangSmith for workflow monitoring and debugging
- **Validated Output**: Uses Pydantic for structured response parsing and data validation

## Technology Stack

- **Python**: 3.11
- **LangGraph**: Agent orchestration and workflow management
- **LangSmith**: Observability and tracing
- **LLMs**: Google Gemini (2.5 Pro, 2.5 Flash)
- **Pydantic**: Structured response parsing and validation
- **Pandas**: Data manipulation
- **Development**: Claude Code for brainstorming and code assistance

## How It Works

MessMiner uses a three-node graph workflow:

```
START → Node 1 (Upload) → Node 2 (Examiner) → Node 3 (Extractor) → END
                              ↓ (parallel)         ↓ (parallel)
                           [Send pattern for multiple sheets]
```

### Workflow Nodes

1. **Node 1: Uploader**

   - Loads Excel files
   - Converts each sheet to CSV format (text)
   - Organizes data for processing

2. **Node 2: Examiner**

   - Analyzes CSV data structure
   - Identifies relevant columns and data organization
   - Creates field definitions (name, type, description)
   - Processes sheets in parallel using Send pattern

3. **Node 3: Extractor**
   - Dynamically builds Pydantic models based on examiner results
   - Extracts data according to identified structure
   - Cleans data (removes empty rows, validates types)
   - Generates clean pandas DataFrames
   - Processes sheets in parallel using Send pattern

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd Agents_capstone_Kaggle_2025
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

## Usage

### Basic Usage

1. Open `MessMiner.ipynb` in Jupyter
2. Configure your input file and user context:

```python
input_file = 'Example_0.xlsx'
output_file = 'Example_0_output.xlsx'

# Optional: Provide context to guide the cleaning
user_context = """The file contains agricultural data that is almost
correctly structured, but has empty rows. I need a clean, contiguous table."""
```

3. Run the workflow:

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

The repository includes three example files demonstrating different use cases:

- **Example_0.xlsx**: Agricultural data with empty rows
- **Example_1.xlsx**: Technical/price data in German
- **Example_2.xlsx**: Trial management software output

## State Management

### OverallState

Tracks the entire workflow state:

- `user_background`: Context information
- `file_name`: Input file path
- `sheets_as_csv`: Dictionary of sheet names to CSV strings
- `csv_structure`: List of identified structures (accumulated via operator.add)
- `cleaned_csv`: List of cleaned DataFrames (accumulated via operator.add)

### SingleCSVState

Used for parallel processing of individual sheets:

- `user_background`: Shared context
- `sheet_name`: Current sheet identifier
- `sheet_value`: CSV data as string
- `csv_structure`: Structure definition for this sheet

## Observability

LangSmith integration is enabled by default. View your workflow traces at:
https://eu.api.smith.langchain.com

Configure in the notebook:

```python
os.environ["LANGSMITH_ENDPOINT"] = "https://eu.api.smith.langchain.com"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "MessMiner_v2"
```

## Development

The notebook uses autoreload for easier development:

```python
%load_ext autoreload
%autoreload 2
```

This automatically reloads imported modules when they change, eliminating the need to restart the kernel during development.

## Next Steps (Roadmap)

- [ ] Support for additional file formats (CSV, JSON, etc.)
- [ ] Web interface for non-technical users
- [ ] Batch processing capabilities
- [ ] Custom validation rules
- [ ] Export to multiple formats (JSON, SQL, etc.)
- [ ] Performance optimization for large datasets
- [ ] Support for additional LLM providers

## License

[Add your license information here]

## Citation

If you use MessMiner in your research or projects, please cite:

```
MessMiner - AI-Powered Data Structure Mining
Author: Andre Moreira
Year: 2025
```

## Contributing

[Add contribution guidelines if applicable]

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your `.env` file contains valid API keys
2. **Model Timeout**: Try switching from Gemini Pro to Flash for faster processing
3. **Structure Detection Issues**: Provide more detailed context in `user_context`
4. **Empty Results**: Check LangSmith traces to debug workflow execution

## Support

[Add support contact information or issue tracker link]

---

Built with LangGraph and Claude Code
