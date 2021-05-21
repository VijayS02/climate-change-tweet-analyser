"""CSC110 Fall 2020: Climate Change and Natural Disaster Sentiment Analysis

This module hydrates contains functions that help hydrate the tweet ids.

Copyright and Usage Information
==============================
This file is Copyright (c) 2020 Akash Ilangovan, Vijay Sambamurthy, Dharmpreet Atwal, Issam Arabi.
"""
import csv
from typing import List

from tqdm import tqdm
from twarc import Twarc

API_KEY = ""  # OMITTED (Was for debugging)
KEY_SECRET = ""  # OMITTED (Was for debugging)
ACCESS_TOKEN = ""  # OMITTED (Was for debugging)
ACCESS_TOKEN_SECRET = ""  # OMITTED (Was for debugging)


def generate_tweets(tweet_ids: str, write_csv: str, keys: List[str]) -> None:
    """
    Convert a dateset of tweet ids to actual tweet content(text, date published, etc).
    """

    with open(write_csv, 'w+', errors="ignore", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["username~str", "date~%a %b %d %H:%M:%S %z %Y", "content~str"])
        t = Twarc(keys[0], keys[1], keys[2], keys[3])
        for tweet in tqdm(t.hydrate(open(tweet_ids))):
            data = [tweet['user']['screen_name'], tweet['created_at'], tweet['full_text']]
            writer.writerow(data)
        csv_file.close()


if __name__ == "__main__":
    # generate_tweets('data/tweet_ids/climate_id0.txt', 'data/demo.txt', API_KEY, KEY_SECRET,
    #                ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    import doctest
    doctest.testmod()
