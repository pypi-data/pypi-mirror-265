import numpy as np
import pandas as pd


def nan_treatment(df: pd.DataFrame, method: str = 'ffill') -> pd.DataFrame:
    """
    NaN treatment for dataframes. Values must be in different columns

    Args:
        df: dataframe in wide format
        method: 'interpolate', 'bfill', 'ffill', 'mean', 'zerofill'

    Returns:
        df
    """
    # Cambiar formato de long a wide para correcto análisis por columnas and set timestamp as index
    df = df.pivot_table(index='timeStamp', columns='uid', values='value', aggfunc='last', dropna=False)
    numeric_cols = df.select_dtypes(include=np.number).columns

    switch = {
        'interpolate': df[numeric_cols].interpolate(),
        'bfill': df[numeric_cols].bfill(),
        'ffill': df[numeric_cols].ffill(),
        'mean': df[numeric_cols].fillna(value=df.mean()),
        'zerofill': df[numeric_cols].fillna(value=0.0)
    }
    try:
        df[numeric_cols] = switch[method]
        df.reset_index(inplace=True)
        df = df.melt(id_vars=['timeStamp'], var_name='uid', value_name='value')
        return df
    except KeyError:
        raise ValueError("Invalid method. Please use 'interpolate', 'bfill', 'ffill', 'mean', or 'zerofill'.")
