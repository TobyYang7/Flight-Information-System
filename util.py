import openai
import random
from retrying import retry
import json
import mysql.connector

prompt = '''
-- create project schema
DROP SCHEMA IF EXISTS FIS;
CREATE SCHEMA IF NOT EXISTS FIS DEFAULT CHARACTER SET utf8;
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
这个是我的数据库relation schema，你可以根据这个来查询你想要的信息，请注意日期格式应该为MM-DD-YYYY或者MM-DD-YYYY-HH-MM。
如果你要输出sql代码，你应该严格按照markdown的形式输出，
例如```sql <你修改之后的代码>```
'''


'''
User Interface: get_flight_info, get_airport_info
Admin Interface: operate_db

LLM Interface: use the output of the user or admin interface to generate the next input.
'''


def prepare_cursor():
    with open('database/fis_config.json') as f:
        config = json.load(f)
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    return cursor, cnx


def format_data(fields, result):
    field = []
    for i in fields:
        field.append(i[0])
    ret = ""
    for iter in result:
        line_data = ""
        for i in range(len(field)):
            line_data += f"{field[i]}: {iter[i]}\n"
        ret += line_data + "\n"
    return ret.rstrip('\n')


def get_flight_info(flight_code):
    '''
    Input:
        flight_code: string, flight number
    Output:
        json, All the information of the flight with the given flight number.
    '''
    try:
        cursor, _ = prepare_cursor()
        cursor.execute(f"SELECT * FROM flight WHERE FlightID='{flight_code}'")
        result = cursor.fetchall()
        fields = cursor.description
        ret = format_data(fields, result)
        return ret

    except Exception as e:
        return f"Error"

    finally:
        if 'cursor' in locals():
            cursor.close()


def get_airport_info(airport_code):
    '''
    Input:
        airport_code: string, IATA code
    Output:
        json, All the information of the airport with the given IATA code.
    '''
    try:
        cursor, _ = prepare_cursor()
        cursor.execute(f"SELECT * FROM airport WHERE AirportID='{airport_code}'")
        result = cursor.fetchall()
        fields = cursor.description
        ret = format_data(fields, result)
        return ret

    except Exception as e:
        return f"Error"

    finally:
        if 'cursor' in locals():
            cursor.close()


def operate_db(code):
    '''
    Input:
        code: string, sql code
    Output:
        Include four operations: insert, delete, update, query
        Each operation will directly return the result(or status) of the operation.
    '''

    try:
        cursor, cnx = prepare_cursor()
        cursor.execute(code)
        if code.lower().startswith("select"):
            result = cursor.fetchall()
            fields = cursor.description
            ret = format_data(fields, result)
            ret += "\n\n" + f"{cursor.rowcount} row(s) returned"
            return ret
        try:
            cnx.commit()
        except Exception as e:
            cnx.rollback()
            return f"Failed to operate: {e}"
        result = f"{cursor.rowcount} row(s) affected, {cursor.warning_count} warning(s)"
        return result

    except Exception as e:
        return f"Failed to operate: {e}"

    finally:
        if 'cursor' in locals():
            cursor.close()


# todo: change your own api base url and config the api key
openai.api_base = "https://api.ai-gaochao.cn/v1"


class OpenAIGPT:
    def __init__(self, model_name="gpt-3.5-turbo", keys_path="apikey.txt"):
        self.model_name = model_name
        with open(keys_path, encoding="utf-8", mode="r") as fr:
            self.keys = [line.strip() for line in fr if len(line.strip()) >= 4]

    def __post_process(self, response):
        return response["choices"][0]["message"]["content"]

    @retry(wait_fixed=300, stop_max_attempt_number=50)
    def __call__(self, message):
        if message is None or message == "":
            return False, "Your input is empty."

        # current_key = random.choice(self.keys)
        current_key = self.keys[0] if len(self.keys) == 1 else random.choice(self.keys)
        openai.api_key = current_key
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": message}],
            temperature=0.3,
            top_p=0.1,
            frequency_penalty=0.6,
            presence_penalty=0.6,
            n=1,
        )
        return self.__post_process(response)

# print(get_flight_info("AA0164051723"))
