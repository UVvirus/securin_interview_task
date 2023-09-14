import json
import os
import xmltodict
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=".env")

BASE_URL = os.environ.get("BASE_URL")


def __get_request(BASE_URL: str) -> dict:
    header = {"Accept": "application/xml"}

    response = requests.get(BASE_URL, headers=header)
    if response.status_code == 200:
        dict_data = xmltodict.parse(response.content)
        return dict_data


def save_file(filename: str, dict_data: dict):
    """

    :param filename: Name of the json file
    :param dict_data: dictionary data we got from the get_request() method
    :return: None

    This function is to save network calls. Instead of sending request to the googlenews,
    we are saving the output and parsing it locally
    """
    exists = filename + ".json"
    if os.path.isfile(exists):
        return "File already exists"

    with open(f"{filename}.json", "w") as file:
        json_data = json.dumps(dict_data)
        file.write(json_data)
    file.close()


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


def __parse(dict_data: dict):
    top_stories=dict_data["rss"]["channel"]["title"]
    print(top_stories)

    for i in range(5):
        published_date = dict_data["rss"]["channel"]["item"][i]["pubDate"]
        print("Date:",published_date)
        title=dict_data["rss"]["channel"]["item"][i]["title"]
        print("Title:",title)
        url=dict_data["rss"]["channel"]["item"][i]["link"]
        print("URL:",url)
        print("=======================================================================================")



if __name__ == "__main__":
    # x = get_request(BASE_URL)
    # save_file("output_file",x)
    x=read_file("output_file.json")
    __parse(x)
