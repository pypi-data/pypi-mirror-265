import fastf1
import fastf1.plotting
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_laps(driver, session):
    '''
    Retrieves the laps for a given driver.

    Parameters:
    driver: string
        the driver that we are retrieving data for
    session: dataframe
        the output from the load_session function

    Returns:
    laps: pandas dataframe
        the laps for the driver
    '''
    # get laps for Hamilton and Leclerc
    laps = session.laps.pick_driver(driver).reset_index()

    return laps

def plot_lap_times(laps, session):
    '''
    Plots the lap times for a given driver.

    Parameters:
    laps: pandas dataframe
        the laps for the driver that is outputted by the get_laps function
    '''
    # set the background to be black so that tire colors are prominent
    sns.set_style("ticks", rc = {"axes.facecolor": "black", "figure.facecolor": "grey"})
    fig, ax = plt.subplots()
    # scatter plot of lap times
    sns.scatterplot(data = laps, x = "LapNumber", y = "LapTime",
                    ax = ax, hue = "Compound", palette = fastf1.plotting.COMPOUND_COLORS,
                    s = 80, linewidth = 0, legend = "auto")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    plt.suptitle(f"{laps.Driver[0]}'s Lap Times in the {session.event.EventName}")
    plt.grid(color = "w", which = 'major', axis = 'both')
    sns.despine(left = True, bottom = True)
    # get the plot's legend
    leg = ax.get_legend()
    # put the legend out of the plot
    leg.set_bbox_to_anchor((1.3, 1))
    # set the legend's background to transparent
    frame = leg.get_frame()
    frame.set_facecolor('none')
    plt.tight_layout()
    plt.show()

def prepare_dataframe(laps1, laps2):
    '''
    Prepares the dataframe for comparison.

    Parameters:
    laps1: pandas dataframe
        the laps for the first driver
    laps2: pandas dataframe
        the laps for the second driver

    Returns:
    combined_dataframe: pandas dataframe
        the combined dataframe
    '''
    # merge the two dataframes
    combined_dataframe = pd.merge(laps1, laps2, on="LapNumber", suffixes=("_" + laps1.Driver[0], "_" + laps2.Driver[0]))
    # Calculate the lap time difference between HAM and LEC
    combined_dataframe['LapTimeDifference'] = combined_dataframe['LapTime_HAM'] - combined_dataframe['LapTime_LEC']

    return combined_dataframe

def plot_lap_time_difference(combined_dataframe, laps1, laps2, session):
    '''
    Plots the lap time difference between two drivers.

    Parameters:
    combined_dataframe: pandas dataframe
        the combined dataframe that is outputted by the prepare_dataframe function
    laps1: pandas dataframe
        the laps for the first driver
    laps2: pandas dataframe
        the laps for the second driver
    session: dataframe
        the output from the load_session function
    '''
    # Plot lap time difference
    fig, ax_diff = plt.subplots()
    ax_diff.plot(laps1['LapNumber'], combined_dataframe['LapTimeDifference'], marker='o')
    ax_diff.axhline(y=0, color='gray', linestyle='--', linewidth=1, label='Equal Lap Time')

    ax_diff.set_xlabel("Lap Number")
    ax_diff.set_ylabel("Lap Time Difference (s)")
    plt.suptitle(f"Lap Time Difference between Hamilton and Leclerc {session.event.EventName}")
    plt.grid(color="w", which='major', axis='both')
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.show()

def when_to_pit(combined_dataframe, laps1, laps2):
    '''
    Identifies when to pit based on lap time difference.

    Parameters:
    combined_dataframe: pandas dataframe
        the combined dataframe that is outputted by the prepare_dataframe function
    laps1: pandas dataframe
        the laps for the first driver
    laps2: pandas dataframe
        the laps for the second driver

    Returns:
    pit_laps: tuple
        the pit laps for the two drivers
    '''
    # find the laps that Hamilton and Leclerc pitted
    pit_laps_1 = laps1[laps1['Pit'] == True].LapNumber.values
    pit_laps_2 = laps2[laps2['Pit'] == True].LapNumber.values

    # Identify when to pit based on lap time difference
    threshold_time_difference = 1  # Set your threshold for pitting
    pit_indices = combined_dataframe[combined_dataframe['LapTimeDifference'] > threshold_time_difference].LapNumber
    # remove pit laps from pit indices
    pit_indices = pit_indices[~pit_indices.isin(pit_laps_1)]
    pit_indices = pit_indices[~pit_indices.isin(pit_laps_2)]

    if not pit_indices.empty:
        print(f"Recommendation: Consider pitting on laps {pit_indices.values.tolist()} for a strategic advantage.")
    else:
        print("No clear advantage gained by pitting based on current lap time difference.")
    
    return (pit_laps_1, pit_laps_2)

def plot_both_drivers(laps1, laps2, session, team1, team2, pit_laps):
    '''
    Plots the lap times for two drivers.

    Parameters:
    laps1: pandas dataframe
        the laps for the first driver
    laps2: pandas dataframe
        the laps for the second driver
    session: dataframe
        the output from the load_session function
    team1: string
        the first team
    team2: string
        the second team
    pit_laps: tuple
        the pit laps for the two drivers outputted by the plot_lap_time_difference function
    '''
    # take the color of the two teams
    team1_color = fastf1.plotting.team_color(team1)
    team2_color = fastf1.plotting.team_color(team2)
    # Plot the first driver's lap times as a line plot with pit annotations
    fig, ax = plt.subplots()
    ax.plot(laps1['LapNumber'], laps1['LapTime'], marker='o', color=team1_color, label=laps1.Driver[0])
    ax.plot(laps2['LapNumber'], laps2['LapTime'], marker='o', color=team2_color, label=laps2.Driver[0])

    # unpack the pit laps
    pit_laps_1, pit_laps_2 = pit_laps

    # Annotate pit laps for driver 1
    for lap in pit_laps_1:
        ax.annotate('Pit', xy=(lap, laps1.loc[laps1['LapNumber'] == lap, 'LapTime'].values[0]),
                    xytext=(5, 5), textcoords='offset points', color='white', fontsize=8, ha='center')

    # Annotate pit laps for driver 2
    for lap in pit_laps_2:
        ax.annotate('Pit', xy=(lap, laps2.loc[laps2['LapNumber'] == lap, 'LapTime'].values[0]),
                    xytext=(5, -15), textcoords='offset points', color='white', fontsize=8, ha='center')

    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    plt.suptitle(f"Lap Times in the {session.event.EventName}")
    plt.grid(color="w", which='major', axis='both')
    sns.despine(left=True, bottom=True)
    plt.legend()
    plt.tight_layout()
    plt.show()