from pymongo import MongoClient
import certifi
from pymongo import database


def get_database(URI: str, DB: str) -> database.Database:
    # get certificate
    cert = certifi.where()

    # Create a new client and connect to the server
    client = MongoClient(
        URI,
        tlsCAFile=cert
    )

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!\n")
    except Exception as e:
        print(e)

    # return DB
    return client.get_database(DB)


if __name__ == '__main__':

    print(get_database(
        URI=f"mongodb+srv://ashikmp:animetrackercr38519@cluster0.yezkdho.mongodb.net/?retryWrites=true&w=majority",
        DB="animeDB"
    ).stats()
    )
