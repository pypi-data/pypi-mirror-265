import numpy as np
import pandas as pd

def winsorize_data(data, selected_columns, lower_pct=5, upper_pct=95):
    """
    Apply Winsorization to selected columns of the dataset.

    Parameters:
        data (list of lists): The input data where each inner list represents a row of data.
        selected_columns (list of str): The names of columns to which Winsorization should be applied.
        lower_pct (float): The lower percentile threshold (default is 5).
        upper_pct (float): The upper percentile threshold (default is 95).

    Returns:
        list of lists: The data with Winsorization applied to selected columns.
    """
    # Create a copy of the data to avoid modifying the original data
    winsorized_data = [row[:] for row in data]

    # Iterate over each column
    for col_idx, col_name in enumerate(data[0]):
        if col_name in selected_columns:
            # Extract values of the column
            col_values = [row[col_idx] for row in winsorized_data[1:]]  # Skip the header

            # Check if the column contains numeric data
            if all(isinstance(val, (int, float)) for val in col_values):
                # Calculate percentile values
                lower_value = np.percentile(col_values, lower_pct)
                upper_value = np.percentile(col_values, upper_pct)
                
                # Print percentiles
                print(f"Lower percentile for column {col_name}: {lower_value}")
                print(f"Upper percentile for column {col_name}: {upper_value}")

                # Apply Winsorization
                for row_idx, value in enumerate(col_values):
                    if value < lower_value:
                        winsorized_data[row_idx + 1][col_idx] = lower_value
                    elif value > upper_value:
                        winsorized_data[row_idx + 1][col_idx] = upper_value
            else:
                # If the column contains non-numeric data, retain the data as it is
                pass

    return winsorized_data