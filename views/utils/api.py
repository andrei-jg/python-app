import requests
import json

url = 'https://andrei00.pythonanywhere.com/api/'

def send_uri(method: str, payload: dict, uri: str) -> dict:

    methods = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put
    }

    response = methods[method](url + uri, json=payload)
    status_code = response.status_code

    decoded_response = json.loads(response.content.decode('utf-8'))
    decoded_response['status_code'] = status_code

    return decoded_response

if __name__ == "__main__":

    data = {
    "email": "a.jimenezgr@gmail.com",
    "password": "Mexico.1"
    }


    print(send_uri(method='POST', payload=data, uri='login'))