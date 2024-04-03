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


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_directory_exists(directory: str) -> None:
    """
    Ensure the specified directory exists. Create it if it does not.
    """
    if not os.path.exists(directory):
        logging.info(f"Creating directory: {directory}")
        os.makedirs(directory)

def fetch_data_from_db(conn_string: str, query: str, stats: PerformanceStats) -> pd.DataFrame:
    """
    Fetch data from the database and return a pandas DataFrame. This function also updates 
    performance statistics including the number of database queries made, the total number of rows fetched,
    and the execution time for fetching the data.

    Parameters:
    - conn_string (str): The connection string for the database.
    - query (str): The SQL query to execute.
    - stats (PerformanceStats): An instance of PerformanceStats to track performance metrics.

    Returns:
    - pd.DataFrame: The fetched data as a pandas DataFrame.
    """
    start_time = time.time()  # Begin timing for this operation
    try:
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(query)
                stats.db_query_count += 1  # Increment database query count
                result = cur.fetchall()
                stats.db_rows_fetched += len(result)  # Update rows fetched
                columns = [desc[0] for desc in cur.description]
                return pd.DataFrame(result, columns=columns)
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return pd.DataFrame()
    finally:
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        stats.execution_time += elapsed_time  # Update execution time in stats

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

def save_data_with_checkpoint(df, filename, file_extension, start_time, end_time, save_location, stats: PerformanceStats):
    """
    Enhanced to handle transactional data saving and marking periods as complete in the checkpoint,
    with added performance statistics tracking for execution time and file I/O operations.
    
    Parameters:
    - df (pd.DataFrame): The DataFrame to save.
    - filename (str): The base name for the file to save the DataFrame to.
    - file_extension (str): The file extension indicating the format to save the DataFrame as.
    - start_time, end_time (datetime): The start and end time for the data period being saved.
    - save_location (str): The directory path where the data file will be saved.
    - stats (PerformanceStats): An instance of PerformanceStats to track performance metrics.
    """
    full_path = os.path.join(save_location, filename + '.' + file_extension)
    operation_start_time = time.time()  # Start timing the entire operation

    # Attempt to save data, marking the start of the attempt in the checkpoint
    mark_period_start_in_checkpoint(start_time, save_location, complete=False)

    try:
        # Save the data based on the specified file extension
        if file_extension == 'pkl':
            df.to_pickle(full_path)
        elif file_extension == 'csv':
            df.to_csv(full_path, index=False)
        elif file_extension in ['xls', 'xlsx']:
            df.to_excel(full_path, index=False)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")
        
        stats.file_write_count += 1
        stats.bytes_written += os.path.getsize(full_path)  # Accurate bytes written

        logging.info(f"Data for period {start_time} to {end_time} successfully saved to {full_path}.")

        # Mark the period as successfully completed in the checkpoint after saving
        mark_period_start_in_checkpoint(start_time, save_location, complete=True)
    except Exception as e:
        logging.error(f"Failed to save data for period {start_time} to {end_time}: {e}")
    finally:
        operation_duration = time.time() - operation_start_time
        stats.execution_time += operation_duration  # Update execution time in stats
        logging.info(f"save_data_with_checkpoint execution time: {operation_duration:.2f} seconds.")

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

    Parameters:
    - start_date: The start datetime of the data interval being processed.
    - aggregation_frequency: The frequency of data aggregation ('daily', 'weekly', 'monthly').
    - save_location: The directory path where data files will be saved.
    - file_extension: The file extension to use for the data file ('pkl', 'csv', 'xlsx').

    Returns:
    - The full path to the data file with the generated filename.
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

def retrieve_dataset(conn_params: Dict[str, str], 
                     query_template: str, 
                     start_time: datetime, end_time: datetime,
                     stats: PerformanceStats,
                     fetch_frequency: str = '1H',
                     save_location: Optional[str] = None, 
                     file_extension: Optional[str] = None,
                     aggregation_frequency: Optional[str] = None) -> pd.DataFrame:
    """
    Retrieves data in specified intervals and optionally saves it. If saving parameters are provided,
    it saves the data in the specified format at the given location. If not, it returns the data as a DataFrame.
    Tracks and logs performance statistics and manages checkpoints.

    Parameters:
    - conn_params: Database connection parameters.
    - query_template: SQL query string with placeholders for start and end times.
    - start_time, end_time: Start and end datetime for data retrieval.
    - fetch_frequency: Granularity for fetching data, e.g., '1H'.
    - stats: An instance of PerformanceStats for tracking performance metrics.
    - save_location: Optional directory path where data files will be saved. If omitted, data is returned as a DataFrame.
    - file_extension: Format for saved data files. Defaults to 'pkl' when saving.
    - aggregation_frequency: How data files are grouped, e.g., 'daily'.

    Returns:
    - A pandas DataFrame of the retrieved data when not saving to files.
    """
    stats = PerformanceStats()  # Initialize performance stats tracking
    combined_data = pd.DataFrame()  # Initialize DataFrame for direct return
    save_required = save_location is not None and file_extension is not None

    # Set default save location and file extension if saving is required but not specified
    if save_required:
        save_location = save_location or 'data_output'
        file_extension = file_extension or 'pkl'
        ensure_directory_exists(save_location)
    
    # Handle checkpoint and existing data
    if save_location:
        last_processed, last_complete = get_last_processed_and_status(save_location)
        # Logic to handle user choice based on checkpoint status

    conn_string = f"postgresql://{conn_params['user']}:{conn_params['password']}@{conn_params['host']}/{conn_params['database']}?sslmode={conn_params['sslmode']}"

    # Data retrieval and processing
    time_ranges = pd.date_range(start=start_time, end=end_time, freq=fetch_frequency)
    for start in time_ranges:
        end = min(start + pd.Timedelta(fetch_frequency), end_time)
        formatted_query = query_template.format(start=start.strftime('%Y-%m-%d %H:%M:%S'), end=end.strftime('%Y-%m-%d %H:%M:%S'))
        df = fetch_data_from_db(conn_string, formatted_query, stats)

        if not df.empty:
            if save_required:
                filename = generate_filename_based_on_aggregation(start, aggregation_frequency, save_location, file_extension)
                save_data_with_checkpoint(df, filename, file_extension, start, end, save_location, stats)
            else:
                combined_data = pd.concat([combined_data, df], ignore_index=True)
    
    # Finalize performance stats and checkpoint updates
    if save_required:
        update_checkpoint(save_location, end_time, True, stats)
    
    stats.log_stats()

    # Return combined DataFrame if not saving to files
    return combined_data if not save_required else None


def read_file(file_path: str, stats: PerformanceStats = None) -> pd.DataFrame:
    """
    Reads a data file based on its extension and returns a pandas DataFrame, with performance tracking.

    Supported formats: .pkl, .csv, .xlsx, .xls

    Parameters:
    - file_path (str): Path to the data file.
    - stats (PerformanceStats, optional): The performance statistics object to track execution metrics. 
      If provided, the function's execution time and file I/O metrics will be tracked and updated.

    Returns:
    - pd.DataFrame: Data loaded into a DataFrame.
    """
    start_time = time.time()  # Begin timing for performance tracking
    
    try:
        _, file_extension = os.path.splitext(file_path)
        if file_extension == '.pkl':
            df = pd.read_pickle(file_path)
        elif file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        if stats is not None:
            # Update stats for file read operation
            stats.file_read_count += 1
            stats.bytes_read += os.path.getsize(file_path)  # Track the size of the file read

        return df
    finally:
        if stats is not None:
            # Update execution time in stats
            operation_duration = time.time() - start_time
            stats.execution_time += operation_duration

def load_dataset(path: str, stats: PerformanceStats = None) -> pd.DataFrame:
    """
    Loads data from a specified path into a pandas DataFrame, with performance tracking.
    The path can be either a directory containing multiple data files or a path to a single data file.

    Supported formats for files: .pkl, .csv, .xlsx, .xls

    Parameters:
    - path (str): Path to the data file or folder containing data files.
    - stats (PerformanceStats, optional): The performance statistics object to track execution metrics. 
      If provided, the function's execution time, number of files read, and data processed will be tracked.

    Returns:
    - pd.DataFrame: Data loaded into a DataFrame.

    Example Usage:
    - Loading from a single file:
      >>> load_data(file_path="data_output/data_file.csv", stats=my_stats)

    - Loading from a directory:
      >>> load_data(folder_path="data_output", stats=my_stats)
    """
    operation_start_time = time.time()  # Begin timing for the entire loading operation
    data_frames = []

    if os.path.isdir(path):
        all_files = glob.glob(os.path.join(path, "*"))
    elif os.path.isfile(path):
        all_files = [path]
    else:
        raise ValueError(f"The path provided does not exist: {path}")

    for filename in all_files:
        try:
            df = read_file(filename, stats)  # Pass the PerformanceStats object
            data_frames.append(df)
        except ValueError as e:
            print(f"Skipping unsupported file type in {filename}: {e}")

    loaded_data = pd.concat(data_frames, ignore_index=True) if data_frames else pd.DataFrame()
    
    if stats is not None:
        # Update execution time in stats for the entire load_dataset operation
        operation_duration = time.time() - operation_start_time
        stats.execution_time += operation_duration
    
    return loaded_data