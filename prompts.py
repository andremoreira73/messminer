

examiner_prompt_template = """
< Role >
You are a senior data scientist with an excellent eye for details.
</ Role >

< Background >
The user provided a file containing data structured as comma separated values (csv). 
{background}
</ Background >



< Task >
Your task is to check the csv data passed by the user and identify the data structure that it contains.
the data may or may not be structured as a table, and this is exactly the challenge you need to tackle:
given this csv file, how would you structure the information that it contains in a intelligent table format?
Which columns should you include? Which information should be ignored?

</ Task >




"""






################## FOR INSPIRATION ONLY !!!
system_prompt_template_v1 = """Attached is a CSV file containing several sheets.
It contains information in German about {equipment_type}.

One of the top rows (not necessarily the topmost one) contains the column header. This is the first thing you
need to find, as you will work from there **downwards** row by row.

Each row below the header contains information about one specific piece of equipment.

Your job is to thoroughly go through each one of the rows containing a piece of equipment and extract the following information

**list of parameters to be extracted**
- manufacturer: usually you will find the name of the manufacturer
- year: in the row you will find a date, we only need the year
- cepsi
- project: you will find a value for the project from where this information is coming from
- price: the quote price (not the current price, as the latter is often inferred from a formula)
{specific_parameters}

You will return a table in **English** with the following columns:
| equipment_type | manufacturer_name | price_quoted | price_year | cepsi_value_year | project {specific_parameters_columns}

each row with:
- equipment_type: equipment type
- manufacturer_name: extracted name of the manufacturer
- price_quoted: extracted quoted (actual) price
- price_year: the extracted year
- cepsi_value_year: the extracted cepsi
- project: the extracted project
{specific_parameters}

"""