"""CSC110 Fall 2020: Climate Change and Natural Disaster Sentiment Analysis

This module contains functions to help manage the date used in our project.

Copyright and Usage Information
==============================
This file is Copyright (c) 2020 Akash Ilangovan, Vijay Sambamurthy, Dharmpreet Atwal, Issam Arabi.
"""
import jsonlines

import csv
import string
from typing import List, Dict, Tuple
from datetime import datetime
from tqdm import tqdm


def readJSONL(filename: str) -> List[List[str]]:
    """
    Reads JSONL file (filename) and converts it into a List of Lists.
    """
    store = [["username~str", "date~%a %b %d %H:%M:%S %z %Y", "content~str"]]
    with jsonlines.open(filename) as reader:
        for obj in tqdm(reader):
            store.append([obj['user']['screen_name'],
                          obj['created_at'],
                          obj['full_text']])
    print("\nreadJSONL: File Read.")
    return store


def clean_string(dirty: str) -> str:
    """
    OPTIONAL function for cleaning up JSONL file look. With this function the list generated by
    readJSONL is more uniform. However, this can cause errors with certain
    emojis/characters and is not used because of this.

    In order to implement, call this function around strings that want to be cleaned. Usually called
    on obj['full_text'] from function readJSONL.
    """

    printable = set(string.printable)
    cleaned = ''.join(filter(lambda x: x in printable, dirty))
    return str(cleaned.encode('unicode-escape'))[2:-1]


def convert_list_to_csv(filename: str, data: List) -> None:
    """
    Writes out a list of lists into a csv (filename)
    """
    with open(filename, 'w+', errors="ignore", newline='') as write_file:
        writer = csv.writer(write_file)
        for line in tqdm(data):
            writer.writerow(line)
        write_file.close()
    print("\nconvert_list_to_csv: File written.")


def gen_header(head: List[str]) -> Dict:
    """
    This is a helper function meant to generate a dictionary that contains parsing information
    for csvs. I.e. it stores how to manage datetimes, integers and floats. Strings are pretty much
    ignored.

    >>> gen_header(["date~%m/%d/%Y","sentiment_value~float"])
    {'date': "datetime.strptime(row[0],'%m/%d/%Y')", 'sentiment_value': 'float(row[1])'}
    """
    final = {}
    for val in head:
        val = val.split('~')
        final[val[0]] = val[1]
    return final


def dict_to_list(data: List[Dict]) -> List[Tuple]:
    """
    Converts a given list of dictionaries to a list of tuples.
    Done by eliminating the keys of the dictionary.

    >>> dict_data = [{"Key1": 123.23, "Key2": "Value2", "Key3": 200}, \
    {"Key1": 20.23, "Key2": "2", "Key3": 0}]
    >>> dict_to_list(dict_data)
    [(123.23, 'Value2', 200), (20.23, '2', 0)]
    """
    list_store = []
    for value in tqdm(data):
        temp = []
        for key in value:
            temp.append(value[key])
        temp = tuple(temp)
        list_store.append(temp)
    return list_store


def read_csv_dict(filename: str) -> List[Dict]:
    """
    Using helper function gen_header, this function reads a csv into a dictionary.
    This is done by reading the first line into the gen_header function, then all subsequent lines
    are formatted by the protocol defined in the header.

    Originally, eval() was used with some tests to make sure the string was safe to execute,
    however, upon further consideration, this was removed and replaced with a less modular solution.
    """
    data = []
    n = 0
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        header = gen_header(next(reader))
        for row in tqdm(reader):
            temp_dict = {}
            i = 0
            for value in header:
                if 'date' in value:
                    temp_dict[value] = datetime.strptime(row[i], header[value])
                elif 'int' in header[value]:
                    temp_dict[value] = int(row[i])
                elif 'float' in header[value]:
                    temp_dict[value] = float(row[i])
                else:
                    temp_dict[value] = row[i]
                i += 1
            data.append(temp_dict)
            n += 1
        file.close()
    print(f"\nread_csv_dict: File {filename} Processed.")
    return data


def convert_jsonl_to_csv(input_jsonl: str, output_csv: str) -> None:
    """
    Uses other functions to convert a JSONL file (input_jsonl) to a CSV.
    """
    json_data = readJSONL(input_jsonl)
    convert_list_to_csv(output_csv, json_data)


if __name__ == "__main__":
    # convert_jsonl_to_csv("C:\\cs\\tweet_ids\\tweets.jsonl", "data\\data_1.csv")
    # read_csv_dict('data/Disasters_Data.csv')
    import doctest
    doctest.testmod()
