# def label_encoding_all(data):
#     """
#     Apply label encoding to all columns containing categorical values in the dataset.

#     Parameters:
#     data (list of lists): Input dataset.

#     Returns:
#     list of lists: Transformed dataset after label encoding.
#     """
#     df = pd.DataFrame(data)
#     categorical_cols = df.select_dtypes(include=['object', 'category']).columns
#     if not categorical_cols.empty:
#         for col in categorical_cols:
#             df[col] = df[col].astype('category').cat.codes
#         return df.values.tolist()
#     return data

def label_encoding_selected(data, selected_columns):
    """
    Apply label encoding to selected columns containing categorical values in the dataset.

    Parameters:
    data (list of lists): Input dataset.
    selected_columns (list): List of column names to apply label encoding.

    Returns:
    list of lists: Transformed dataset after label encoding.
    """
    import pandas as pd

    df = pd.DataFrame(data)
    df_encoded = df.copy()
    
    for col in selected_columns:
        if col in df.columns and all(isinstance(value, str) for value in df[col]) and not any(value.isdigit() for value in df[col]):
            df_encoded[col] = df_encoded[col].astype('category').cat.codes
            
    return df_encoded.values.tolist()
