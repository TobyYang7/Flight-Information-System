# Flight Information System

## Group Members

- Yuzhe Yang: <121090684@link.cuhk.edu.cn>
- Zitong Wang: <121090530@link.cuhk.edu.cn>
- Baoyin Zhang: <121090761@link.cuhk.edu.cn>
- Haoqi Zhang: <121090766@link.cuhk.edu.cn>
- Jianzhen Chen: <121090036@link.cuhk.edu.cn>
- Zhidong Peng: <121090448@link.cuhk.edu.cn>

## Dataset

From United States Department of Transportation: <https://www.transtats.bts.gov/DataIndex.asp>

From Kaggle: <https://www.kaggle.com/datasets/iamsouravbanerjee/airline-dataset>

## ER diagram

```mermaid
erDiagram
    PASSENGER ||--o{ FLIGHT : books
    FLIGHT ||--|| AIRPORT : departs
    FLIGHT ||--|| AIRPORT : arrives
    FLIGHT ||--|| PLANE : uses
    AIRLINE ||--o{ FLIGHT : operates
    FLIGHT ||--|| FLIGHT-SCHEDULE : scheduled

    PASSENGER {
        int PassengerID PK "Unique identifier"
        string FirstName "First name"
        string LastName "Last name"
        char Gender "Gender"
        int Age "Age"
        string Nationality "Nationality"
    }

    AIRPORT {
        string AirportName PK "Name of the airport"
        char AirportCountryCode "Country code"
        string CountryName "Country name"
        string AirportContinent "Continent"
    }

    PLANE {
        int PlaneID PK "Unique identifier"
        string PlaneModel "Model"
        int Capacity "Capacity"
    }

    FLIGHT {
        int FlightID PK "Unique identifier"
        string DepartureAirport FK "Departure airport"
        string ArrivalAirport FK "Arrival airport"
        date DepartureDate "Departure date"
        string FlightStatus "Status"
        int PlaneID FK "Plane used"
        int AirlineID FK "Operated by"
    }

    AIRLINE {
        int AirlineID PK "Unique identifier"
        string AirlineName "Name"
        string Headquarters "Headquarters"
    }

    FLIGHT-SCHEDULE {
        int FlightID FK "Flight"
        datetime ScheduledDeparture "Scheduled departure"
        datetime ActualDeparture "Actual departure"
        datetime ScheduledArrival "Scheduled arrival"
        datetime ActualArrival "Actual arrival"
    }
```

## How to run this project

```bash
# install dependencies
pip install -r requirements.txt

# run the app
python app.py

```

Then open your browser and visit <http://127.0.0.1:5000/>

There are two types of ways to interact with the database:

|        | ID | Password | Interaction|
| ------ | --- | ----------- |----------------|
| Admin  | admin   | admin1234     |add, delete, update, and query the data|
| User   | user   | user1234     |only query the data|

If you cannot find the interface, please check whether the database is running.

## LLM interface

User can use this interface to query the flight information by using natural language.
