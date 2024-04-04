import pandas as pd


def drop_null_values_from_selected_columns(input_data, selected_columns, column_names):
    """
    Drops null values from selected columns in a DataFrame.

    Parameters:
        input_data (list of lists): The input data as a list of lists.
        selected_columns (list): A list of column names from which null values will be dropped.
        column_names (list): A list of all column names in the DataFrame.

    Returns:
        list of lists: The output data with null values dropped from selected columns.
    """
    try:
        # Convert input data to a DataFrame
        df = pd.DataFrame(input_data, columns=column_names)
        
        # Convert selected column names to indices
        selected_column_indices = [df.columns.get_loc(col) for col in selected_columns]
        
        # Drop null values from selected columns
        df.dropna(subset=selected_columns, inplace=True)
        
        # Convert DataFrame back to a list of lists
        output_data = df.values.tolist()
        
        return output_data
    except Exception as e:
        # Handle any errors that might occur
        print(f"An error occurred: {str(e)}")
        return None