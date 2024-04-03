# Query2Dataframe Project

![Query2DataFrame Logo](<images/logo.webp>)

## Overview

This project provides a toolkit for retrieving, saving, and loading datasets from a PostgreSQL database, aimed at simplifying data handling and preprocessing tasks for data analysis and machine learning projects. It includes functionality to ensure robust data retrieval processes, including handling checkpoints for long-running data retrieval tasks and saving data in various formats.

## Features

- Retrieve data from a PostgreSQL database with customizable query templates.
- Save retrieved data in different formats (CSV, PKL, Excel) with checkpointing to manage long-running tasks.
- Load datasets from saved files into pandas DataFrames, supporting various file formats.
- Modular design for easy integration into data processing pipelines.

## Installation

To use this project, you need to have Python installed on your machine. It is recommended to use Python 3.8 or higher.

1. **Clone the repository:**

```   sh
      git clone (https://github.com/Shazankk/Query2DataFrame)
      cd Query2DataFrame
```

Install required libraries:
Ensure you have pip installed and then run:

```   sh
      pip install -r requirements.txt
```

Configure database connection:
Modify the [config.json](config.json) file with your PostgreSQL database connection details:

``` JSON
{
  "database": {
    "user": "your_username",
    "password": "your_password",
    "host": "database_host",
    "database": "your_database",
    "sslmode": "require"
  }
}
```

Update the placeholders with your actual database connection details.

## Usage

### Example Usage Script

See [example_usage.py](example_usage.py) for a detailed example on how to use the toolkit. This script demonstrates:

- Loading database connection configurations from `config.json`.
- Constructing a SQL query with placeholders for date ranges.
- Retrieving and saving datasets for specified time periods.
- Loading datasets from saved files.

### Data Retrieval and Saving

You can customize data retrieval by modifying the SQL query template, specifying start and end times, and choosing your data saving and aggregation preferences.

### Loading Datasets

Use the load_dataset function to load data from saved files into pandas DataFrames. This function supports loading from both individual files and directories containing multiple data files.

## Contributing

Contributions to the project are welcome. Please follow the standard fork and pull request workflow.

## License

This project is open-sourced under the MIT License. See the LICENSE file for more details.
