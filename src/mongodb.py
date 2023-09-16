from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError, BulkWriteError
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

DB_URL = os.environ.get("DB_URL")

client = MongoClient(DB_URL)
database_name = client["dbname"]
collection = database_name["collection_name"]


def insert(documents):
    try:
        # Create the unique index on "Hashed" if it doesn't exist
        # Check if an index with the same name exists
        existing_index_info = None
        for index_info in collection.list_indexes():
            print(1)
            if index_info["name"] == "Hash_1":
                print(2)
                existing_index_info = index_info
                break

        # Drop the existing index if it exists
        if existing_index_info:

            collection.drop_index("Hash_1")

        collection.create_index([("Hash", ASCENDING)], unique=True, name="IndexName")



    except DuplicateKeyError:
        pass

    batch_size = 100  # Adjust the batch size as needed
    for i in range(0, len(documents), batch_size):

        batch = documents[i:i + batch_size]
        try:
            collection.insert_many(batch, ordered=False)

        except BulkWriteError as e:
            # Handle the bulk write error, if necessary
            print(e)


def query_from_database(user_input) -> list:
    results_from_db = []
    documents = collection.find({"website": user_input}, {"Hash": 0, '_id': 0})
    for document in documents:
        results_from_db.append(document)
    return results_from_db


if __name__ == "__main__":
    # create_db("test")
    # x = read_file("output_file.json")
    # y=__parse(x)
    #
    # insert(y)
    query_from_database("https://indianexpress.com")
