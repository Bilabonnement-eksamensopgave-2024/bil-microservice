from flask import Flask, jsonify, request, make_response
import requests
import os
import auth
from dotenv import load_dotenv
from flasgger import swag_from
from datetime import datetime
from swagger.config import init_swagger
# from swagger.config import init_swagger
import cars
#from auth import role_required

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

init_swagger(app)
# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
BASE_ADMIN_URL = ""


# ----------------------------------------------------- GET /
@app.route('/', methods=['GET'])
def service_info():
    return jsonify({
        "service": "Car Management Microservice",
        "description": "This microservice handles car-related operations such as adding cars, retrieving car details, and managing availability.",
        "endpoints": [
            {
                "path": "/cars",
                "method": "POST",
                "description": "Add a new car to the system",
                "response": "JSON object with success or error message",
                "role_required": "admin"
            },
            {
                "path": "/cars",
                "method": "GET",
                "description": "Retrieve a list of all cars",
                "response": "JSON array of car objects",
                "role_required": "admin"
            },
            {
                "path": "/cars/<int:id>",
                "method": "GET",
                "description": "Retrieve details of a specific car by ID",
                "response": "JSON object with car details",
                "role_required": "admin"
            },
            {
                "path": "/cars/<int:id>",
                "method": "PATCH",
                "description": "Update details of a specific car (e.g., availability or kilometers driven)",
                "response": "JSON object with success or error message",
                "role_required": "admin"
            },
            {
                "path": "/cars/<int:id>",
                "method": "DELETE",
                "description": "Delete a car by ID",
                "response": "JSON object with success or error message",
                "role_required": "admin"
            },
            {
                "path": "/cars/availability",
                "method": "GET",
                "description": "Check the availability of all cars",
                "response": "JSON array of available cars",
                "role_required": "none"
            },
            {
                "path": "/health",
                "method": "GET",
                "description": "Check the health status of the microservice",
                "response": "JSON object indicating the health status",
                "role_required": "none"
            }
        ]
    })





#-------------------------- GET /cars 
@app.route('/cars', methods=['GET']) 
@swag_from('swagger/get_cars.yaml')
@auth.role_required('admin')
def cars_get():
    
    status, result = cars.get_cars()

    return jsonify(result), status


#-------------------------- GET /cars/available
@app.route('/cars/available', methods=['GET']) 
@swag_from('swagger/get_available_cars.yaml')
@auth.role_required('admin')
def available_cars_get():
    
    status, result = cars.get_available_cars()

    return jsonify(result), status



#-------------------------- GET /car/id
@app.route('/cars/<int:id>', methods=['GET'])
@swag_from('swagger/get_cars_by_id.yaml')
@auth.role_required('admin')
def get_car_by_id(id):
    status, result = cars.get_car_by_id(id)

    return jsonify(result), status


#--------------------------- PATCH /car/id
@app.route('/cars/<int:id>', methods=['PATCH'])
@swag_from('swagger/patch_car.yaml')
@auth.role_required('admin')
def patch_car(id):    
    data = request.json
    
    status, result = cars.update_car(id, data)

    return jsonify(result), status



#-------------------------- POST /cars
@app.route('/cars', methods=['POST'])
@swag_from('swagger/post_car.yaml')
@auth.role_required('admin')
def post_cars():
    data = request.json

    if not data:
        return jsonify({"message": "No data provided"}), 400

    try:
        car_item = _data_to_cars_dict(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    result = cars.add_car(car_item)
    return jsonify(result[1]), result[0]


#------------------------- DELETE /cars
@app.route('/cars/<int:id>', methods=['DELETE'])
@auth.role_required('admin')
@swag_from('swagger/delete_car.yaml')
def delete_car(id):
    status, result = cars.delete_car_by_id(id)
    return jsonify(result), status



# ----------------------------------------------------- GET /health
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200











def _data_to_cars_dict(data):
    """
    Validate input data and transform it into a dictionary compatible with the database schema.
    """
    try:
        # Validate required fields
        required_fields = ['car_brand', 'fuel_type', 'purchase_date', 'purchase_price']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Missing required field: {field}")

        # Validate purchase_date format
        try:
            purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Invalid date format for 'purchase_date'. Expected format: YYYY-MM-DD")

        # Validate optional fields and set defaults
        return {
            "car_id": data.get('car_id'),  # Allow null for auto-increment
            "car_brand": data['car_brand'],
            "car_type": data.get('car_type', None), #None is Null in sqlite
            "fuel_type": data['fuel_type'],
            "purchase_date": purchase_date,  # Store date in ISO 8601 format
            "purchase_price": int(data['purchase_price']),
            "km_driven_since_last_end_subscription": data.get('km_driven_since_last_end_subscription', 0),
            "is_available": bool(data.get('is_available', True))  # Default to True if not provided
        }
    except Exception as e:
        raise ValueError(str(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5002)))