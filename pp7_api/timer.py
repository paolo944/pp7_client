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
    
    