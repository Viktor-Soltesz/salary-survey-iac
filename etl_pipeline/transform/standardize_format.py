import pandas as pd

def standardize_format(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes column names by converting to lowercase, replacing spaces with underscores, 
    and renaming specific columns.
    
    Also converts all string values in object-type columns to lowercase.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame to transform.
    
    Returns:
        pd.DataFrame: Transformed DataFrame.
    """
    
    # Convert all column names to lowercase
    df.columns = df.columns.str.lower()

    # Strip leading/trailing whitespaces from column names
    df.columns = df.columns.str.strip()
    
    # Replace spaces with underscores in column names
    df.columns = df.columns.str.replace(' ', '_', regex=False)

    # Rename specific columns based on mapping
    column_mappings = {
        'work_year': 'year',
        'experience_level': 'seniority_level',
        'employment_type': 'employment_status',
        'employee_residence': 'country',
        'salary': 'salary_eur',
        'salary_in_usd': 'salary'
    }
    df = df.rename(columns=column_mappings)

    # Convert all object-type (string) columns to lowercase
    str_columns = df.select_dtypes(include=['object']).columns
    for col in str_columns:
        df[col] = df[col].map(lambda x: x.lower() if isinstance(x, str) else x)

    return df
