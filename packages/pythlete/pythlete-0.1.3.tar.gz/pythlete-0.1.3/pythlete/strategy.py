import fastf1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import fastf1.plotting
import scipy.stats as sts
from pythlete.general import data_pre_processing

def load_practices(year, race):
    '''
    Loads the practice session data for the weekend
    '''
    # define the sessions
    practice_1 = fastf1.get_session(year, race, 'FP1')
    practice_2 = fastf1.get_session(year, race, 'FP2')
    practice_3 = fastf1.get_session(year, race, 'FP3')
    # load the sessions
    practice_1.load()
    practice_2.load()
    practice_3.load()

    return (practice_1, practice_2, practice_3)

def subset_columns(practices):
    '''
    This function takes in a dataframe and returns a subset of the dataframe

    Parameters:
    practices (tuple): dataframes to be processed

    Returns:
    practices (tuple): subset of the dataframes
    '''
    # unpack the practice sessions
    practice_1, practice_2, practice_3 = practices
    practice_1 =  practice_1[['Driver', 'DriverNumber', 'LapTime', 'LapNumber', 'Stint',
               'PitOutTime', 'PitInTime', 'Sector1Time', 'Sector2Time', 'Sector3Time',
               'IsPersonalBest', 'Compound', 'TyreLife', 'Team', 'Deleted', 'Pit']]
    practice_2 =  practice_2[['Driver', 'DriverNumber', 'LapTime', 'LapNumber', 'Stint',
                'PitOutTime', 'PitInTime', 'Sector1Time', 'Sector2Time', 'Sector3Time',
                'IsPersonalBest', 'Compound', 'TyreLife', 'Team', 'Deleted', 'Pit']]
    practice_3 =  practice_3[['Driver', 'DriverNumber', 'LapTime', 'LapNumber', 'Stint',
                'PitOutTime', 'PitInTime', 'Sector1Time', 'Sector2Time', 'Sector3Time',
                'IsPersonalBest', 'Compound', 'TyreLife', 'Team', 'Deleted', 'Pit']]
    return (practice_1, practice_2, practice_3)

def process_practice_data(driver, practices):
    '''
    This function processes the practice data for a given driver

    Parameters:
    driver (string): the driver of interest
    practices (tuple): the practice sessions

    Returns:
    driver_practice_hard (dataframe): the driver's lap times on hard compound
    driver_practice_medium (dataframe): the driver's lap times on medium compound
    driver_practice_soft (dataframe): the driver's lap times on soft compound
    '''

    # unpack the practice sessions
    practice_1, practice_2, practice_3 = practices

    # retrieve the data for hamilton
    driver_fp1 = practice_1.laps.pick_driver(driver)
    driver_fp2 = practice_2.laps.pick_driver(driver)
    driver_fp3 = practice_3.laps.pick_driver(driver)
    # process the data
    driver_fp1 = data_pre_processing(driver_fp1)
    driver_fp2 = data_pre_processing(driver_fp2)
    driver_fp3 = data_pre_processing(driver_fp3)
    # subset the columns
    driver_fp1, driver_fp2, driver_fp3 = subset_columns((driver_fp1, driver_fp2, driver_fp3))    
    # remove pit laps
    driver_fp1 = driver_fp1[driver_fp1['Pit'] == False]
    driver_fp2 = driver_fp2[driver_fp2['Pit'] == False]
    driver_fp3 = driver_fp3[driver_fp3['Pit'] == False]
    # pick the quick laps
    driver_fp1 = driver_fp1.pick_quicklaps()
    driver_fp2 = driver_fp2.pick_quicklaps()
    driver_fp3 = driver_fp3.pick_quicklaps()

    # group the laps by compound for each practice session
    driver_fp1_hard = driver_fp1[driver_fp1['Compound'] == 'HARD']
    driver_fp1_medium = driver_fp1[driver_fp1['Compound'] == 'MEDIUM']
    driver_fp1_soft = driver_fp1[driver_fp1['Compound'] == 'SOFT']

    driver_fp2_hard = driver_fp2[driver_fp2['Compound'] == 'HARD']
    driver_fp2_medium = driver_fp2[driver_fp2['Compound'] == 'MEDIUM']
    driver_fp2_soft = driver_fp2[driver_fp2['Compound'] == 'SOFT']

    driver_fp3_hard = driver_fp3[driver_fp3['Compound'] == 'HARD']
    driver_fp3_medium = driver_fp3[driver_fp3['Compound'] == 'MEDIUM']
    driver_fp3_soft = driver_fp3[driver_fp3['Compound'] == 'SOFT']

    # Concatenate all the practice sessions
    driver_practice_hard = pd.concat([driver_fp1_hard, driver_fp2_hard, driver_fp3_hard])
    driver_practice_medium = pd.concat([driver_fp1_medium, driver_fp2_medium, driver_fp3_medium])
    driver_practice_soft = pd.concat([driver_fp1_soft, driver_fp2_soft, driver_fp3_soft])

    return (driver_practice_hard, driver_practice_medium, driver_practice_soft)

def practice_data_distributions(practices):
    '''
    This function calculates the distributions for a driver's lap times on each compound

    Parameters:
    practices (tuple): the practice sessions

    Returns:
    driver_hard_dist (scipy.stats.rv_frozen): the distribution of the driver's lap times on hard compound
    driver_medium_dist (scipy.stats.rv_frozen): the distribution of the driver's lap times on medium compound
    driver_soft_dist (scipy.stats.rv_frozen): the distribution of the driver's lap times on soft compound
    '''
    # unpack the practice sessions
    hard, medium, soft = practices
    # find the means on each compound
    driver_mean_hard = hard['LapTime'].mean()
    driver_mean_medium = medium['LapTime'].mean()
    driver_mean_soft = soft['LapTime'].mean()
    # find the standard deviations on each compound
    driver_std_hard = hard['LapTime'].std()
    driver_std_medium = medium['LapTime'].std()
    driver_std_soft = soft['LapTime'].std()

    # define distributions for each compound
    driver_hard_dist = sts.halfnorm(driver_mean_hard, driver_std_hard)
    driver_medium_dist = sts.halfnorm(driver_mean_medium, driver_std_medium)
    driver_soft_dist = sts.halfnorm(driver_mean_soft, driver_std_soft)

    return (driver_hard_dist, driver_medium_dist, driver_soft_dist)

def plot_practice_distributions(practices, distributions):
    '''
    This function plots the distributions of a driver's lap times on each compound

    Parameters:
    distributions (tuple): the distributions of the driver's lap times on each compound
    practices (tuple): the practice sessions
    '''
    # unpack the distributions
    driver_hard_dist, driver_medium_dist, driver_soft_dist = distributions
    # unpack the practice sessions
    hard, medium, soft = practices
    # find the smallest time over all the practice sessions
    min_time = min(hard['LapTime'].min(), medium['LapTime'].min(), soft['LapTime'].min())
    # find the largest time over all the practice sessions
    max_time = max(hard['LapTime'].max(), medium['LapTime'].max(), soft['LapTime'].max())

    # plot the distributions
    # set the background to be black
    plt.style.use('dark_background')
    # set grid lines to be grey
    plt.rcParams['grid.color'] = 'grey'
    # show grid lines
    plt.grid(True)
    # set the range of lap times / values that the distributions will be plotted over
    x = np.linspace(min_time, max_time + 3, 1000)
    # plot the pdfs
    plt.plot(x, driver_hard_dist.pdf(x), color = fastf1.plotting.COMPOUND_COLORS['HARD'], label='Hard')
    plt.plot(x, driver_medium_dist.pdf(x), color = fastf1.plotting.COMPOUND_COLORS['MEDIUM'], label='Medium')
    plt.plot(x, driver_soft_dist.pdf(x), color = fastf1.plotting.COMPOUND_COLORS['SOFT'], label='Soft')
    plt.legend()
    plt.xlabel('Lap Time')
    plt.ylabel('Probability Density')
    plt.title('Hamilton Lap Time Distributions')
    plt.show()

# define distributions for the tire wear on each tire
hard_wear_dist_10 = sts.halfnorm(0.2, 0.1)
hard_wear_dist_10_to_20 = sts.halfnorm(0.5, 0.2)
hard_wear_dist_20_to_30 = sts.halfnorm(1, 0.2)
hard_wear_dist_30_to_40 = sts.halfnorm(1.5, 0.2)
hard_wear_dist_after_40 = sts.halfnorm(2, 0.2)

medium_wear_dist_10 = sts.halfnorm(0.5, 0.2)
medium_wear_dist_10_to_20 = sts.halfnorm(1, 0.3)
medium_wear_dist_20_to_30 = sts.halfnorm(2, 0.4)
medium_wear_dist_after_30 = sts.halfnorm(3, 0.5)

soft_wear_dist_10 = sts.halfnorm(1, 0.3)
soft_wear_dist_10_to_20 = sts.halfnorm(2, 0.4)
soft_wear_dist_after_20 = sts.halfnorm(4, 0.5)

def tire_wear_hard(laps, threshold_value):
    '''
    This function takes in the number of laps and the threshold value and returns the tire wears and tire performance for the hard compound

    Parameters:
    laps (int): number of laps to run
    threshold_value (float): threshold value for the tire performance

    Returns:
    tire_wears (list): list of tire wears
    tire_performance (list): list of tire performance
    '''
    # initialize the lists and counter
    tire_wears = []
    tire_performance = [1]
    counter = 0
    # run until tire reaches threshold or counter reaches laps
    while tire_performance[-1] > threshold_value and counter < laps:
        # set the current tire performance
        current_tire_life = tire_performance[-1]
        # find the right distribution to use based on the counter, then append tire wear, update tire performance, and increment counter
        if counter < 10:
            tire_wears.append(hard_wear_dist_10.rvs()/100)
            current_tire_life -= tire_wears[counter]
            tire_performance.append(current_tire_life)
            counter += 1
        elif counter < 20:
            tire_wears.append(hard_wear_dist_10_to_20.rvs()/100)
            current_tire_life -= tire_wears[counter]
            tire_performance.append(current_tire_life)
            counter += 1
        elif counter < 30:
            tire_wears.append(hard_wear_dist_20_to_30.rvs()/100)
            current_tire_life -= tire_wears[counter]
            tire_performance.append(current_tire_life)
            counter += 1
        elif counter < 40:
            tire_wears.append(hard_wear_dist_30_to_40.rvs()/100)
            current_tire_life -= tire_wears[counter]
            tire_performance.append(current_tire_life)
            counter += 1
        else:
            tire_wears.append(hard_wear_dist_after_40.rvs()/100)
            current_tire_life -= tire_wears[counter]
            tire_performance.append(current_tire_life)
            counter += 1

    # remove the last element from tire performance because it is always less than the threshold value
    tire_performance.pop()

    return tire_wears, tire_performance    

def tire_wear_medium(laps, threshold_value):
    '''
    This function takes in the number of laps and the threshold value and returns the tire wears and tire performance for the medium compound

    Parameters:
    laps (int): number of laps to run
    threshold_value (float): threshold value for the tire performance

    Returns:
    tire_wears (list): list of tire wears
    tire_performance (list): list of tire performance
    '''
    # initialize the lists and counter
    tire_wears = []
    tire_performance = [1]
    counter = 0
    # run until tire reaches threshold or counter reaches laps
    while tire_performance[-1] > threshold_value and counter < laps:
        # set the current tire performance
        current_tire_life = tire_performance[-1]
        # find the right distribution to use based on the counter, then append tire wear, update tire performance, and increment counter
        if counter < 10:
            tire_wears.append(medium_wear_dist_10.rvs()/100)
            current_tire_life -= tire_wears[counter]
            tire_performance.append(current_tire_life)
            counter += 1
        elif counter < 20:
            tire_wears.append(medium_wear_dist_10_to_20.rvs()/100)
            current_tire_life -= tire_wears[counter]
            tire_performance.append(current_tire_life)
            counter += 1
        elif counter < 30:
            tire_wears.append(medium_wear_dist_20_to_30.rvs()/100)
            current_tire_life -= tire_wears[counter]
            tire_performance.append(current_tire_life)
            counter += 1
        else:
            tire_wears.append(medium_wear_dist_after_30.rvs()/100)
            current_tire_life -= tire_wears[counter]
            tire_performance.append(current_tire_life)
            counter += 1

    # remove the last element from tire performance because it is always less than the threshold value
    tire_performance.pop()
    
    return tire_wears, tire_performance

def tire_wear_soft(laps, threshold_value):
    '''
    This function takes in the number of laps and the threshold value and returns the tire wears and tire performance for the soft compound

    Parameters:
    laps (int): number of laps to run
    threshold_value (float): threshold value for the tire performance

    Returns:
    tire_wears (list): list of tire wears
    tire_performance (list): list of tire performance
    '''
    # initialize the lists and counter
    tire_wears = []
    tire_performance = [1]
    counter = 0
    # run until tire reaches threshold or counter reaches laps
    while tire_performance[-1] > threshold_value and counter < laps:
        # set the current tire performance
        current_tire_life = tire_performance[-1]
        # find the right distribution to use based on the counter, then append tire wear, update tire performance, and increment counter
        if counter < 10:
            tire_wears.append(soft_wear_dist_10.rvs()/100)
            current_tire_life -= tire_wears[counter]
            tire_performance.append(current_tire_life)
            counter += 1
        elif counter < 20:
            tire_wears.append(soft_wear_dist_10_to_20.rvs()/100)
            current_tire_life -= tire_wears[counter]
            tire_performance.append(current_tire_life)
            counter += 1
        else:
            tire_wears.append(soft_wear_dist_after_20.rvs()/100)
            current_tire_life -= tire_wears[counter]
            tire_performance.append(current_tire_life)
            counter += 1

    # remove the last element from tire performance because it is always less than the threshold value
    tire_performance.pop()
    
    return tire_wears, tire_performance

class Race:
    '''
    This class runs the simulation of the race and keeps track of all attributes associated with the race
    '''
    def __init__(self, proposed_tires, pit_time_lost, laps, distributions, race, threshold_value = 0.5):
        '''
        Intializes the class with the proposed tires, pit time lost, laps, and threshold value

        Parameters:
        proposed_tires (list): list of proposed tires
        pit_time_lost (float): time lost in the pit
        laps (int): number of laps to run
        '''
        self.proposed_tires = proposed_tires
        self.pit_time_lost = pit_time_lost
        self.threshold_value = threshold_value
        self.laps = laps
        self.name = race
        self.distribution_hard, self.distribution_medium, self.distribution_soft = distributions
        # intialize the attributes to keep track of
        self.stints = {}
        self.lap_times = []
        self.tire_performance = []
        self.total_time = 0

    def run(self):
        '''
        This function runs the simulation for the entire race and updates the attributes accordingly

        Parameters:
        None

        Returns:
        None
        '''
        # loop through the proposed tires
        for tire in self.proposed_tires:
            # if this isn't the first tire, add pit stop time to the total time
            if self.total_time != 0:
                self.total_time += self.pit_time_lost
            # get the proposed tire wear values for the tire and the right lap time distribution
            if tire == "HARD":
                proposed_tire_wears, proposed_tire_performance = tire_wear_hard(self.laps, self.threshold_value)
                lap_time_dist = self.distribution_hard
            elif tire == "MEDIUM":
                proposed_tire_wears, proposed_tire_performance = tire_wear_medium(self.laps, self.threshold_value)
                lap_time_dist = self.distribution_medium
            else:
                proposed_tire_wears, proposed_tire_performance = tire_wear_soft(self.laps, self.threshold_value)
                lap_time_dist = self.distribution_soft
            # set the stint length
            stint_length = len(proposed_tire_wears)
            # sample the lap times
            proposed_lap_times = lap_time_dist.rvs(stint_length)
            # append the lap times and tire performance to the lists
            for time in proposed_lap_times:
                self.lap_times.append(time)
            for performance in proposed_tire_performance:
                self.tire_performance.append(performance)
            # update the number of laps left
            self.laps -= stint_length
            # add the stint to the dictionary
            self.stints.update({tire: stint_length})
            # update the total_time variable to include the lap times for the stint
            self.total_time += sum(proposed_lap_times)


def get_race_stats(race):
    '''
    This function takes in the race object and returns a dataframe of the lap times

    Parameters:
    race: object
        the object that contains the race that was simulated
    
    Returns:
    lap_times_df: dataframe
        the dataframe of the lap times
    '''
    # get the lap times and tire performance
    lap_times = race.lap_times
    tire_performance = race.tire_performance
    # get the compounds from the stints
    compounds = []
    for key in race.stints:
        for i in range(race.stints[key]):
            compounds.append(key)

    # make a dataframe of the lap times and compounds
    lap_times_df = pd.DataFrame({'Race': race.name * len(lap_times), 'Lap Times': lap_times, 'Compound': compounds, 'Tire Performance': tire_performance})
    return lap_times_df

def plot_simulated_tire_performance(lap_times_df):
    '''
    This function takes in the dataframe of the lap times and plots the tire performance

    Parameters:
    lap_times_df: dataframe
        the dataframe of the lap times
    '''
        # set the background to be black to make the colors easier to read and standardize the style
    sns.set_style("ticks", rc = {"axes.facecolor": "black", "figure.facecolor": "grey"})
    fig, ax = plt.subplots()

    # get the unique compounds
    compounds = lap_times_df['Compound'].unique()

    # for each compound, plot the line and fill the area under the line
    for compound in compounds:
        df = lap_times_df[lap_times_df['Compound'] == compound]
        line = ax.plot(df.index, df['Tire Performance'], label=compound, color = fastf1.plotting.COMPOUND_COLORS[compound])
        ax.fill_between(df.index, df['Tire Performance'], color=line[0].get_color(), alpha=0.3)

    # annotate pit stops
    previous_compound = lap_times_df['Compound'].iloc[0]
    for i in range(1, len(lap_times_df)):
        current_compound = lap_times_df['Compound'].iloc[i]
        if current_compound != previous_compound:
            ax.annotate('Pit Lap', (i, lap_times_df['Tire Performance'].iloc[i]), textcoords="offset points",
                        color = "white", xytext=(-10,-100), ha='center')
        previous_compound = current_compound

    # set the x and y limits, labels, and title
    ax.set_xlim(0, 78)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Tire Performance")
    plt.suptitle(f"The driver's Simulated Tire Performance at {lap_times_df.Race[0]}")
    plt.grid(color = "w", which = 'major', axis = 'both')
    sns.despine(left = True, bottom = True)

    plt.legend()
    # get the plot's legend
    leg = ax.get_legend()
    # put the legend out of the plot
    leg.set_bbox_to_anchor((1.3, 1))
    # set the legend's background to transparent
    frame = leg.get_frame()
    frame.set_facecolor('none')
    plt.tight_layout()
    plt.show()

def plot_simulated_lap_times(lap_times_df):
    '''
    This function takes in the dataframe of the lap times and plots the lap times

    Parameters:
    lap_times_df: dataframe
        the dataframe of the lap times
    '''
    sns.set_style("ticks", rc = {"axes.facecolor": "black", "figure.facecolor": "grey"})
    fig, ax = plt.subplots()
    # make a scatterplot of the lap times that have been simulated for the Monaco Grand Prix
    sns.scatterplot(data = lap_times_df, x = lap_times_df.index, y = "Lap Times", 
                    ax = ax, hue = "Compound", palette = fastf1.plotting.COMPOUND_COLORS,
                    s = 80, linewidth = 0, legend = "auto")
    # set labels and title
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time (s)")
    plt.suptitle(f"The driver's Simulated Lap Times at {lap_times_df.Race[0]}")
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

def compare_results(actual_race, simulated_race):
    '''
    This function compares the actual race time with the simulated race time

    Parameters:
    actual_race: fastf1 object
        dataframe loaded from fastf1 for the actual race session
    simulated_race: object
        the object that contains the simulated race from the algorithm
    '''
    # retrieve the results
    results = actual_race.results
    # find the time from the actual race
    race_time = results[0:1].Time
    # convert the time to minutes
    actual_time = race_time.iloc[0].total_seconds()/60
    # get the predicted time from the simulation
    predicted_time = simulated_race.total_time/60
    # print the values for comparison
    print(f"During the race, the finish time was {actual_time : 2f} minutes")
    print(f"The predicted finish time was {predicted_time: 2f} minutes")