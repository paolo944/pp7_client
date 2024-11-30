import requests
import json

class Timer:
    def __init__(self):
        with open('info.json', 'r') as config_file:
            config = json.load(config_file)
            self.url = f'{config["url"]}timer'
                    
    def play(self, uuid):
        headers = {
            'Content-Type': 'application/json',
            'accept': '*/*'
        }

        response = requests.get(f"{self.url}/{uuid}/start", headers=headers)

        if response.status_code == 204:
            print(f"Clock {uuid} play")
            return True
        else:
            print(f'Échec de la requête. Code de statut : {response.status_code}')
            return False

    def pause(self, uuid):
        headers = {
            'Content-Type': 'application/json',
            'accept': '*/*'
        }

        response = requests.get(f"{self.url}/{uuid}/stop", headers=headers)

        if response.status_code == 204:
            print(f"Clock {uuid} stopped")
            return True
        else:
            print(f'Échec de la requête. Code de statut : {response.status_code}')
            return False

    def reset(self, uuid):
        headers = {
            'Content-Type': 'application/json',
            'accept': '*/*'
        }

        response = requests.get(f"{self.url}/{uuid}/reset", headers=headers)

        if response.status_code == 204:
            print(f"Clock {uuid} reset")
            return True
        else:
            print(f'Échec de la requête. Code de statut : {response.status_code}')
            return False

    def delete(self, uuid):
        headers = {
            'Content-Type': 'application/json',
            'accept': '*/*'
        }

        response = requests.delete(f"{self.url}/{uuid}", headers=headers)

        if response.status_code == 204:
            print(f"Clock {uuid} deleted")
            return True
        else:
            print(f'Échec de la requête. Code de statut : {response.status_code}')
            return False

    def post(self, data):
        headers = {
            'Content-Type': 'application/json',
            'accept': '*/*'
        }

        hours = data.get('hours')
        minutes = data.get('minutes')
        seconds = data.get('seconds')
        name = data.get('clock_name')

        seconds = int(seconds)
        seconds += int(minutes) * 60
        seconds += int(hours) * 3600

        data = {
            "allows_overrun": True,
            "countdown": {
                "duration": seconds
            },
            "name": name
        }

        json_data = json.dumps(data)

        response = requests.post(f"{self.url}s", headers=headers, data=json_data)

        if response.status_code == 200:
            print(f"Clock {name} ajouté")
            return True
        else:
            print(f'Échec de la requête. Ajout clock, Code de statut : {response.status_code}')
            return False
    
    