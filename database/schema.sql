CREATE DATABASE IF NOT EXISTS railway_management;

USE railway_management;


CREATE TABLE trains (
    train_id INT AUTO_INCREMENT PRIMARY KEY,
    train_number VARCHAR(10) UNIQUE NOT NULL,
    train_name VARCHAR(100) NOT NULL,
    source VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    total_seats INT NOT NULL,
    fare DECIMAL(10,2) NOT NULL
);



CREATE TABLE passengers (
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15)
);




CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_id INT NOT NULL,
    train_id INT NOT NULL,
    journey_date DATE NOT NULL,
    seat_number INT NOT NULL,
    booking_status VARCHAR(20) DEFAULT 'CONFIRMED',
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (passenger_id)
        REFERENCES passengers(passenger_id),

    FOREIGN KEY (train_id)
        REFERENCES trains(train_id),

    UNIQUE (train_id, journey_date, seat_number)
);




CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL UNIQUE,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(30),
    payment_status VARCHAR(20) DEFAULT 'PENDING',
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (booking_id)
        REFERENCES bookings(booking_id)
);