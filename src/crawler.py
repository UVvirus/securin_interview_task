import json
import os
import xmltodict
import requests
from dotenv import load_dotenv, find_dotenv
import hashlib
import time

load_dotenv(dotenv_path="../.env")

BASE_URL = os.environ.get("BASE_URL")



def get_request() -> dict:
    header = {"Accept": "application/xml"}

    response = requests.get(BASE_URL, headers=header)
    if response.status_code == 200:
        dict_data = xmltodict.parse(response.content)
        return dict_data


def save_file(dict_data: dict):
    """

    :param dict_data: dictionary data we got from the get_request() method
    :return: filname with json extension

    This function is to save network calls. Instead of sending request to the googlenews,
    we are saving the output and parsing it locally
    """
    #filename=hashlib.md5(dict_data).hexdigest()
    filename=str(time.time())
    filename=hashlib.md5(filename.encode()).hexdigest()
    exists = filename + ".json"
    if os.path.isfile(exists):
        return "File already exists"

    with open(f"{filename}.json", "w") as file:
        json_data = json.dumps(dict_data)
        file.write(json_data)
    file.close()

    return exists


def read_file(filename: str):
    """
    :param filename: Name of the file to read
    """

    try:
        if filename.split(".")[-1] != "json":
            return "Only JSON Filetype is supported"

        with open(filename, "r") as file:
            f = file.read()
            loaded_json_data = json.loads(f)
        return loaded_json_data
    except FileNotFoundError as file_not_found:
        return file_not_found


def parse(dict_data: dict) -> list:
    """

    :param dict_data: data we got from read_file() method
    :return: returns a list which contains Title, date and url
    """
    top_stories = dict_data["rss"]["channel"]["title"]
    print(top_stories)
    result = []
    url_set = set()  # A set that will keep track of all the website urls, Incase user enters wrong url
    # this will be shown


    for i in range(5):
        published_date = dict_data["rss"]["channel"]["item"][i]["pubDate"]

        title = dict_data["rss"]["channel"]["item"][i]["title"]

        url = dict_data["rss"]["channel"]["item"][i]["link"]
        website = dict_data["rss"]["channel"]["item"][i]["source"]["@url"]

        url_set.add(website)  # planning to show this to user for reference

        hAsh = md5hash(title, url)
        result_dict = {"Hash": hAsh,
                       "pub_date": published_date,
                       "title": title,
                       "url": url,
                       "website": website}
        result.append(result_dict)
    #print(result)
    return result


def md5hash(title: str, url: str) -> str:
    # create a md5 hash using title and url
    bytes = title + url
    encoded_data = hashlib.md5(bytes.encode())
    Hash = encoded_data.hexdigest()

    return Hash


if __name__ == "__main__":
    # x = get_request(BASE_URL)
    # save_file("output_file",x)
    x = read_file("../output_file.json")
    parse(x)
