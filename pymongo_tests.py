# coding: utf8
# !/usr/bin/env sh

import datetime
from pymongo import MongoClient
import pymongo
import pprint


def _HEADER(header):
    print()
    print("{}".format('#' * 50))
    print("{HEADER}¶".format(HEADER=header))
    print("{}".format('#' * 50))


def _EXECUTE_PYMONGO_CMD(pymongo_cmd, desc=None):
    """
    """
    results_cmd = None
    if desc:
        print("{}".format(desc))
    if pymongo_cmd:
        str_output = "[pymongo][cmd] {}".format(pymongo_cmd)
        results_cmd = eval(pymongo_cmd)
        if results_cmd:
            str_output += " ->\n{}".format(pprint.pformat(results_cmd, indent=4))
        print(str_output)
    return results_cmd


if __name__ == '__main__':
    # Making a Connection with MongoClient¶
    _HEADER("Making a Connection with MongoClient")

    uri = 'mongodb://{user}:{passwd}@{host}:{port}/{db_name}'.format(
        host='127.0.0.1',
        port=27017,
        db_name='kanban',
        user='kanbanUser',
        passwd='unAutrePasswordQuiVaBien',
    )
    print("URI Mongo connection: {}".format(uri))

    with MongoClient(uri) as client:
        # Getting a Database¶
        _HEADER("Getting a Database")
        db = _EXECUTE_PYMONGO_CMD(
            desc="Retrieve kanban database access",
            pymongo_cmd="client.kanban"
        )

        # Show Collection¶
        _HEADER("Show Collection")
        show_collections = _EXECUTE_PYMONGO_CMD(
            desc="Show collections in 'kanban' database",
            pymongo_cmd='db.collection_names(include_system_collections=True)'
        )

        # Getting a Collection¶
        _HEADER("Getting a Collection")
        kanban = posts = _EXECUTE_PYMONGO_CMD(
            desc="Retrieve 'kanban' collection (in 'kanban' db)",
            pymongo_cmd='db.kanban'
        )

        # Drop Collection¶
        _HEADER("Drop Collection")
        _EXECUTE_PYMONGO_CMD(
            pymongo_cmd='posts.drop()'
        )

        # Documents¶
        _HEADER("Documents")
        post = {
            "author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()
        }
        print("INPUTS -> post")
        pprint.pprint(post, indent=4)

        # Inserting a Document¶
        _HEADER("Inserting a Document")
        post_id = _EXECUTE_PYMONGO_CMD(
            pymongo_cmd='posts.insert_one(post).inserted_id',
            desc='DB_RESULTS -> post_id'
        )

        # After inserting the first document, the posts collection has actually been created on the server.
        # We can verify this by listing all of the collections in our database:
        print(db.collection_names(include_system_collections=False))

        # Getting a Single Document With find_one()¶
        _HEADER("Getting a Single Document With find_one()")
        # find_one() also supports querying on specific elements that the resulting document must match.
        # To limit our results to a document with author “Mike” we do:
        _EXECUTE_PYMONGO_CMD(
            pymongo_cmd='posts.find_one({"author": "Mike"})',
            desc='Find elements: Match happen'
        )

        # If we try with a different author, like “Eliot”, we’ll get no result:
        _EXECUTE_PYMONGO_CMD(
            pymongo_cmd='posts.find_one({"author": "Eliot"})',
            desc='Find elements: Match failed'
        )

        # Querying By ObjectId¶
        _HEADER("Querying By ObjectId")
        _EXECUTE_PYMONGO_CMD(
            pymongo_cmd='posts.find_one({"_id": post_id})',
        )

        post_id_as_str = str(post_id)
        posts.find_one({"_id": post_id_as_str})     # No result
        _EXECUTE_PYMONGO_CMD(
            pymongo_cmd='posts.find_one({"_id": post_id_as_str})',
            desc='No result'
        )

        # Bulk Inserts¶
        _HEADER("Bulk Inserts")
        new_posts = [
            {
                "author": "Mike",
                "text": "Another post!",
                "tags": ["bulk", "insert"],
                "date": datetime.datetime(2009, 11, 12, 11, 14)
            },
            {
                "author": "Eliot",
                "title": "MongoDB is fun",
                "text": "and pretty easy too!",
                "date": datetime.datetime(2009, 11, 10, 10, 45)
            }
        ]
        print("new_posts:")
        pprint.pprint(new_posts, indent=4)
        _EXECUTE_PYMONGO_CMD(
            pymongo_cmd='posts.insert_many(new_posts)'
        )

        # Querying for More Than One Document¶
        _HEADER("Querying for More Than One Document")
        _EXECUTE_PYMONGO_CMD(
            pymongo_cmd='posts.find()'
        )
        _EXECUTE_PYMONGO_CMD(
            pymongo_cmd='posts.find({"author": "Mike"})'
        )

        # Counting¶
        _HEADER("Counting")
        _EXECUTE_PYMONGO_CMD(pymongo_cmd='posts.count()')
        _EXECUTE_PYMONGO_CMD(pymongo_cmd='posts.find({"author": "Mike"}).count()')

        # Range Queries¶
        _HEADER("Range Queries")
        d = datetime.datetime(2009, 11, 12, 12)
        _EXECUTE_PYMONGO_CMD(
            pymongo_cmd='posts.find({"date": {"$lt": d}}).sort("author")',
            desc="request datetime: < {}".format(d)
        )

        # Indexing¶
        _HEADER("Indexing")
        _EXECUTE_PYMONGO_CMD(
            pymongo_cmd='db.profiles.drop()',
        )

        result = _EXECUTE_PYMONGO_CMD(
            pymongo_cmd="db.profiles.create_index([('user_id', pymongo.ASCENDING)], unique=True)",
        )
        index_information = _EXECUTE_PYMONGO_CMD(
            pymongo_cmd="sorted(list(db.profiles.index_information()))"
        )

        user_profiles = [
            {'user_id': 211, 'name': 'Luke'},
            {'user_id': 212, 'name': 'Ziltoid'}
        ]
        pprint.pprint("user_profiles: {}".format(user_profiles), indent=4)
        print("insert many")
        result = db.profiles.insert_many(user_profiles)
        print("result: {}".format(result))

        new_profile = {'user_id': 213, 'name': 'Drew'}
        print("insert new profile => This is fine !")
        result = db.profiles.insert_one(new_profile)  # This is fine.

        duplicate_profile = {'user_id': 212, 'name': 'Tommy'}
        print("insert duplicate profile => Exception !")
        try:
            result = db.profiles.insert_one(duplicate_profile)
        except pymongo.errors.DuplicateKeyError as e:
            print("Exception 'pymongo.errors.DuplicateKeyError' catched !\n{}".format(repr(e)))
