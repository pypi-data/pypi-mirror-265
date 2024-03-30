import fastf1
import pandas as pd
import numpy as np

def load_session(year, race, session):
    '''
    Loads the session data for a given race.

    Parameters:
    year: int
        the year of the race
    race: string
        the exact race that we are retrieving data for
    session: string
        the session that we are retrieving data for such as FP1, FP2, FP3, Q, R

    Returns:
    session_data: pandas dataframe
        the session data
    '''
    # load the session
    session = fastf1.get_session(year, race, session)
    session.load()
    
    # return session
    return session

def data_pre_processing(df):
    '''
    This function takes in a dataframe and converts the time columns to seconds, replace nan values, and adds a new columns

    Parameters:
    df (dataframe): dataframe to be processed

    Returns:
    df (dataframe): processed dataframe
    '''
    # convert the time columns to seconds
    convert_to_seconds = lambda x: x.total_seconds() if pd.Timedelta == type(x) else x
    df = df.applymap(convert_to_seconds)
    # replace nan values with None
    df.replace({np.nan: None}, inplace=True)
    # set a new column "Pit" to True if the PitOutTime is not null or PitInTime is not null
    df['Pit'] = df['PitOutTime'].notnull() | df['PitInTime'].notnull()
    return df