import requests
import json

class Stage:
    def __init__(self):
        with open('info.json', 'r') as config_file:
            config = json.load(config_file)
            self.url = f'{config["url"]}stage'
                    
    def send_msg(self, msg):
        headers = {
            'Content-Type': 'application/json',
            'accept': '*/*'
        }

        if(not isinstance(msg, str)):
            print("erreur, le message doit être une string")
            return False

        msg = f'\"{msg}\"'

        response = requests.put(f"{self.url}/message", data=msg.encode('utf-8'), headers=headers)

        if response.status_code == 204:
            print(f"Message envoyé au prompteur: {msg}")
            return True
        else:
            print(f'Échec de la requête. Code de statut : {response.status_code}')
            return False

    def delete_msg(self):
        headers = {
            'Content-Type': 'application/json',
            'accept': '*/*'
        }

        response = requests.delete(f"{self.url}/message", headers=headers)

        if response.status_code == 204:
            print(f"Message Supprimé du prompteur")
            return True
        else:
            print(f'Échec de la requête. Code de statut : {response.status_code}')
            return False