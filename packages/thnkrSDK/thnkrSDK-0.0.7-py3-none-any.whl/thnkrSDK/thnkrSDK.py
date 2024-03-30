import requests

BASE_URL = 'https://api.thnkrai.com/'
#BASE_URL = 'http://localhost:8000/'

def ping():
   response = requests.get(BASE_URL)
   return response.json()


def example(endpoint):
   response = requests.get(BASE_URL + endpoint)
   return response.json()


def predict(endpoint, input, username, password):
   headers = {
      'Content-Type': 'application/json',
   }

   payload = {
      **input,
      "Username": username,
      "Password": password,
   }

   response = requests.post(BASE_URL + endpoint, headers=headers, json=payload) # add error handling if anything other than response 200
   
   return response.json()