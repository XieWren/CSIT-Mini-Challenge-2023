# import third-party libraries
from pymongo.database import Database
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

# import local Python libraries
#

# import Python's standard libraries
import datetime

def getMongoCollection(name: str):
    client: MongoClient = AsyncIOMotorClient("mongodb+srv://userReadOnly:7ZT817O8ejDfhnBM@minichallenge.q4nve1r.mongodb.net/")
    db: Database= client["minichallenge"]
    return db.get_collection(name=name)


def dateToDatetime(date: datetime.date):
    return datetime.datetime(date.year, date.month, date.day)


def datesValidated(dates: list[datetime.datetime]):
    for index, date in enumerate(dates[:-1]):
        nextDate = dates[index + 1]
        if (nextDate - date).days != 1:
            return False
    return True