import pandas as pd
import numpy as np

class DataPrepKit:
    """
    A class for data preprocessing tasks.
    """

    def __init__(self, file_path):
        """
        Initialize the DataPrepKit object with the file path.

        Parameters:
        - file_path (str): The path to the data file.
        """
        self.file_path = file_path
        self.read_data()  # Read data from file
    
    def read_data(self):
        """
        Read data from the specified file based on its format (CSV, Excel, or JSON).
        """
        if self.file_path.endswith('.csv'):
            self.data = pd.read_csv(self.file_path)  # Read data from CSV file
        elif self.file_path.endswith('.xlsx') or self.file_path.endswith('.xls'):
            self.data = pd.read_excel(self.file_path)  # Read data from Excel file
        elif self.file_path.endswith('.json'):
            self.data = pd.read_json(self.file_path)  # Read data from JSON file
        else:
            raise ValueError("Unsupported file format. Supported formats: CSV, Excel, JSON.")
    
    def data_summary(self):
        """
        Generate statistical summary of the data.

        Returns:
        - summary (DataFrame): Statistical summary of the data.
        """
        summary = self.data.describe()  # Generate statistical summary
        return summary
    
    def handle_missing_values(self, strategy='remove'):
        """
        Handle missing values in the data.

        Parameters:
        - strategy (str): The strategy for handling missing values. Options are 'remove' (default) or 'impute'.

        Returns:
        - data (DataFrame): Data after handling missing values.
        """
        if strategy == 'remove':
            self.data.dropna(inplace=True)  # Remove rows with missing values
        elif strategy == 'impute':
            # Impute missing values with mean, median, or mode
            self.data.fillna(self.data.mean(), inplace=True)
        return self.data
    
    def encode_categorical_data(self, columns=None):
        """
        Encode categorical data in the data.

        Parameters:
        - columns (list or None): List of columns to encode. If None, automatically detect categorical columns.

        Returns:
        - encoded_data (DataFrame): Data after encoding categorical columns.
        """
        if columns is None:
            # Detect categorical columns automatically
            categorical_columns = self.data.select_dtypes(include=['object']).columns
        else:
            categorical_columns = columns
        
        if len(categorical_columns) == 0:
            print("No categorical columns found.")
            return self.data
        
        encoded_data = pd.get_dummies(self.data, columns=categorical_columns)  # One-hot encoding
        return encoded_data

