import boto3
from botocore.config import Config
import json

my_config = Config(
    region_name='ap-south-1',
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

client = boto3.client(
    'dynamodb',
    aws_access_key_id="AKIAU7JS6AAIZ3IYAAGC",
    aws_secret_access_key="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",
    config=my_config
)

item = {
    "id": 165992,
    "title": {"english": None, "romaji": "Jitsuroku: Hoikushi Deko Sensei"},
    "synonyms": ["Nursery School Teacher Deko Sensei"],
    "type": "MANGA",
    "episodes": None,
    "meanScoreAni": None,
    "genres": ["Comedy", "Slice of Life"],
    "tags": [],
    "status": "FINISHED",
    "isAdult": False,
    "description": "The funny and beloved nursery teacher Deko-sensei and the children can't stop laughing about their everyday life at the nursery school! A manga based on a true story, full of laughter and tears, written with love by the author, a former nursery school teacher.",
    "season": None,
    "startDate": {"year": 2019, "month": 9, "day": 13},
    "endDate": {"year": 2023, "month": 6, "day": 14},
    "bannerImage": None,
    "coverImage": {
        "extraLarge": "https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx165992-Km0l45iMG89p.jpg",
        "large": "https://s4.anilist.co/file/anilistcdn/media/manga/cover/medium/bx165992-Km0l45iMG89p.jpg",
        "medium": "https://s4.anilist.co/file/anilistcdn/media/manga/cover/small/bx165992-Km0l45iMG89p.jpg",
        "color": None
    },
    "characters": {"edges": []},
    "studios": {"edges": []}
}

client.put_item(
    Item=item,
    TableName='AnimeTable'
)
