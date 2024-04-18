-- create project schema
DROP SCHEMA IF EXISTS FIS;
CREATE SCHEMA IF NOT EXISTS FIS DEFAULT CHARACTER SET utf8 ;
USE FIS;

-- 创建 AIRPORT 表
CREATE TABLE AIRPORT (
    AirportID VARCHAR(255) PRIMARY KEY,
    AirportCity VARCHAR(255),
    TimeZone VARCHAR(255),
    Type VARCHAR(255)
);

-- 创建 AIRLINE 表
CREATE TABLE AIRLINE (
    IATACode VARCHAR(255) PRIMARY KEY,
    Headquarters VARCHAR(255),
    Alliance VARCHAR(255),
    FoundingYear VARCHAR(255)
);

-- 创建 PLANE 表
CREATE TABLE PLANE (
    PlaneID VARCHAR(255) PRIMARY KEY,
    PlaneModel VARCHAR(255),
    Capacity INT,
    RegistrationCountryCode VARCHAR(255),
    Age INT,
    CurrentOperator VARCHAR(255),
    FOREIGN KEY (CurrentOperator) REFERENCES AIRLINE(IATACode)
);

-- 创建 PASSENGER 表
CREATE TABLE PASSENGER (
    PassengerID INT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Gender CHAR(1),
    Age INT,
    NationalityCode VARCHAR(255)
);

-- 创建 FLIGHT 表
CREATE TABLE FLIGHT (
    FlightID VARCHAR(255) PRIMARY KEY,
    DepartureAirportID VARCHAR(255),
    ArrivalAirportID VARCHAR(255),
    FlightStatus VARCHAR(255),
    PlaneID VARCHAR(255),
    ScheduledDeparture VARCHAR(255),
    ActualDeparture VARCHAR(255),
    ScheduledArrival VARCHAR(255),
    ActualArrival VARCHAR(255),
    FOREIGN KEY (DepartureAirportID) REFERENCES AIRPORT(AirportID),
    FOREIGN KEY (ArrivalAirportID) REFERENCES AIRPORT(AirportID),
    FOREIGN KEY (PlaneID) REFERENCES PLANE(PlaneID)
);

-- 创建 BOOKING 表
CREATE TABLE BOOKING (
    BookingID INT PRIMARY KEY,
    PassengerID INT,
    FlightID VARCHAR(255),
    BookingDate VARCHAR(255),
    SeatID VARCHAR(255),
    FOREIGN KEY (PassengerID) REFERENCES PASSENGER(PassengerID),
    FOREIGN KEY (FlightID) REFERENCES FLIGHT(FlightID)
);
