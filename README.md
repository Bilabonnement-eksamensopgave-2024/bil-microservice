# Car Management Microservice

## Overview

The Car Microservice is responsible for handling car-related operations such as adding cars, retrieving car details, and managing the availability of cars. It provides a simple API for interacting with the car database.

### Domain Model
The domain model of this service revolves around a `Car` entity with the following attributes:

``` mermaid
classDiagram
  class cars {
        Int car_id
        String car_brand
        String car_model
        String fuel_type
        Date registration_date
        Int purchase_price
        Int km_driven_since_last_end_subscription
        Boolean is_available
        get_cars() List
        get_available_cars() List
        get_car_by_id(car_id: Int) Dict
        update_car(updated_car: Dict) String
        delete_car(car_id: Int) String
        add_car(new_car: Dict) String
    }
```

- `car_id`: Unique identifier for the car (auto-incremented).
- `car_brand`: Brand of the car (e.g., Toyota, Ford).
- `car_type`: Type of the car (optional).
- `fuel_type`: Type of fuel used (e.g., Petrol, Diesel, Electric).
- `purchase_date`: Date when the car was purchased.
- `purchase_price`: The price at which the car was purchased.
- `km_driven_since_last_end_subscription`: The kilometers driven since the car's last maintenance.
- `is_available`: Availability status of the car (true or false).

This service follows a microservice architecture, where it operates independently while being able to interact with other services in the overall application.

## Architecture Diagram
*(Insert Architecture Diagram here)*

## Features

- **Add Car**: Ability to add a new car to the system.
- **Retrieve Cars**: Retrieve a list of all cars in the system.
- **Retrieve Car by ID**: Get detailed information of a specific car by its ID.
- **Update Car**: Update the details of a specific car.
- **Delete Car**: Delete a car from the system.
- **Check Availability**: Check the availability status of all cars.

### JWT Authentication
The service uses JWT for securing API endpoints, ensuring only authorized users can perform sensitive operations like adding, updating, or deleting cars.

## Database Structure

The database used by this microservice is an SQLite3 database with a table `cars` that holds the following fields:

| Field                                      | Type        | Description                                        |
|--------------------------------------------|-------------|----------------------------------------------------|
| `car_id`                                   | INTEGER     | Primary Key (auto-incremented)                     |
| `car_brand`                                | TEXT        | Brand of the car                                   |
| `car_type`                                 | TEXT        | Type of the car (optional)                         |
| `fuel_type`                                | TEXT        | Fuel type used by the car                          |
| `purchase_date`                            | DATE        | Date of purchase                                   |
| `purchase_price`                           | INTEGER     | Purchase price of the car                          |
| `km_driven_since_last_end_subscription`    | INTEGER     | Kilometers driven since the last maintenance       |
| `is_available`                             | BOOLEAN     | Availability status of the car (true or false)     |

## Technology Stack

- **Programming Language**: Python
- **Framework**: Flask
- **Database**: SQLite3
- **API Documentation**: Swagger/OpenAPI
- **Deployment**: Azure Web App (using Docker container)
- **CI/CD**: GitHub Actions

## Environment Variables

The following environment variables are required for the service:

| Environment Variable | Description                                      |
|----------------------|--------------------------------------------------|
| `SECRET_KEY`         | Secret key used for JWT authentication.          |
| `DB_PATH`            | Path to the SQLite3 database file.               |
| `PORT`               | Port the Flask app will run on (default 5002).    |

## Endpoints

### Base URL

- **Local**: http://localhost:5002
- **Production (Azure)**: `<Azure App URL>`

### Endpoint Documentation

| Method | Endpoint                  | Description                                       | Request Body     | Response Codes             | Role Required    |
|--------|---------------------------|---------------------------------------------------|------------------|----------------------------|------------------|
| GET    | `/api/v1/cars`             | Retrieve all cars                                 | N/A              | 200, 204, 404, 500         | Admin            |
| POST   | `/api/v1/cars`             | Create a new car                                  | JSON payload     | 200, 204, 404, 500         | Admin            |
| GET    | `/api/v1/cars/<int:id>`    | Retrieve a car by ID                              | N/A              | 200, 204, 404, 500         | Admin            |
| PATCH  | `/api/v1/cars/<int:id>`    | Update a car's details                            | JSON payload     | 200, 204, 404, 500         | Admin            |
| DELETE | `/api/v1/cars/<int:id>`    | Delete a car by ID                                | N/A              | 200, 204, 404, 500         | Admin            |
| GET    | `/api/v1/cars/available`   | Retrieve all available cars                       | N/A              | 200, 204, 404, 500         | Sales, Admin     |
| GET    | `/api/v1/health`           | Check health status of the microservice           | N/A              | 200                        | None             |

### Swagger Documentation

Swagger UI for API documentation is available at:  
`<Base URL>/docs`

