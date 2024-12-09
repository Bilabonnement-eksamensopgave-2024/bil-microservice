# Car Management Microservice

This microservice provides endpoints to manage cars in a system, including adding, updating, retrieving, and checking the availability of cars. It is designed to be a lightweight RESTful API with role-based access control.

## Features

- Add new cars to the system
- Retrieve details of individual cars or all cars
- Update car details (e.g., availability or kilometers driven)
- Delete cars from the system
- Check the availability of cars
- Health status monitoring of the microservice

## Endpoints

| **Path**                 | **Method** | **Description**                                    | **Response**                     | **Role Required** |
|--------------------------|------------|----------------------------------------------------|-----------------------------------|-------------------|
| `/cars`                  | POST       | Add a new car                                      | JSON object (success or error)   | Admin             |
| `/cars`                  | GET        | Retrieve a list of all cars                       | JSON array of car objects         | Admin             |
| `/cars/<int:id>`         | GET        | Retrieve details of a specific car by ID          | JSON object (car details)         | Admin             |
| `/cars/<int:id>`         | PATCH      | Update details of a specific car                  | JSON object (success or error)   | Admin             |
| `/cars/<int:id>`         | DELETE     | Delete a car by ID                                | JSON object (success or error)   | Admin             |
| `/cars/availability`     | GET        | Check the availability of all cars                | JSON array of available cars      | None              |
| `/health`                | GET        | Check the health status of the microservice       | JSON object (health status)       | None              |

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/car_microservice.git
   cd car_microservice


2. Create a virtual environment and activate it:
    ```bash
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Run the microservice:
    ```bash
    python app.py

5.Access the service at http://127.0.0.1:5000.



