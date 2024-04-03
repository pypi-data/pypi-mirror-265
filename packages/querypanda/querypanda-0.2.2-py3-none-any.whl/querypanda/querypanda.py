from .performance_stats import PerformanceStats

import os
import glob
import time
import pandas as pd
import psycopg2
import psycopg2.extras
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict
import pickle

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

stats = PerformanceStats
# Flag to check if columns have been printed
columns_printed = False

def ensure_directory_exists(directory: str) -> None:
    """
    Ensure the specified directory exists. Create it if it does not.
    """
    if not os.path.exists(directory):
        logging.info(f"Creating directory: {directory}")
        os.makedirs(directory)

def fetch_data_from_db(conn_string: str, query: str) -> pd.DataFrame:
    """
    Fetch data from the database and return a pandas DataFrame.
    Also, prints the column names before fetching data, but only once.
    """
    global columns_printed  # Use the global flag

    try:
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(query)
                columns = [desc[0] for desc in cur.description]
                
                # Print column names only if they haven't been printed before
                if not columns_printed:
                    print("Columns:", columns)
                    columns_printed = True  # Update flag to indicate columns have been printed
                
                result = cur.fetchall()
                return pd.DataFrame(result, columns=columns)
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return pd.DataFrame()


def mark_period_start_in_checkpoint(start_time, save_location, complete):
    """
    Marks the start of a period processing in the checkpoint, indicating whether it's complete.
    """
    checkpoint_path = os.path.join(save_location, 'checkpoint.pkl')
    # Load existing checkpoint data if present
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path, 'rb') as file:
            checkpoint_data = pickle.load(file)
    else:
        checkpoint_data = {}

    checkpoint_data['last_processed'] = start_time
    checkpoint_data['complete'] = complete

    # Save updated checkpoint data
    with open(checkpoint_path, 'wb') as file:
        pickle.dump(checkpoint_data, file)

def save_data_with_checkpoint(df, filename, file_extension, start_time, end_time, save_location):
    """
    Enhanced to handle transactional data saving and marking periods as complete in the checkpoint.
    """
    # Attempt to save data, marking the start of the attempt in the checkpoint
    mark_period_start_in_checkpoint(start_time, save_location, complete=False)

    try:
        if file_extension == 'pkl':
            df.to_pickle(filename)
        elif file_extension == 'csv':
            df.to_csv(filename, index=False)
        elif file_extension in ['xls', 'xlsx']:
            df.to_excel(filename, index=False)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")

        logging.info(f"Data for period {start_time} to {end_time} successfully saved to {filename}.")
        
        # Mark the period as successfully completed in the checkpoint after saving
        mark_period_start_in_checkpoint(start_time, save_location, complete=True)
    except Exception as e:
        # Handle saving exceptions: log error, potentially delete the incomplete file here
        logging.error(f"Failed to save data for period {start_time} to {end_time}: {e}")

def get_last_processed_and_status(save_location: str):
    """
    Retrieves the last processed period and its completion status from the checkpoint.
    """
    checkpoint_path = os.path.join(save_location, 'checkpoint.pkl')
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path, 'rb') as file:
            checkpoint_data = pickle.load(file)
            last_processed = checkpoint_data.get('last_processed')
            complete = checkpoint_data.get('complete', False)
            return last_processed, complete
    return None, False

def check_for_checkpoint(save_location: str) -> datetime:
    """
    Check for an existing checkpoint and offer to continue or restart.
    """
    checkpoint_path = os.path.join(save_location, 'checkpoint.pkl')
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path, 'rb') as file:
            last_processed = pickle.load(file)
        return last_processed
    return None

def update_checkpoint(save_location: str, last_processed: datetime, complete: bool = True, stats: PerformanceStats = None):
    """
    Updates the checkpoint with the latest processed time and completion status, with added performance tracking.

    Parameters:
    - save_location (str): The directory where the checkpoint file is stored.
    - last_processed (datetime): The last datetime that was processed.
    - complete (bool): Whether the processing for the last period was completed successfully.
    - stats (PerformanceStats, optional): The performance statistics object to track execution metrics. If provided,
      the function's execution time will be tracked and logged.
    """
    start_time = time.time()  # Begin timing for performance tracking

    checkpoint_data = {'last_processed': last_processed, 'complete': complete}
    checkpoint_path = os.path.join(save_location, 'checkpoint.pkl')
    try:
        with open(checkpoint_path, 'wb') as file:
            pickle.dump(checkpoint_data, file)
    finally:
        if stats is not None:
            # Update execution time in stats only if stats object is provided
            operation_duration = time.time() - start_time
            stats.execution_time += operation_duration

            # Optionally, track file writes for checkpoint operations as well
            stats.file_write_count += 1
            stats.bytes_written += os.path.getsize(checkpoint_path)  # Track the size of the checkpoint file written

def clear_checkpoint(save_location: str):
    """
    Clear the checkpoint after successful completion or if the user decides to overwrite.
    """
    checkpoint_path = os.path.join(save_location, 'checkpoint.pkl')
    if os.path.exists(checkpoint_path):
        os.remove(checkpoint_path)

def clear_data_files(save_location: str, file_extension: str):
    """
    Deletes all files in the specified save location with the given file extension.

    Parameters:
    - save_location (str): The directory from which to delete files.
    - file_extension (str): The extension of files to delete (e.g., 'csv', 'pkl').
    """
    for file in glob.glob(os.path.join(save_location, f"*.{file_extension}")):
        try:
            os.remove(file)
            logging.info(f"Deleted existing file: {file}")
        except OSError as e:
            logging.error(f"Error deleting file {file}: {e}")

def find_latest_period(save_location: str, file_extension: str) -> datetime:
    """Finds the latest period for which data exists in the save_location."""
    files = glob.glob(os.path.join(save_location, f"*.{file_extension}"))
    latest_date = None
    for file in files:
        file_date_str = file.split('_')[-1].split('.')[0]
        file_date = datetime.strptime(file_date_str, "%Y_%m_%d")
        if not latest_date or file_date > latest_date:
            latest_date = file_date
    return latest_date

def generate_filename_based_on_aggregation(start_date: datetime, aggregation_frequency: str, save_location: str, file_extension: str) -> str:
    """
    Generates a filename based on the aggregation frequency and the start date of the data.
    """
    # Define the base name of the file
    base_filename = "data"

    # Generate the date part of the filename based on the aggregation frequency
    if aggregation_frequency == 'daily':
        date_part = start_date.strftime('%Y_%m_%d')
    elif aggregation_frequency == 'weekly':
        year, week, _ = start_date.isocalendar()
        date_part = f"{year}_week{week}"
    elif aggregation_frequency == 'monthly':
        date_part = start_date.strftime('%Y_%m')
    else:
        raise ValueError(f"Unsupported aggregation frequency: {aggregation_frequency}")

    # Assemble the full filename with the directory, base filename, date part, and file extension
    filename = f"{base_filename}_{date_part}.{file_extension}"
    full_path = os.path.join(save_location, filename)

    return full_path

def retrieve_dataset(conn_params: Dict[str, str], query_template: str, start_time: datetime, end_time: datetime, 
                     fetch_frequency: str = '1H', aggregation_frequency: str = 'daily', 
                     save_location: Optional[str] = None, file_extension: str = 'pkl') -> None:
    """
    Retrieves data in specified intervals and saves it, with options to manage existing data and resume after interruptions.

    Parameters:
    - conn_params: Dictionary with database connection parameters (user, password, host, database, sslmode).
    - query_template: SQL query string with placeholders for start and end times ('{start}' and '{end}').
    - start_time: The start datetime for data retrieval.
    - end_time: The end datetime for data retrieval.
    - fetch_frequency: Granularity for fetching data, e.g., '1H' for hourly. Determines the size of each fetch interval.
    - aggregation_frequency: How data files are grouped, e.g., 'daily'. Affects file naming and potentially data structure.
    - save_location: Directory path where data files will be saved. Defaults to 'data_output' if None.
    - file_extension: Format for saved data files ('pkl', 'csv', 'xlsx').

    The function checks for existing data and a checkpoint. If a checkpoint is found, it prompts the user to continue from
    the checkpoint, overwrite existing data, or exit. Data is fetched in intervals based on 'fetch_frequency' and saved
    according to 'aggregation_frequency', with each successful fetch updating the checkpoint.
    """

    # Set the default save location if not provided
    save_location = save_location or 'data_output'
    ensure_directory_exists(save_location)

    # Before data retrieval starts, check the checkpoint for the last processed period and its completion status
    last_processed, last_complete = get_last_processed_and_status(save_location)
    if last_processed:
        if not last_complete:
            logging.info(f"Redoing data retrieval for incomplete period starting at {last_processed}.")
            start_time = last_processed  # Adjust start_time to include the incomplete period
        else:
            logging.info(f"Resuming data retrieval from after the last completed period at {last_processed}.")
            start_time = max(start_time, last_processed + timedelta(seconds=1))
    
        # If the checkpoint exists, prompt the user for how to proceed
        user_choice = input(f"Data up to {last_processed} already processed. Continue (c), Restart (r), or Exit (e)? ").lower()
        if user_choice == 'c':
            # If continuing, adjust start_time to resume from the last processed point
            logging.info(f"Continuing data retrieval from {last_processed + timedelta(seconds=1)}.")
            start_time = max(start_time, last_processed + timedelta(seconds=1))
        elif user_choice == 'r':
            # If restarting, clear existing data files and checkpoint, then start from the beginning
            logging.info("Restarting data retrieval. Clearing existing data and starting afresh.")
            clear_data_files(save_location, file_extension)
            clear_checkpoint(save_location)
            # No adjustment needed to start_time, as we're restarting
            # Start from the original start_time as specified by the user
        elif user_choice == 'e':
            logging.info("Exiting as per user choice.")
            return
        else:
            logging.info("No existing data found or checkpoint. Starting new data retrieval.")


    # Setup database connection string
    conn_string = f"postgresql://{conn_params['user']}:{conn_params['password']}@{conn_params['host']}/{conn_params['database']}?sslmode={conn_params['sslmode']}"

    # Data retrieval and saving process
    time_ranges = pd.date_range(start=start_time, end=end_time, freq=fetch_frequency)
    for start in time_ranges:
        end = min(start + pd.Timedelta(fetch_frequency), end_time)  # Adjust the end to not exceed the overall end_time
        formatted_query = query_template.format(start=start.strftime('%Y-%m-%d %H:%M:%S'), end=end.strftime('%Y-%m-%d %H:%M:%S'))
        df = fetch_data_from_db(conn_string, formatted_query)

        if not df.empty:
            filename = generate_filename_based_on_aggregation(start, aggregation_frequency, save_location, file_extension)
            save_data_with_checkpoint(df, filename, file_extension, start, end, save_location)
            update_checkpoint(save_location, end)  # Update checkpoint after each successful save

    # After completing data retrieval and saving, clear the checkpoint
    update_checkpoint(save_location, end_time)
    logging.info(f"Data retrieval and processing up to {end_time} completed successfully.")


def read_file(file_path: str, stats: PerformanceStats) -> pd.DataFrame:
    """
    Reads a data file based on its extension and returns a pandas DataFrame,
    with performance tracking.
    """
    read_funcs = {
        '.pkl': pd.read_pickle,
        '.csv': pd.read_csv,
        '.xlsx': pd.read_excel,
        '.xls': pd.read_excel
    }

    _, file_extension = os.path.splitext(file_path)
    read_func = read_funcs.get(file_extension)

    if read_func:
        start_time = time.time()
        df = read_func(file_path)
        stats.update(file_path, start_time)
        return df
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


def load_dataset(path: str, stats: PerformanceStats) -> pd.DataFrame:
    """
    Loads data from a specified path into a pandas DataFrame with performance tracking.
    The path can be either a directory containing multiple data files or a path to a single data file.

    Supported formats for files: .pkl, .csv, .xlsx, .xls

    Parameters:
    - path (str): Path to the data file or folder containing data files.
    - stats (PerformanceStats): Performance stats object to track metrics.

    Returns:
    - pd.DataFrame: Data loaded into a DataFrame.

    Example Usage:
    - Loading from a single file:
      >>> load_dataset(file_path="data_output/data_file.csv")

    - Loading from a directory:
      >>> load_dataset(folder_path="data_output")
    """
    if os.path.isdir(path):
        all_files = glob.glob(os.path.join(path, "*"))
    elif os.path.isfile(path):
        all_files = [path]
    else:
        raise ValueError(f"The path provided does not exist: {path}")

    # Define files or patterns to skip
    files_to_skip = ["checkpoint.pkl"]
    
    data_frames = []
    for f in all_files:
        if any(skip_file in f for skip_file in files_to_skip):
            print(f"Skipping file {f} based on skip criteria.")
            continue
        try:
            df = read_file(f, stats)
            if isinstance(df, pd.DataFrame):  # Check if df is a DataFrame
                data_frames.append(df)
            else:
                print(f"Skipping: {f} did not return a DataFrame.")
        except ValueError as e:
            print(f"Skipping unsupported file type in {f}: {e}")
        except Exception as e:
            print(f"Error reading file {f}: {e}")

    if data_frames:
        return pd.concat(data_frames, ignore_index=True)
    else:
        return pd.DataFrame()