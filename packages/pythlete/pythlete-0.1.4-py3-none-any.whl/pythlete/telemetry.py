import matplotlib.pyplot as plt
import fastf1.plotting
import fastf1
import pandas as pd

fastf1.plotting.setup_mpl(misc_mpl_mods = False)

def circuit_info(session):
    '''
    Retrieves the circuit information for a given session.

    Parameters:
    session: dataframe
        the output from the load_session function
    '''
    # get the circuit information
    circuit_info = session.get_circuit_info()
    # get the corners
    corners = circuit_info.corners
    corners = corners[['Distance', 'Number']]

    return corners

def label_turn(distance, corners):
    '''
    Labels the turn for a given distance.

    Parameters:
    distance: float
        the distance of the car
    corners: dataframe
        the output from the circuit_info function

    Returns:
    turn: string
        a string describing the corner the distance is closest to
    '''
    # loop through the corners dataframe
    for idx, corner_distance in enumerate(corners['Distance']):
        # if the distance is within 100m of the corner distance approaching
        if abs(distance - corner_distance) <= 100:
            return f'Into Turn {corners["Number"].iloc[idx]}'
        # if the distance is within 100m of the corner distance leaving
        elif abs(distance - corner_distance) <= 100:
            return f'Out of Turn {corners["Number"].iloc[idx]}'
    # if the distance is not within 100m of any corner
    return f'Between Turns'

def pick_fastest_laps(driver, session):
    '''
    Picks the fastest laps for a given driver.

    Parameters:
    driver: string
        the driver that we are retrieving data for
    session: dataframe
        the output from the load_session function

    Returns:
    fastest_laps: pandas dataframe
        the fastest laps for the driver
    '''
    # pick the fastest lap
    fastest_lap = session.laps.pick_driver(driver).pick_fastest()

    # return fastest lap
    return fastest_lap

def add_distance_to_lap(fastest_lap):
    '''
    Adds distance to the fastest lap.

    Parameters:
    fastest_lap: dataframe
        the output from the pick_fastest_laps function

    Returns:
    fastest_lap: dataframe
        the fastest lap with distance added
    '''
    Driver = fastest_lap.Driver

    # add distance to the fastest lap
    fastest_lap = fastest_lap.get_car_data().add_distance()
    
    information = (fastest_lap, Driver)
    # return the information
    return information

def prepare_dataframe(info1, info2, session):
    '''
    Prepares the dataframe for plotting.

    Parameters:
    info1: tuple
        the output from the add_distance_to_lap function for the first driver
    info2: tuple
        the output from the add_distance_to_lap function for the second driver
    
    Returns:
    df: dataframe
        the prepared dataframe
    '''
    # unpack the tuples
    df1, driver1 = info1
    df2, driver2 = info2

    # subset columns
    df1 = df1[['RPM', 'Speed', 'Time', 'Distance']]
    df2 = df2[['RPM', 'Speed', 'Time', 'Distance']]

    # load circuit information
    corners = circuit_info(session)

    # Apply the labeling function to create new columns in telemetry dataframes
    df1['Turn_Label'] = df1['Distance'].apply(lambda x: label_turn(x, corners))
    df2['Turn_Label'] = df2['Distance'].apply(lambda x: label_turn(x, corners))

    # merge the two telemetry dataframes on the index
    tel = pd.merge(df1, df2, left_index=True, right_index=True, suffixes=('_' + driver1, '_' + driver2))

    # transform the Time columns to seconds
    tel['Time_' + driver1] = tel['Time_' + driver1].dt.total_seconds()
    tel['Time_' + driver2] = tel['Time_' + driver2].dt.total_seconds()   

    # round the distances to make calculations easier and more interpretable
    tel['Distance_' + driver1] = tel['Distance_' + driver1].round()
    tel['Distance_' + driver2] = tel['Distance_' + driver2].round()
    # add in the delta column
    tel['Delta'] = tel['Distance_' + driver1] - tel['Distance_' + driver2]
    
    return tel 

def find_loss(tel, driver):
    '''
    Takes a dataframe of telemetry data and returns a list of turns where the driver is losing time

    Parameters
    ----------
    tel : pandas.DataFrame
        A dataframe of telemetry data with columns 'Delta' and 'Turn_Label'
    driver : string
        The name of the first driver/the driver that we are interested in

    Returns
    -------
    list
        A list of turns where the driver is losing time
    '''
    # loop through the rows of the dataframe and if delta is less than the previous delta, append the Turn Label to a list
    # return the list of turns
    turns = []
    for idx, row in tel.iterrows():
        if idx == 0:
            continue
        if row['Delta'] < tel['Delta'].iloc[idx-1]:
            turns.append(row['Turn_Label_' + driver])

    # find the counts of all values in the turns and remove all those that have less than 5 counts
    turns = pd.Series(turns).value_counts()
    turns = turns[turns > 5]

    # print the turn labels to the driver as a message
    print(f'{driver}, we are losing time in {turns.index.values}')

def find_gain(tel, driver):
    '''
    Takes a dataframe of telemetry data and returns a list of turns where the driver is gaining time

    Parameters
    ----------
    tel : pandas.DataFrame
        A dataframe of telemetry data with columns 'Delta' and 'Turn_Label'
    driver : string
        The name of the first driver/the driver that we are interested in

    Returns
    -------
    list
        A list of turns where the driver is losing time
    '''
    # loop through the rows of the dataframe and if delta is more than the previous delta, append the Turn Label to a list
    # return the list of turns
    turns = []
    for idx, row in tel.iterrows():
        if idx == 0:
            continue
        if row['Delta'] > tel['Delta'].iloc[idx-1]:
            turns.append(row['Turn_Label_' + driver])

    # find the counts of all values in the turns and remove all those that have less than 4 counts
    turns = pd.Series(turns).value_counts()
    turns = turns[turns > 5]

    # print the turn labels to the driver as a message
    print(f'{driver}, we are gaining time in {turns.index.values}')

def plot_laps(info1, info2, team1, team2, session):
    '''
    Plots the laps for two drivers.

    Parameters:
    info1: tuple
        the output from the add_distance_to_lap function for the first driver
    info2: tuple
        the output from the add_distance_to_lap function for the second driver
    team1: string
        the team of the first driver
    team2: string
        the team of the second driver
    session: dataframe
        the output from the load_session function

    Returns:
    plot: plot
        the plot of the laps for the two drivers
    '''
    # unpack the tuples
    df1, driver1 = info1
    df2, driver2 = info2

    # get the team colors
    team1_color = fastf1.plotting.team_color(team1)
    team2_color = fastf1.plotting.team_color(team2)

    # plot the time against distance for each driver using the telemetry data
    fig, ax = plt.subplots()
    ax.plot(df1['Distance'], df1['Time'], color=team1_color, label=driver1, alpha=0.7)
    ax.plot(df2['Distance'], df2['Time'], color=team2_color, label=driver2, alpha = 0.7)

    ax.set_xlabel('Distance [m]')
    ax.set_ylabel('Time [s]')
    ax.legend()
    plt.suptitle(f'Fastest Lap comparison \n'
                f"{session.event.EventName} {session.event.year} Qualifying")
    plt.show()