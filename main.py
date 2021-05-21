"""CSC110 Fall 2020: Climate Change and Natural Disaster Sentiment Analysis

This is the main module that converts dataset of ids to tweet sentiments and then plots the results.

Copyright and Usage Information
==============================
This file is Copyright (c) 2020 Akash Ilangovan, Vijay Sambamurthy, Dharmpreet Atwal, Issam Arabi.
"""

from datetime import datetime, timedelta
from typing import List, Tuple

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import data_management
import gen_ids
import sentiment
import hydration

API_KEY = ""  # OMITTED
KEY_SECRET = ""  # OMITTED
ACCESS_TOKEN = ""  # OMITTED
ACCESS_TOKEN_SECRET = ""  # OMITTED
KEYS = (API_KEY, KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def ids_to_sentiment(directory: str, max_tweets: int, keys: Tuple[str, str, str, str], random: bool,
                     output_file: str) -> None:
    """
    Generates a csv of tweet sentiments from a directory of tweet ids.
    """
    if directory[-1] != "/" and directory[-1] != "\\":
        directory += "/"
    tweet_ids = directory
    csv_store = directory
    if random:
        gen_ids.randomize_csvs(directory, max_tweets)
        tweet_ids += 'generated_ids/randomized.txt'
        csv_store += 'randomized_data.csv'
    else:
        gen_ids.gen_regular_csvs(directory, max_tweets)
        tweet_ids += 'generated_ids/regularized.txt'
        csv_store += 'regularized_data.csv'
    print("Tweet Ids Generated.")
    hydration.generate_tweets(tweet_ids, csv_store, keys)
    print("Tweets Hydrated.")
    dat = data_management.read_csv_dict(csv_store)
    averages = sentiment.generate_average_sentiments(dat)
    data_management.convert_list_to_csv(output_file, averages)


def plot_with_dd_csv(filename: str, disaster_data: str) -> None:
    """
    Plot tweet sentiment data points in conjunction with natural disaster data points
    """
    data = data_management.read_csv_dict(filename)
    disaster_info = data_management.read_csv_dict(disaster_data)
    data = data_management.dict_to_list(data)
    disaster_info = data_management.dict_to_list(disaster_info)
    disaster_tweets = near_disater_data(data, disaster_info)
    plottable = list_to_plottable(data)
    plottable1 = list_to_plottable(disaster_tweets)
    legend = ["Non-Disaster Tweets", "Disaster Tweets"]
    plot([plottable, plottable1], legend)
    print("Average for non-disaster:", average_of_all(data))
    print("Average for disaster:", average_of_all(disaster_tweets))


def average_of_all(data: List[Tuple[datetime, float]]) -> float:
    """
    Return average sentiment of a list of tweet sentiments
    >>> average_of_all([(datetime(2020, 12, 11), 2.0), \
    (datetime(2020, 12, 11), 4.0), (datetime(2020, 12, 12), 3.0)])
    3.0
    """
    sum_value = 0
    for value in data:
        sum_value += value[1]
    return sum_value / len(data)


def near_disater_data(data: List[Tuple[datetime, float]],
                      info: List[Tuple[datetime]]) -> List[Tuple[datetime, float]]:
    """
    Remove any tweets that are within three days of a natural disaster
     and add them to a list for only disaster tweets.
    >>> tweets = [(datetime(2020, 12, 6), 2.0), (datetime(2020, 12, 12), 4.0),\
    (datetime(2020, 12, 10), 3.0)]
    >>> disaster_info = [(datetime(2020, 12, 11),)]
    >>> near_disater_data(tweets, disaster_info)
    [(datetime.datetime(2020, 12, 12, 0, 0), 4.0), (datetime.datetime(2020, 12, 10, 0, 0), 3.0)]
    >>> tweets
    [(datetime.datetime(2020, 12, 6, 0, 0), 2.0)]
    """
    near_disasters = []
    for value in data:
        for event in info:
            span_start = event[0] - timedelta(days=3)
            span_end = event[0] + timedelta(days=3)
            if span_end >= value[0] >= span_start and value not in near_disasters:
                near_disasters.append(value)

    for item in near_disasters:
        data.remove(item)

    return near_disasters


def list_to_plottable(data: List) -> Tuple[List[datetime], List[float]]:
    """
    Convert a list to a set of parallel lists
    >>> list_to_plottable([(datetime(2020, 12, 6), 2.0), (datetime(2020, 12, 10), 3.0)])
    ([datetime.datetime(2020, 12, 6, 0, 0), datetime.datetime(2020, 12, 10, 0, 0)], [2.0, 3.0])
    """
    list1 = []
    list2 = []
    for value in data:
        list1.append(value[0])
        list2.append(value[1])
    return (list1, list2)


############################

def plot(data: List[Tuple[List, List]], legend: List[str]) -> None:
    """
    Creates a scatter plot based on the input data(data) and legend (legend).
    """
    colors = ['blue', 'red', 'green']
    fig = plt.figure()
    ax = fig.add_subplot()
    plt.xlabel("Date")
    for values in data:
        ax.scatter(values[0], values[1], color=colors[data.index(values)])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.ylabel("Average Sentiment Value of Tweets")
    fig.legend(legend)
    plt.show()


def plot_from_csv(filename: str) -> None:
    """
    Directly attempts to plot from a given CSV File.
    """
    data = data_management.read_csv_dict(filename)
    data = data_management.dict_to_list(data)
    plottable = list_to_plottable(data)
    plot([plottable], ['All tweets on the day'])


if __name__ == "__main__":
    data_file = "data/backup_sentiments.csv"
    # This file has already been generated by the output of the line of code below
    # calling ids_to_sentiment.

    # In order to run it, please fill in the twitter api KEYS at the top. For more reference
    # please check twarc documentation at https://github.com/DocNow/twarc.
    # Also check twitter TOS and api https://developer.twitter.com/

    # Make sure there are txt/csv files within twarc_data/csvs/ for this program to work. Any number
    # of csvs would work.

    # Un-comment this line if you would like to test this with hydration.
    # ids_to_sentiment("twarc_data/", 20000, KEYS, False, data_file)

    plot_with_dd_csv(data_file, 'data/Disasters_Data.csv')

    import doctest
    doctest.testmod()
