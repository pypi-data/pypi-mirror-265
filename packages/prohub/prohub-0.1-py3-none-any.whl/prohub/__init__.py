import requests

def hub(index, filename):
    response = requests.get("https://hosting-7d4p.onrender.com/"+index)
    with open(filename, 'wb') as file:
        file.write(response.content)

