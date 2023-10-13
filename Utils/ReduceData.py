import json
from .ConnectMongoDB import get_database
from tqdm import tqdm

# as the anime metadata from anilist api is incredibly bulky, there was a need to reduce the data.

# function ReduceData() -> for new documents


def ReduceData(data: dict) -> dict:
    # reduce tag list
    data["tags"] = data["tags"][:10]

    # reduce nesting in characters list
    data["characters"] = data["characters"][:8]
    data["characters"] = data["characters"]["edges"]

    for i in range(len(data["characters"])):
        data["characters"][i]["name"] = data["characters"][i]["node"]["name"]["full"]
        data["characters"][i]["image"] = data["characters"][i]["node"]["image"]["medium"]

        for j in range(len(data["characters"][i]["voiceActors"])):
            data["characters"][i]["voiceActors"][j]["image"] = data["characters"][i]["voiceActors"][j]["image"]["medium"]
            data["characters"][i]["voiceActors"][j]["name"] = data["characters"][i]["voiceActors"][j]["name"]["full"]

        del data["characters"][i]["node"]

    # reduce studio list
    data["studios"] = data["studios"][:3]

    # reduce nesting in studios list
    data["studios"] = data["studios"]["edges"]

    for i in range(len(data["studios"])):
        data["studios"][i]["name"] = data["studios"][i]["node"]["name"]
        del data["studios"][i]["node"]

    return data

# helper function


def update_document(collection, document):
    with collection.start_transaction():
        collection.update_one(
            {"_id": document["_id"]},
            {"$set": ReduceData(document)}
        )

# function ReduceExistingData() -> for existing documents in mongoDB atlas


def ReduceExistingData(URI: str, DB: str, Collection: str, Skip_Docs: int):
    AnimeDB = get_database(URI=URI, DB=DB)
    AnimeCollection = AnimeDB.get_collection(Collection)
    # pool = mp.Pool(mp.cpu_count())

    progressbar = tqdm(initial=Skip_Docs, colour='green', unit='anime',
                       desc='Anime Updated', total=AnimeCollection.count_documents({}))

    try:
        lastExecuted = Skip_Docs
        with AnimeCollection.find().skip(Skip_Docs) as cursor:
            for document in cursor:
                AnimeCollection.update_one(
                    {"_id": document["_id"]},
                    {"$set": ReduceData(document)}
                )

                progressbar.update(1)
                lastExecuted += 1
                # pool.apply_async(update_document, args=(AnimeCollection, document))

            cursor.close()
        progressbar.close()

    except Exception as e:
        # save progress
        with open("../Progress.json", 'w+') as file:
            data = json.load(file)
            data["SkipDocs"] = lastExecuted
            json.dump(data, file)

        # print error
        print(e)
