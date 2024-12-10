from datetime import datetime
from dotenv import load_dotenv
import os
import sqlite3

# Load environment variables from .env file
load_dotenv()
DB_PATH = os.getenv('DB_PATH', "cars.db")
TABLE_NAME = "cars"

def create_table(): 
    with sqlite3.connect(DB_PATH) as conn: 
        cur = conn.cursor() 
        cur.execute(
            f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} 
            (
                car_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                car_brand TEXT, 
                car_type TEXT DEFAULT NULL, 
                fuel_type TEXT, 
                purchase_date DATE, 
                purchase_price INTEGER,
                km_driven_since_last_end_subscription INTEGER,
                is_available BOOLEAN DEFAULT TRUE
            )'''
        )
create_table()


def get_cars():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
            cur.execute(f'SELECT * FROM {TABLE_NAME}')
            data = cur.fetchall()
            
            if not data:
                return [404, {"message": "Cars not found"}]
                    
            return [200, [dict(row) for row in data]]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]
    


def get_available_cars():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
            cur.execute(f'''SELECT * FROM {TABLE_NAME} 
                        WHERE is_available = 1''')
            data = cur.fetchall()
            
            if not data:
                return [404, {"message": "No available cars found"}]
                    
            return [200, [dict(row) for row in data]]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]
    

def get_car_by_id(id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
            cur.execute(f'SELECT * FROM {TABLE_NAME} WHERE car_id = ?', (id,))
            data = cur.fetchone()
            
            if not data:
                return [404, {"message": "Car not found by id"}]
                    
            return [200, dict(data)]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]


def update_car(id, data):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            
            query = f'''
            UPDATE {TABLE_NAME}
            SET '''

            i = 0
            for key,value in data.items():
                if key not in query:
                    if i > 0:
                        query+= ", "

                    if isinstance(value, str):
                        query += f'{key} = "{value}"'
                    else:
                        query += f'{key} = {value}'
                    i += 1

            query += f" WHERE car_id = {id}"
            print(query)

            cur.execute(query)
            if cur.rowcount == 0:
                return [404, {"message": "Car not found."}]
            
            return [201, {"message": "Car updated successfully."}]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]



def delete_car_by_id(id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()

            # Delete the row with the specified id
            cur.execute(f'DELETE FROM {TABLE_NAME} WHERE car_id = ?', (id,))
            
            if cur.rowcount == 0:
                return [404, {"message": "Car not found."}]
            
            return [200, {"message": f"Car deleted from {TABLE_NAME} successfully."}]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]




def add_car(data):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            
            cur.execute(
                f''' INSERT OR IGNORE INTO {TABLE_NAME} 
                ( 
                    car_id, 
                    car_brand, 
                    car_type, 
                    fuel_type,
                    purchase_date,
                    purchase_price,
                    km_driven_since_last_end_subscription,
                    is_available
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ''', 
                (
                    data.get('car_id'), 
                    data.get('car_brand'), 
                    data.get('car_type'), 
                    data.get('fuel_type'), 
                    data.get('purchase_date'), 
                    data.get('purchase_price'), 
                    data.get('km_driven_since_last_end_subscription'), 
                    data.get('is_available')
                )
            )

        return [201, {"message": "New car added to database"}]

    except sqlite3.Error as e:
        return [500, {"error": str(e)}]