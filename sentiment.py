"""CSC110 Fall 2020: Climate Change and Natural Disaster Sentiment Analysis

This module does the sentiment analysis computations on the dataset

Copyright and Usage Information
==============================
This file is Copyright (c) 2020 Akash Ilangovan, Vijay Sambamurthy, Dharmpreet Atwal, Issam Arabi.
"""

import data_management
import datetime
from typing import List, Tuple, Dict
from tqdm import tqdm
import math

from textblob import TextBlob


def generate_average_sentiments(raw_dat: List[Dict]) -> List[Tuple[str, float]]:
    """
        Return the average tweet sentiment for each day as a list from a
        dictionary of unsorted tweet data
        >>> raw_tweets = [{'date':datetime.datetime(2020,2,5), 'username': "Twitter_user", \
        'content' : "Tweet about Climate change"}]
        >>> generate_average_sentiments(raw_tweets)
        [['date~%m/%d/%Y', 'sentiment_value~float'], ('02/05/2020', 0.0)]
    """
    daily_data_timestamps = []
    daily_data_sentiment = []
    for val in tqdm(raw_dat):
        cur_date = val['date'].strftime('%m/%d/%Y')

        sent = get_sentiment(val['content'])
        if cur_date not in daily_data_timestamps:
            daily_data_timestamps.append(cur_date)
            daily_data_sentiment.append([sent])
        else:
            pos = daily_data_timestamps.index(cur_date)
            daily_data_sentiment[pos].append(sent)

    calculated_avgs = [['date~%m/%d/%Y', 'sentiment_value~float']]
    for i in range(len(daily_data_sentiment)):
        sum_for_avg = 0
        for value in daily_data_sentiment[i]:
            sum_for_avg += value
        average = sum_for_avg / len(daily_data_sentiment[i])
        calculated_avgs.append((daily_data_timestamps[i], average))
    #  print("generate_average_sentiments: Data Generated.")
    return calculated_avgs


def get_sentiment(input_text: str) -> int:
    """ Get sentiment value for a string using the TextBlob module.

        Sentiment is on a scale from -1 to 1. With 1 being very positive and -1 being very negative.
        >>> input_string = "This is a very negative review about a very bad product"
        >>> math.isclose(-0.65, get_sentiment(input_string))
        True

    """
    return TextBlob(input_text).sentiment.polarity


def generate_sent_from_json(filename: str, output_file: str) -> None:
    """
    Generate csv file of tweet sentiment from JSON file containing raw tweet
    """
    csv_temp = filename.replace(".jsonl", '.csv')
    data_management.convert_jsonl_to_csv(filename, csv_temp)
    dat = data_management.read_csv_dict(csv_temp)
    averages = generate_average_sentiments(dat)
    data_management.convert_list_to_csv(output_file, averages)


if __name__ == "__main__":
    # generate_sent_from_JSON('twarc_data/regular_tweets.jsonl', 'data/regular_sentiments.csv')
    import doctest
    doctest.testmod()
