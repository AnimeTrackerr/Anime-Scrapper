import pymongo
from ConnectMongoDB import get_database
import os
from dotenv import load_dotenv
from tqdm import tqdm


def BuildSynonyms(URI: str, DataBase: str, *args: list):
    DB = get_database(URI=URI, DB=DataBase)
    animeCol = DB.get_collection("animeCollection")
    # mangaCol = DB.get_collection("mangaCollection")
    synonymsCol = DB.get_collection("animeSynCollection")

    # upload synonyms
    pbar = tqdm(initial=0, total=10000,
                desc="synonyms collected", colour="green")

    synonyms_list = []

    for doc in animeCol.find().sort('meanScoreAni', pymongo.DESCENDING).limit(10000):
        synonyms = []

        if doc["title"]["english"] != None:
            synonyms.append(str(doc["title"]["english"]))

        if doc["title"]["romaji"] != None:
            synonyms.append(str(doc["title"]["romaji"]))

        if len(doc["synonyms"]) != 0:
            synonyms.extend(doc["synonyms"])

        if len(synonyms) != 0:
            synonyms_list.append({
                "mappingType": "equivalent",
                "synonyms": synonyms
            })

        pbar.update(1)

    pbar.close()
    synonymsCol.insert_many(synonyms_list)


def AddNewSynonyms():
    pass


if __name__ == "__main__":
    load_dotenv()
    BuildSynonyms(URI=os.getenv("MONGODB_URI"), DataBase="animeDB")
