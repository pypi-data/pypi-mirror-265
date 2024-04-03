import logging
import time
import os

class PerformanceStats:
    def __init__(self):
        self.db_query_count = 0
        self.db_rows_fetched = 0
        self.file_read_count = 0
        self.file_write_count = 0
        self.bytes_read = 0
        self.bytes_written = 0
        self.execution_time = 0
    
    def update(self, file_path, start_time):
        self.file_read_count += 1
        self.bytes_read += os.path.getsize(file_path)
        self.execution_time += time.time() - start_time

    def log_stats(self):
        logging.info(f"Database queries: {self.db_query_count}, Rows fetched: {self.db_rows_fetched}")
        logging.info(f"Files read: {self.file_read_count}, Files written: {self.file_write_count}")
        logging.info(f"Bytes read: {self.bytes_read}, Bytes written: {self.bytes_written}")
        logging.info(f"Total execution time: {self.execution_time:.2f} seconds")
