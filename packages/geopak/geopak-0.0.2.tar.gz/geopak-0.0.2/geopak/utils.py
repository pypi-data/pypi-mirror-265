"""This is the utils module that contains utility functions for the geopak package"""


def csv_to_df(csv_file):
    """Converts a CSV file  to a pandas Dataframe

    Args:
        csv_file (_type_): The path to the csv file.


    References:
        pandas.dataFrame: The pandas DataFrame
    """

    import pandas as pd

    return pd.read_csv(csv_file)

