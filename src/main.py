# import third-party libraries
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
import pymongo
import uvicorn

# import local Python libraries
from helpers import (
    datesValidated,
    dateToDatetime,
    getMongoCollection,
)

# import Python"s standard libraries
import datetime

DEBUG_MODE = False
app = FastAPI(debug=DEBUG_MODE)

# Force error 400 instead of 422
@app.exception_handler(RequestValidationError)
async def validationExceptionHandler(request: Request, exc: RequestValidationError):
    return ORJSONResponse(
        content=exc.errors(),
        status_code=400,
    )

@app.get("/flight")
async def flight(
    departureDate: datetime.date,
    returnDate: datetime.date,
    destination: str,
):
    if departureDate > returnDate:
        raise HTTPException(
            status_code=400,
            detail=f"Departure date {departureDate} should be before return date {returnDate}",
        )

    col = getMongoCollection("flights")
    cursor = col.aggregate([
        {"$match": {
            "$or": [{
                "srccity": "Singapore", 
                "destcity": destination, 
                "date": dateToDatetime(departureDate),
            }, {
                "srccity": destination, 
                "destcity": "Singapore", 
                "date": dateToDatetime(returnDate)
            }]}
        }, 
        {"$sort": {"date": 1}},
        {"$group": {
            "_id": "$airlinename", 
            "prices": {"$push": "$price"}, 
            "total": {"$sum": "$price"}
        }}, 
        {"$sort": {"total": 1}}, 
    ])

    returnFlights = []
    while cursor.alive:
        async for flight in cursor:
            if returnFlights and \
            (returnFlights[0]["Departure Price"] + returnFlights[0]["Return Price"]) != flight["total"]:
                await cursor.close()
                break

            returnFlights.append({
                "City": destination,
                "Departure Date": departureDate,
                "Departure Airline": flight["_id"],
                "Departure Price": flight["prices"][0],
                "Return Date": returnDate,
                "Return Airline": flight["_id"],
                "Return Price": flight["prices"][1],
            })

        if cursor.alive:
            await cursor.next()

    return returnFlights

@app.get("/hotel")
async def hotel(
    checkInDate: datetime.date,
    checkOutDate: datetime.date,
    destination: str,
):
    if checkInDate > checkOutDate:
        raise HTTPException(
            status_code=400,
            detail=f"Check-In date {checkInDate} should be before Check-Out date {checkOutDate}",
        )

    checkInDate = dateToDatetime(checkInDate)
    checkOutDate = dateToDatetime(checkOutDate)

    col = getMongoCollection("hotels")
    cursor = col.aggregate([
        # Get all hotels with existing range 
        {"$match": {
            "city": destination, 
            "$and": [
                {"date": {"$gte": checkInDate}},
                {"date": {"$lte": checkOutDate}},
            ]
        }}, 
        {"$sort": {"date": pymongo.ASCENDING}},
        {"$group": {
            "_id": "$hotelName", 
            "dates": {"$push": "$date"}, 
            "total": {"$sum": "$price"},
        }},
        {"$sort": {"total": pymongo.ASCENDING}},
    ])

    hotels = []
    while cursor.alive:
        async for hotelFee in cursor:
            if hotels and hotels[0]["Price"] != hotelFee["total"]:
                await cursor.close()
                break

            if (
                hotelFee["dates"][0] != checkInDate or 
                hotelFee["dates"][-1] != checkOutDate or
                not datesValidated(hotelFee["dates"])
            ):
                continue

            hotels.append({
                "City": destination,
                "Check In Date": checkInDate.date(),
                "Check Out Date": checkOutDate.date(),
                "Hotel": hotelFee["_id"],
                "Price": hotelFee["total"],
            })
        
        if cursor.alive:
            await cursor.next()
    
    return hotels

if __name__ == "__main__":
    config = {
        "app": "main:app",
        "host": "0.0.0.0",
        "log_level": "debug",
        "reload": True,
    } if DEBUG_MODE else {"app": app, "host": "0.0.0.0"} 
    uvicorn.run(port=8080, **config)