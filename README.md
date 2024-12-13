# Car Management Microservice

## Table of Contents
- [Overview](#overview)
- [Core Functionalities](#core-functionalities)
  - [Features](#features)
  - [CRUD Operations](#crud-operations)
  - [JWT Authentication](#jwt-authentication)
  - [Token Validation](#token-validation)
- [Domain Model](#domain-model)
- [Technology Stack](#technology-stack)
- [Environment Variables](#environment-variables)
- [Endpoints](#endpoints)
  - [Base URL](#base-url)
  - [Endpoint Documentation](#endpoint-documentation)
- [Swagger Documentation](#swagger-documentation)

## Overview

The Car Management Microservice is responsible for handling car-related operations such as adding cars, retrieving car details, and managing the availability of cars. It provides a simple API for interacting with the car database. 
It is designed as part of a microservice architecture, enabling independent development, deployment, and scaling. The Car Management Microservice interacts with other services in the system to provide a seamless experience within the overall application.

## Core Functionalities

### Features

- **Add Car**: Ability to add a new car to the system.
- **Retrieve Cars**: Retrieve a list of all cars in the system.
- **Retrieve Car by ID**: Get detailed information of a specific car by its ID.
- **Update Car**: Update the details of a specific car.
- **Delete Car**: Delete a car from the system.
- **Check Availability**: Check the availability status of all cars.

### CRUD Operations
- **Create**: Add new cars to the database.
- **Read**: Retrieve all cars, specific car details, or available cars.
- **Update**: Modify details of an existing car (e.g., kilometers driven, availability).
- **Delete**: Remove cars from the database by their ID.

### JWT Authentication
JWTs are used for secure access to endpoints. Each JWT includes a role claim that determines the user's permissions:

- **Admin**: Access to all endpoints, including adding, updating, and deleting cars.
- **Maintenance**: Access to read and update car details.
- **Sales**: Access to view available cars.

### Token Validation
1. Tokens are validated for authenticity.
2. Roles are verified before granting access to protected endpoints.

## Domain Model
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
        get_cars() : List
        get_available_cars() : List
        get_car_by_id(id : Int) : Dict  
        update_car(id : Int, data : Any) : String
        delete_car_by_id(id : Int) : String
        add_car(new_car : Dict) : String
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
| `SECRET_KEY`         | Secret key used for the application.             |
| `DB_PATH`            | Path to the SQLite3 database file.               |

## Endpoints

### Base URL

- **Local**: [Localhost URL](http://localhost:5002) 
- **Production (Azure)**: [Azure URL](https://https://car-microservice-ayhzdgdrfxgrdgby.northeurope-01.azurewebsites.net)

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
[Swagger URL](https://https://car-microservice-ayhzdgdrfxgrdgby.northeurope-01.azurewebsites.net/docs)

