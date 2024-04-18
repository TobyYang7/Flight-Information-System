import openai
import random
from retrying import retry


'''
User Interface: get_flight_info, get_airport_info
Admin Interface: operate_db

LLM Interface: use the output of the user or admin interface to generate the next input.
'''


def get_flight_info(flight_code):
    # todo
    '''
    Input:
        flight_code: string, flight number
    Output:
        json, All the information of the flight with the given flight number.
    '''
    pass


def get_airport_info(airport_code):
    # todo
    '''
    Input:
        airport_code: string, IATA code
    Output:
        json, All the information of the airport with the given IATA code.
    '''
    pass


def operate_db(code):
    # todo
    '''
    Input:
        code: string, sql code
    Output:
        Include four operations: insert, delete, update, query
        Each operation will directly return the result(or status) of the operation.
    '''
    pass


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
