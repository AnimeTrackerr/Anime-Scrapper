import dotenv
import json
import os
import multiprocessing as mp
import time
from tqdm import tqdm
from Utils.ConnectMongoDB import get_database
from Utils.FetchAnime import AnimeScrapper
from Utils.QueryParams import AnimeMetaData, Pagination, Variables
from Utils.ReduceData import ReduceExistingData, ReduceData
# function to scrape anime


def ScrapeAnime():
    anime_dir = 'Data/AnimeData'

    # create directory to collect data
    if(not os.path.exists(anime_dir)):
        os.makedirs(anime_dir)

    # fetch last executed page
    lastExecuted = 0

    with open('Progress.json', 'r+') as progressFile:
        try:
            obj = json.load(progressFile)

            if("lastExecutedPage" in obj.keys()):
                lastExecuted = obj["lastExecutedPage"]
            else:
                json.dump({"lastExecutedPage": 0}, progressFile, indent=4)

        except json.decoder.JSONDecodeError:
            print("No JSON data to load; creating new entry !!")
            json.dump({"lastExecutedPage": 0}, progressFile, indent=4)

    Variables["page"] = lastExecuted + 1

    # fetch anime
    progressBar = tqdm(initial=Variables["page"], total=2250, colour='green',
                       unit='page', desc='Anime Downloaded')

    with open('Progress.json', 'w+') as progressFile:
        # set query and pagination
        while True:
            fetchObj = AnimeScrapper(
                base_url='https://graphql.anilist.co',
                query="query ($id: Int, $page: Int, $perPage: Int, $charLimitPerAnime: Int, $sortCharBasedOn: [CharacterSort]) { "
                + "Page(page: $page, perPage: $perPage) {"
                + Pagination
                + AnimeMetaData
                + "}"
                + "}"
            )

            # fetch anime
            anime, rateLimitRemaining = fetchObj.getAnimeByID(
                variables=Variables)

            pageInfo = anime["data"]["Page"]["pageInfo"]

            if(not pageInfo["hasNextPage"]):
                break

            # dump the page(list of anime) into a file
            with open(f'{anime_dir}/page {pageInfo["currentPage"]}.json', 'w') as animeFile:
                # reduce the data to a lean form and then dump
                anime["data"]["Page"]["media"] = ReduceData(
                    anime["data"]["Page"]["media"])
                json.dump(anime["data"]["Page"]["media"], animeFile)

            # update all the variables involved
            progressFile.seek(0)
            json.dump(
                {
                    "lastExecutedPage": pageInfo["currentPage"],
                    "SkipDocs": 0
                },
                progressFile,
                indent=4
            )
            Variables["page"] += 1
            progressBar.update(1)

            # if reate-limit exceeded then sleep
            if(rateLimitRemaining == 1):
                time.sleep(60)

        progressBar.close()

# function to upload scrapped anime to Mongo DB


def UploadAnimeToMongoDB(URI: str, uploadDir: str):
    DB = get_database(
        URI=URI,
        DB="animeDB"
    )

    animeCollection = DB["animeCollection"]
    mangaCollection = DB["mangaCollection"]
    pool = mp.Pool(mp.cpu_count())

    # sort file names
    fileNames = sorted(os.listdir(uploadDir), key=lambda k: int(k[5:-5]))

    # iterate files and upload
    for fileName in tqdm(fileNames, desc='Anime/Manga Uploaded', colour='green', unit='page'):

        with open(f'{uploadDir}/{fileName}', 'r') as file:
            page_i = json.load(file)
            anime = [i for i in page_i if i["type"] == "ANIME"]
            manga = [i for i in page_i if i["type"] == "MANGA"]

            pool.map(
                lambda collection, data: collection.insert_many(data),
                [
                    (animeCollection, anime),
                    (mangaCollection, manga)
                ]
            )

# upload anime to Dynamo DB


def UploadAnimeToDynamoDB(uploadDir: str, ClientInfo: dict):
    # sort file names
    fileNames = sorted(os.listdir(uploadDir), key=lambda k: int(k[5:-5]))

    # iterate files and upload
    for fileName in tqdm(fileNames, desc='Anime Uploaded', colour='green', unit='page'):
        with open(f'{uploadDir}/{fileName}', 'r') as file:
            pass


if __name__ == '__main__':
    # get env variables
    dotenv.load_dotenv()

    # scrape anime
    do = input("\nDo You Want to Scrape Anime ? (y/n)")
    if do == 'y':
        ScrapeAnime()

    # upload anime to MongoDB
    do = input("\nDo You Want to Upload Anime to MongoDB ? (y/n)")
    if do == 'y':
        UploadAnimeToMongoDB(URI=os.getenv("MONGODB_URI"),
                             uploadDir='Data/AnimeData')

    # reduce existing data
    do = input("\nDo You Want to Reduce Existing DB ? (y/n)")
    if do == 'y':
        with open("Progress.json", 'r') as file:
            SkipDocs = json.load(file)

            if "SkipDocs" in SkipDocs.keys():
                SkipDocs = SkipDocs["SkipDocs"]
            else:
                SkipDocs = 1

        ReduceExistingData(URI=os.getenv("MONGODB_URI"),
                           DB="animeDB",
                           Collection="animeCollection",
                           Skip_Docs=SkipDocs
                           )
