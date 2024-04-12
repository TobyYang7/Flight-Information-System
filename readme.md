# Flight Information System

## Group Members

Yuzhe Yang: <121090684@link.cuhk.edu.cn>
Zitong Wang: <121090530@link.cuhk.edu.cn>
Baoyin Zhang: <121090761@link.cuhk.edu.cn>
Haoqi Zhang: <121090766@link.cuhk.edu.cn>
Jianzhen Chen: <121090036@link.cuhk.edu.cn>
Zhidong Peng: <121090448@link.cuhk.edu.cn>

## Dataset

From United States Department of Transportation: <https://www.transtats.bts.gov/DataIndex.asp>
From Kaggle: <https://www.kaggle.com/datasets/iamsouravbanerjee/airline-dataset>

## Some useful links

<https://github.com/fuzhengwei/CodeGuide/blob/50a1d68e4038d8f0eee966e49d65d74926676ad4/docs/md/road-map/mysql.md?plain=1#L119>
<https://github.com/dongmingli-Ben/CSC3170-Database-NBA>

## Environment

linux x86_64

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
