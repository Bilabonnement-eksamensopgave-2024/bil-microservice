from flask import Flask, jsonify, request, make_response
import requests
import os
from dotenv import load_dotenv
from flasgger import swag_from
from datetime import datetime
# from swagger.config import init_swagger
import cars
#from auth import role_required

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
BASE_ADMIN_URL = ""

# Initialize Swagger
#init_swagger(app)


#-------------------------- GET /cars 
@app.route('/cars', methods=['GET']) 
#@swag_from('swagger/get_cars.yaml') #TODO
#@role_required('user') # TODO UPDATE LATER
def cars_get():
    
    status, result = cars.get_cars()

    return jsonify(result), status


#-------------------------- GET /cars/avaliable
@app.route('/cars/avaliable', methods=['GET']) 
#@swag_from('swagger/get_cars.yaml') #TODO
#@role_required('user') # TODO UPDATE LATER
def avaliable_cars_get():
    
    status, result = cars.get_available_cars()

    return jsonify(result), status



#-------------------------- GET /car/id
@app.route('/cars/<int:id>', methods=['GET'])
#@swag_from('swagger/get_damage_type_by_id.yaml')
#@role_required('user') # TODO UPDATE LATER
def get_car_by_id(id):
    status, result = cars.get_car_by_id(id)

    return jsonify(result), status


#--------------------------- PATCH /car/id
@app.route('/cars/<int:id>', methods=['PATCH'])
#@swag_from('swagger/get_damage_type_by_id.yaml')
#@role_required('user') # TODO UPDATE LATER
def patch_car(id):    
    data = request.json
    
    status, result = cars.update_car(id, data)

    return jsonify(result), status



#-------------------------- POST /cars
@app.route('/cars', methods=['POST'])
#@swag_from('swagger/post_subscriptions.yaml') #TODO
#@role_required('user') # TODO UPDATE LATER
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
            "is_avaliable": bool(data.get('is_avaliable', True))  # Default to True if not provided
        }
    except Exception as e:
        raise ValueError(str(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5002)))