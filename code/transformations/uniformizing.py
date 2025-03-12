import pandas as pd

def uniformize_action_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Uniformizes the 'action' column by mapping various action names to a consistent set.

    Args:
        df: The input DataFrame.

    Returns:
        The DataFrame with the 'action' column uniformized.
    """
    if 'action' in df.columns:
        action_mapping = {
            'purchase': 'purchase',
            'buy': 'purchase',
            'add_to_cart': 'add_to_cart',
            'cart': 'add_to_cart',
            'view': "view",
            'view_product':'view'
        }
        df['action'] = df['action'].str.lower().map(action_mapping).fillna(df['action'])
    return df
