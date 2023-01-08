import pymongo
from pathlib import Path
from dotenv import dotenv_values

dotenv_path = Path('.env')
if dotenv_path:
    config = dotenv_values(dotenv_path)
    mongo = pymongo.MongoClient(
        host=config['MONGO_SERVER'],
        port=int(config['MONGO_PORT']),
        username=config['MONGO_USERNAME'],
        password=config['MONGO_PASSWORD'],
        serverSelectionTimeoutMS=1000
    )
    # db - Webtronics
    db = mongo[config['MONGO_DATABASE']]
else:
    print("Don't start server - .env not exists")
    exit()
