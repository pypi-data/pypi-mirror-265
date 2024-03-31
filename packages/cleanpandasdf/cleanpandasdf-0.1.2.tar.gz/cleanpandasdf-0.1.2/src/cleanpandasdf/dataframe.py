import pandas as pd
import numpy as np

def optimize_memory(df):
    """
    Reduce memory usage of a pandas dataframe by downcasting numeric columns.
    """
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    return df

def clean_column_names(df):
    """
    Clean column names: make lowercase and replace spaces with underscores.
    """
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df

def clean(df):
    """
    Read a file, reduce its memory usage, and clean its column names.
    """
    # # Determine the file type
    # file_ext = file_path.split('.')[-1].lower()
    
    # # Read the file using pandas
    # if file_ext == 'csv':
    #     df = pd.read_csv(file_path)
    # elif file_ext == 'pkl':
    #     df = pd.read_pickle(file_path)
    # elif file_ext == 'xlsx':
    #     df = pd.read_excel(file_path)
    # else:
    #     raise ValueError("Unsupported file type")
    
    # Apply cleaning functions
    df = clean_column_names(df)
    df = optimize_memory(df)
    
    return df
