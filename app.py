from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "nexus_drive_secure_matrix_key"

# ==========================================================
# EXACT LOCAL MONGODB CONNECTION (Matched with your Compass)
# ==========================================================
client = MongoClient("mongodb://localhost:27017/")
db = client["nexus_drive_db"]  
bookings_collection = db["ride"]  # Connected directly to your 'ride' collection

# 15 Variant Fleet Data
FLEET_CATEGORIES = [
    {"id": "nx_01", "name": "Standard Moto", "type": "Economy", "rate": 1.0, "eta": "2 min", "icon": "bike", "desc": "Quick and affordable rides for your daily commute."},
    {"id": "nx_02", "name": "Priority Moto", "type": "Premium", "rate": 1.3, "eta": "1 min", "icon": "bike", "desc": "High-speed engine bikes for urgent travel."},
    {"id": "nx_03", "name": "Delivery Moto", "type": "Courier", "rate": 1.2, "eta": "4 min", "icon": "bike", "desc": "Safe handling for your packages and documents."},
    {"id": "nx_04", "name": "Mini Economy", "type": "Small Car", "rate": 1.8, "eta": "4 min", "icon": "car", "desc": "Budget-friendly travel in compact hatchbacks."},
    {"id": "nx_05", "name": "Comfort Eco", "type": "AC Hatchback", "rate": 2.2, "eta": "3 min", "icon": "car", "desc": "Stay cool with air conditioning at a low price."},
    {"id": "nx_06", "name": "Smart Drive", "type": "Compact", "rate": 2.0, "eta": "5 min", "icon": "car", "desc": "Modern compact cars for smooth urban navigation."},
    {"id": "nx_07", "name": "Standard Sedan", "type": "Comfort", "rate": 2.8, "eta": "5 min", "icon": "premium", "desc": "Spacious sedans perfect for family trips."},
    {"id": "nx_08", "name": "Business Class", "type": "Executive", "rate": 3.5, "eta": "4 min", "icon": "premium", "desc": "Premium vehicles for corporate and formal events."},
    {"id": "nx_09", "name": "Luxury Deluxe", "type": "VIP Sedan", "rate": 4.5, "eta": "6 min", "icon": "premium", "desc": "Top-tier comfort with high-end interior features."},
    {"id": "nx_10", "name": "Family SUV", "type": "Crossover", "rate": 4.0, "eta": "6 min", "icon": "suv", "desc": "Reliable 5-seater SUVs with extra luggage space."},
    {"id": "nx_11", "name": "Grand SUV", "type": "7-Seater", "rate": 5.2, "eta": "8 min", "icon": "suv", "desc": "Large vehicles for groups or big family outings."},
    {"id": "nx_12", "name": "Premium 4x4", "type": "Luxury SUV", "rate": 6.5, "eta": "7 min", "icon": "suv", "desc": "Powerful all-terrain vehicles for maximum safety."},
    {"id": "nx_13", "name": "Cargo Van", "type": "Loader", "rate": 3.0, "eta": "8 min", "icon": "van", "desc": "Designed for shifting furniture and heavy boxes."},
    {"id": "nx_14", "name": "Shuttle Van", "type": "12-Seater", "rate": 4.2, "eta": "9 min", "icon": "van", "desc": "Perfect for group picnics and team travel."},
    {"id": "nx_15", "name": "Executive Van", "type": "VIP Lounge", "rate": 7.5, "eta": "10 min", "icon": "van", "desc": "Ultra-luxury van with premium reclining seats."}
]

@app.route('/')
def home():
    return render_template('index.html', page='home', fleet=FLEET_CATEGORIES[:3])

@app.route('/fleet')
def fleet():
    return render_template('index.html', page='fleet', fleet=FLEET_CATEGORIES)

@app.route('/book', methods=['POST'])
def book_ride():
    vehicle_name = request.form.get('vehicle_name')
    rate = float(request.form.get('rate_per_km'))
    return render_template('index.html', page='confirm_booking', vehicle_name=vehicle_name, rate=rate)

@app.route('/confirm', methods=['POST'])
def confirm():
    try:
        passenger_name = request.form.get('passenger_name')
        passenger_phone = request.form.get('passenger_phone')
        pickup_location = request.form.get('pickup_location')
        drop_location = request.form.get('drop_location')
        vehicle_name = request.form.get('vehicle_name')
        user_bid = request.form.get('user_bid')
        payment_method = request.form.get('payment_method')

        booking_data = {
            "passenger_name": passenger_name,
            "passenger_phone": passenger_phone,
            "pickup_location": pickup_location,
            "drop_location": drop_location,
            "vehicle_name": vehicle_name,
            "final_fare": float(user_bid) if user_bid else 0.0,
            "payment_method": payment_method if payment_method else "Cash Terminal",
            "status": "Searching for Driver..."
        }
        
        # Injecting directly into 'ride' collection
        bookings_collection.insert_one(booking_data)
    except Exception as e:
        print(f"Database insertion failed: {e}")
        
    return redirect(url_for('terminal'))

@app.route('/terminal')
def terminal():
    # Fetch data from 'ride' collection to display on UI
    bookings = list(bookings_collection.find().sort("_id", -1))
    return render_template('index.html', page='terminal', bookings=bookings)

@app.route('/cancel/<booking_id>')
def cancel(booking_id):
    bookings_collection.delete_one({"_id": ObjectId(booking_id)})
    return redirect(url_for('terminal'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)