import requests
from pydantic import BaseModel, ValidationError, validator

class SMSModel(BaseModel):
    source_number: str
    destination_number: str
    message: str

    @validator('destination_number')
    def validate_destination_number(cls, v):
        if not v.isdigit():
            raise ValueError('Destination number must contain only digits')
        if len(v) < 10 or len(v) > 15:
            raise ValueError('Destination number length must be between 10 and 15 digits')
        return v

    @validator('message')
    def validate_message_length(cls, v):
        if len(v) > 100:
            raise ValueError('Message must not exceed 100 characters')
        return v

class Chromastone:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.base_url = 'https://chromastone-production.up.railway.app'
        
    
    def check_balance(self) -> str:
        '''this function will be used to check the balance of the user, it will return the balance as a string,'''


        full_url = self.base_url + '/check_balance'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        try:
            res = requests.post(url=full_url, headers=headers, json={'api_key': self.api_key})
            if res.status_code != 200:
                print('Failed to check balance, check your api key or internet. Status code:', res.status_code)
                return 'Failed to check balance, check your api key or internet connection'
            self.balance = res.json()['balance']
            return str(self.balance)
        except Exception as e:
            return e

    def buy_sms(self, amount: int) -> None:
        '''this function will be used to buy more sms but it is not implemented yet,'''

        return 'This function is not implemented yet'
        

    def send_sms(self, source_number: str, destination_number: str, message: str):
        full_url = self.base_url + '/send_sms'
        headers = {'Authorization': f'Bearer {self.api_key}',
                   'Content-Type': 'application/json'}
        # check if the user has enough balance to send the SMS
        balance = self.check_balance()
        if balance == 'Failed to check balance, check your api key or internet connection':
            raise Exception('Failed to check balance, check your api key or internet connection')
        else:
            balance = int(balance)
        if balance > 0:
            try:
                sms = SMSModel(source_number=source_number, destination_number=destination_number, message=message)
                response = requests.post(url=full_url, json=sms.model_dump_json(), headers=headers)
                if response.status_code == 200:
                    print('SMS sent successfully, remaining balance:', response.json()['balance'])
                    return 'SMS sent successfully'
                else:
                    print('Failed to send SMS, status code:', response.status_code)
                    return 'Failed to send SMS'
            except ValidationError as e:
                print(e.json())
    


