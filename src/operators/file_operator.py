import logging
import os
from typing import List

import pandas as pd


class FileOperator:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def read_csv(self, file_path, usecols=None):
        """
        Reads a CSV file and returns a DataFrame.
        :param file_path: Path to the CSV file.
        :param usecols: List of column names to read, optional.
        :return: DataFrame with the read data.
        """
        try:
            return pd.read_csv(file_path, usecols=usecols)
        except FileNotFoundError:
            self._logger.error(f"File not found: {file_path}")
        except Exception as e:
            self._logger.error(f"Error reading the CSV file at {file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

    def write_csv(self, df, file_path, index=False):
        """
        Writes a DataFrame to a CSV file.
        :param df: DataFrame to write.
        :param file_path: Path where the CSV should be written.
        :param index: Whether to write row names (index). Defaults to False.
        """
        try:
            df.to_csv(file_path, index=index)
            self._logger.info(f"Data successfully written to {file_path}")
        except Exception as e:
            self._logger.error(f"Failed to write to {file_path}: {e}")

    def read_all_csvs_in_folder(self, folder_path, usecols=None):
        """
        Reads all CSV files in the specified folder and combines them into a single DataFrame.
        Assumes all CSVs have the same structure.
        :param folder_path: Path to the folder containing CSV files.
        :param usecols: List of columns to read from each CSV, optional.
        :return: DataFrame containing all data from the CSV files.
        """
        all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".csv")]
        df_list = []

        for file in all_files:
            try:
                df = self.read_csv(file, usecols=usecols)
                if not df.empty:
                    df_list.append(df)
            except Exception as e:
                self._logger.error(f"Failed to process {file}: {e}")

        if df_list:
            return pd.concat(df_list, ignore_index=True)
        else:
            return pd.DataFrame()  # Return an empty DataFrame if no files were processed or if all reads failed

    def read_all_txts_in_folder(self, folder_path: str) -> List[str]:
        """
        Reads all text files in the specified folder and returns their contents as a list of strings.
        :param folder_path: Path to the folder containing text files.
        :return: List of strings, where each string represents the content of a text file.
        """
        all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
        file_contents = []

        for file in all_files:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()
                    file_contents.append(content)
            except FileNotFoundError:
                self._logger.error(f"File not found: {file}")
            except UnicodeDecodeError as e:
                self._logger.error(f"Error decoding the text file at {file}: {e}")
                # Try reading the file with a different encoding
                try:
                    with open(file, "r", encoding="latin-1") as f:
                        content = f.read()
                        file_contents.append(content)
                except Exception as e:
                    self._logger.error(f"Error reading the text file at {file}: {e}")
            except Exception as e:
                self._logger.error(f"Error reading the text file at {file}: {e}")

        return file_contents
