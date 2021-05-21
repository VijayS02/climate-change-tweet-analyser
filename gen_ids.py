"""CSC110 Fall 2020: Climate Change and Natural Disaster Sentiment Analysis

This module contains the functions to read the csv files and shorten the dataset based on
user choice(random or regularized)

Copyright and Usage Information
==============================
This file is Copyright (c) 2020 Akash Ilangovan, Vijay Sambamurthy, Dharmpreet Atwal, Issam Arabi.
"""

import csv
import math
import random
from typing import List
from os import listdir
from os.path import isfile, join
from tqdm import tqdm

from jsonlines import jsonlines

import data_management


# Functions for Regular Option

def generate_regulars(data: List[int], max_step: int) -> List[List[int]]:
    """ Generate a set of evenly distributed tweet ids from a large dataset of tweet ids.

        For example a dataset of every 2000th tweet id from a dataset of 40 million tweets
    >>> tweet_ids = list(range(100))
    >>> regularized = generate_regulars(tweet_ids, 5, 20)
    >>> regularized[0] == [0]
    True
    >>> regularized[1] == [5]
    True
    >>> regularized[2] == [10]    ## Every 5th element is chosen
    True
    >>> regularized[3] == [15]
    True
    >>> regularized[4] == [20]
    True
    """
    regular_data = []
    n = 0
    for i in range(0, len(data), max_step):
        regular_data.append([data[i]])
        n += 1
    return regular_data


def gen_regular_csvs(directory: str, max_size: int) -> None:
    """
    Convert a directory of CSV files containing 40 million tweet ids to a shortened,
    regularized dataset of tweet ids.

    For example, every 2000th tweet in the dataset.
    """

    if directory[-1] != "/" and directory[-1] != "\\":
        directory += "/"
    csv_dir = directory + "csvs/"
    files = get_csvs_from_file(csv_dir)
    total_data = []
    for file in files:
        if file[-4:] == ".csv" or file[-4:] == ".txt":
            file = csv_dir + file
            total_data += read_csv(file)
    max_step = math.floor(len(total_data) / max_size)
    regularized = generate_regulars(total_data, max_step)
    data_management.convert_list_to_csv(directory + "generated_ids/regularized.txt", regularized)


# Functions for Random Option

def generate_randoms(data: List[int], max_step: int, max_size: int) -> List[List[int]]:
    """
    Generate a random set of tweet ids from a large dataset of tweet ids.

    For example choose 100,000 random tweets from a dataset of 40 million.
    """
    randomized_data = []
    random_selection = range(max_step)
    n = 0
    index = 0
    while n < max_size:
        index = index + random.choice(random_selection)
        if index > len(data):
            index = random.choice(random_selection)
        randomized_data.append([data[index]])
        n += 1
    return randomized_data


def randomize_csvs(directory: str, max_size: int) -> None:
    """
    Generate a csv of of randomly distributed tweet ids from a directory of
    CSVs containing tweet ids.
    """
    if directory[-1] != "/" and directory[-1] != "\\":
        directory += "/"
    csv_dir = directory + "csvs/"
    files = get_csvs_from_file(csv_dir)
    total_data = []
    for file in files:
        if file[-4:] == ".csv" or file[-4:] == ".txt":
            file = csv_dir + file
            total_data += read_csv(file)
    max_step = math.floor(len(total_data) / max_size)
    randomized = generate_randoms(total_data, max_step, max_size)
    data_management.convert_list_to_csv(directory + "generated_ids/randomized.txt", randomized)


def read_csv(filename: str) -> List[int]:
    """
    Helper file to read csv files to a list.
    """
    data = []
    with open(filename) as file:
        reader = csv.reader(file)
        for line in tqdm(reader):
            data.append(int(line[0]))
    return data


def get_csvs_from_file(directory: str) -> List[str]:
    """
    Get all csv files from a specified directory
    """
    files = [file for file in listdir(directory) if isfile(join(directory, file))]
    return files


def count_lines_json(filename: str) -> int:
    """
    Return number of lines in JSONL file for debugging purposes

    """
    #  store = []
    n = 0
    with jsonlines.open(filename) as reader:
        for _ in tqdm(reader):
            n += 1
    return n


def count_lines_csv(filename: str) -> int:
    """
    Count lines in CSV file for debugging purposes
    """
    #  store = []
    n = 0
    with open(filename) as file:
        reader = csv.reader(file)
        for _ in tqdm(reader):
            n += 1
    return n


if __name__ == "__main__":
    # gen_regular_csvs("twarc_data/", 20000)
    # count_lines_JSON('twarc_data/tweets.jsonl')
    # count_lines_CSV("twarc_data/csvs/randomized.txt")
    import doctest
    doctest.testmod()
