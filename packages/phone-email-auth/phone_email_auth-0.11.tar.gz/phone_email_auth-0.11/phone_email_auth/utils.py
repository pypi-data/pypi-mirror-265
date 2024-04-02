from django.shortcuts import render
# Create your views here.
import requests

def get_verified_phone(CLIENT_ID,ACCESS_TOKEN):

    url = "https://eapi.phone.email/getuser"
    if not CLIENT_ID or not ACCESS_TOKEN:
        raise ValueError("Client ID and Access Token must be set")

    postData = {
        'client_id': CLIENT_ID,
        'access_token': ACCESS_TOKEN
    }

    response = requests.post(url, data=postData, verify=True) 

    if response.status_code != 200:
        print("Error:", response.text)
        exit()

    json_data = response.json()
    if json_data['status'] != 200:
            print("Error:")
            exit()

    country_code = json_data['country_code']
    phone_no = json_data['phone_no']
    ph_email_jwt = json_data['ph_email_jwt']

    print(country_code+phone_no)
    return (country_code, phone_no)