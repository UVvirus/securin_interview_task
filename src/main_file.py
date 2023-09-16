from src.crawler import *


def main():
    dictionary_data=get_request()
    filename=save_file(dictionary_data)
    json_file=read_file(filename)
    parsed_result=parse(json_file)
    return parsed_result


if __name__ == "__main__":
    main()
