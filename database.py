from pymongo import MongoClient
from bson.objectid import ObjectId

def get_db_connection():
    # Local MongoDB Server Configuration
    client = MongoClient('mongodb://localhost:27017/')
    db = client['velocity_db']
    return db

def insert_ride_booking(booking_obj):
    db = get_db_connection()
    return db.bookings.insert_one(booking_obj)

def get_user_bookings():
    db = get_db_connection()
    # Fetching latest bookings first
    return list(db.bookings.find().sort('_id', -1))

def cancel_booking(booking_id):
    db = get_db_connection()
    db.bookings.delete_one({"_id": ObjectId(booking_id)})