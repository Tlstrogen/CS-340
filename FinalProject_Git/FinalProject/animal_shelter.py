# animal_shelter.py

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(self):
        """
        Initialize the connection to the MongoDB database using environment variables.
        """
        # Load environment variables from .env file if it exists
        load_dotenv()

        # Fetching credentials from environment variables
        USER = os.getenv('MONGO_USER')
        PASS = os.getenv('MONGO_PASS')
        HOST = os.getenv('MONGO_HOST')
        PORT = os.getenv('MONGO_PORT')
        DB = os.getenv('MONGO_DB_NAME')
        COL = os.getenv('MONGO_COLLECTION')

        if not all([USER, PASS, HOST, PORT, DB, COL]):
            raise EnvironmentError("One or more MongoDB environment variables are missing.")

        # Building the MongoDB URI using the provided connection details
        uri = f"mongodb://{USER}:{PASS}@{HOST}:{PORT}/?authSource=admin"

        try:
            # Trying to connect to MongoDB with the URI we just built
            self.client = MongoClient(uri)
            # Accessing the specific database
            self.database = self.client[DB]
            # And now, getting the specific collection within that database
            self.collection = self.database[COL]
            print("Successfully connected to MongoDB!")
        except ConnectionFailure as e:
            # If something goes wrong with the connection, we'll let you know
            print(f"Could not connect to MongoDB: {e}")

    def create(self, data):
        """
        Insert a document into the collection.
        :param data: A dictionary containing the document to be inserted.
        :return: True if insert is successful, else False.
        """
        if data:
            try:
                # Let's try adding the new document to our collection
                insert_result = self.collection.insert_one(data)
                # If MongoDB gives us an ID back, we know it worked
                if insert_result.inserted_id:
                    print("Document inserted successfully.")
                    return True
                else:
                    print("Document insertion failed.")
                    return False
            except Exception as e:
                # Oops, something went wrong while inserting
                print(f"An error occurred while inserting: {e}")
                return False
        else:
            # You need to provide some data to insert!
            raise ValueError("The data parameter is empty")

    def read(self, query):
        """
        Query documents from the collection.
        :param query: A dictionary specifying the query criteria.
        :return: A list of documents matching the query if successful, else an empty list.
        """
        if query is not None:
            try:
                # Let's fetch the documents that match our query
                cursor = self.collection.find(query)
                # Converting the cursor to a list so we can work with it easily
                results = [document for document in cursor]
                print(f"Found {len(results)} document(s) matching the query.")
                return results
            except Exception as e:
                # Something went wrong while fetching the documents
                print(f"An error occurred while querying: {e}")
                return []
        else:
            # You need to specify what you're looking for!
            raise ValueError("The query parameter is empty")

    def update(self, query, update_data):
        """
        Update document(s) in the collection that match the query criteria.
        :param query: A dictionary specifying the query criteria.
        :param update_data: A dictionary specifying the fields to update.
        :return: The number of documents modified.
        """
        if query and update_data:
            try:
                # Let's update the documents that match our query with the new data
                update_result = self.collection.update_many(query, {'$set': update_data})
                print(f"Updated {update_result.modified_count} document(s).")
                return update_result.modified_count
            except Exception as e:
                # Something went wrong during the update
                print(f"An error occurred while updating: {e}")
                return 0
        else:
            # We need both a query to find the documents and the new data to update them with
            raise ValueError("The query and update_data parameters cannot be empty")

    def delete(self, query):
        """
        Delete document(s) from the collection that match the query criteria.
        :param query: A dictionary specifying the query criteria.
        :return: The number of documents deleted.
        """
        if query:
            try:
                # Let's remove the documents that match our query
                delete_result = self.collection.delete_many(query)
                print(f"Deleted {delete_result.deleted_count} document(s).")
                return delete_result.deleted_count
            except Exception as e:
                # Something went wrong while trying to delete
                print(f"An error occurred while deleting: {e}")
                return 0
        else:
            # You need to tell us which documents to delete!
            raise ValueError("The query parameter is empty")
