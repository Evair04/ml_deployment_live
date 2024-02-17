import requests

# teste 1 - hello world

response = requests.get('http://localhost:8000/hello_world')

print(response.json())

if response.status_code == 200:
    response_data = response.json()
    print("response_data: ", response_data)
else:
    print("Error: ", response.status_code)