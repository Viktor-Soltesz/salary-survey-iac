"""
Test the out_of_scope function from the transform module.
"""

import pandas as pd
from etl_pipeline.transform.out_of_scope import out_of_scope

def test_out_of_scope_filters_only_full_time():
    """ Test that the out_of_scope function filters out non-full-time employees. """
    df_dirty = pd.DataFrame({
        'employment_status': ['ft', 'pt', 'contractor', 'intern', 'ft'],
        'job_title': ['Data Analyst'] * 5
    })

    df_filtered = out_of_scope(df_dirty)

    # Only rows with 'ft' (exact lowercase match) should remain
    assert df_filtered.shape[0] == 2
    assert all(df_filtered['employment_status'] == 'ft')
