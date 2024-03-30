import pandas as pd
import numpy as np
from odhpy import utils
from datetime import datetime, timedelta


"""_summary_
"""
def assert_df_has_one_column(df):
    n_cols = len(df.columns)
    if not n_cols == 1:
        raise Exception(f"The dataframe must have exactly 1 column, but {n_cols} found.") 


"""
WATERHOLES
This EFO is about avoiding periods with no (<=2ML/d) flow.
The EFO says the percentage of days in 'no flow periods' cannot increase above some given value.
And it defines 'no flow periods' as periods >60 days when the flow was <=2 ML/d.
Returns:
    _type_: _description_
"""
def days_in_no_flow_periods(df, lower_threshold=2, duration_threshold=60, as_percentage=True):
    assert_df_has_one_column(df)
    col = df.columns[0]
    duration_threshold_excl = duration_threshold + 1
    current_spell = 0
    total_days = 0
    for idx, value in df[col].items():
        if value <= lower_threshold:
            current_spell += 1
            if current_spell < duration_threshold_excl:
                pass
            elif current_spell == duration_threshold_excl:
                #current_spell just became long enough to count
                total_days += current_spell
            else:
                #long run is continuing
                total_days += 1 
        else:
            current_spell = 0
    ans = 100.0*total_days/len(df) if as_percentage else total_days
    return ans


"""
ECOLOGICAL LOW FLOW PERIODS
This EFO is about avoiding periods with low flow, in certain months.
The EFO says the percentage of days in 'ecological asset low flow periods' in certain months cannot increase above some given value.
And it defines 'ecological asset low flow periods' as periods longer than some duration_threshold, when the flow was less than some lower_threshold.
Returns:
    _type_: _description_
"""
def days_in_ecological_low_flow_periods(df, lower_threshold, duration_threshold, months=[1,2,3,4,5,6,7,8,9,10,11,12], as_percentage=True):
    assert_df_has_one_column(df)
    col = df.columns[0]
    duration_threshold_excl = duration_threshold + 1
    total_days = 0
    current_spell = 0
    current_season_days = 0
    for idx, value in df[col].items():
        month_int = int(idx[5:7])
        if month_int in months:
            current_season_days += 1
        else:
            current_season_days = 0
        if value > lower_threshold:
            current_spell = 0
        else:
            current_spell += 1
            if current_spell < duration_threshold_excl:
                pass 
            elif current_spell == duration_threshold_excl:
                #current_spell just became long enough to count
                total_days += min(current_spell, current_season_days)
            else:
                if current_season_days > 0:
                    #long run is continuing
                    total_days += 1
    ans = 100.0*total_days/len(df) if as_percentage else total_days
    return ans


"""
RIFFLE PERIODS
This EFO is about maintaining periods when flow is in a range beneficial to riffle habitat.
Not sure whether any specific seasons or durations apply. Assuming all days count.
Returns:
    _type_: _description_
"""
def days_in_riffle_periods(df, lower_threshold, upper_threshold, as_percentage=True):
    assert_df_has_one_column(df)
    col = df.columns[0]
    total_days = ((df[col] >= lower_threshold) & (df[col] <= upper_threshold)).sum()
    ans = 100.0*total_days/len(df) if as_percentage else total_days
    return ans


"""
RIVER FORMING PERIODS
This EFO is about maintaining a frequency of overbank flows necessary for river forming processes.
The EFO says that the percentage of days in 'river-forming flow periods' cannot drop below some given value.
And it defines 'river-forming flow periods' as periods when the the flow is higher than some threshold (notionally the bank-full flow rate).
Returns:
    _type_: _description_
"""
def days_in_river_forming_periods(df, lower_threshold, as_percentage=True):
    assert_df_has_one_column(df)
    col = df.columns[0]
    total_days = (df[col] > lower_threshold).sum()
    ans = 100.0*total_days/len(df) if as_percentage else total_days
    return ans


"""
RIPARIAN AND FLOODPLAIN VEGETATION
This EFO is about maintaining a frequency of floods for riparian and floodplain health.
Confusingly, the plan defines 'riparian and floodplain vegetation flow periods' by inadequate flow criteria
and then stating that the percentage of days in 'riparian and floodplain vegetation flow periods' must not be
higher than some (small) value.
The definition of 'riparian and floodplain vegetation flow periods' is periods longer than 1 year, when the 
flow was less than some lower_threshold.
Returns:
    _type_: _description_
"""
def days_in_riparian_flow_periods(df, lower_threshold, as_percentage=True):
    assert_df_has_one_column(df)
    col = df.columns[0]
    one_year = 366
    total_days = 0
    current_spell = 0
    for idx, value in df[col].items():
        # Now look at the current spell of low flows
        if value <= lower_threshold:
            current_spell += 1
            if current_spell < one_year:
                pass 
            elif current_spell == one_year:
                total_days += current_spell
            else:
                total_days += 1
        else:
            current_spell = 0
    ans = 100.0*total_days/len(df) if as_percentage else total_days
    return ans
