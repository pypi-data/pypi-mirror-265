import pandas as pd

# def one_hot_encoding_all(data):
#     """
#     Apply one-hot encoding to all columns containing categorical values in the dataset.

#     Parameters:
#     data (list of lists): Input dataset.

#     Returns:
#     list of lists: Transformed dataset after one-hot encoding.
#     """
#     df = pd.DataFrame(data)
#     categorical_cols = df.select_dtypes(include=['object', 'category']).columns
#     if not categorical_cols.empty:
#         df_encoded = pd.get_dummies(df, columns=categorical_cols)
#         return df_encoded.values.tolist()
#     return data



def one_hot_encoding_selected(data, selected_columns):
    """
    Apply one-hot encoding to selected columns containing categorical values in the dataset.

    Parameters:
    data (list of lists): Input dataset.
    selected_columns (list): List of column names to apply one-hot encoding.

    Returns:
    list of lists: Transformed dataset after one-hot encoding.
    """
    import pandas as pd

    df = pd.DataFrame(data)
    df_encoded = df.copy()

    for col in selected_columns:
        if col in df.columns and all(isinstance(value, str) for value in df[col]) and not any(value.isdigit() for value in df[col]):
            df_encoded = pd.get_dummies(df_encoded, columns=[col])

    return df_encoded.values.tolist()
