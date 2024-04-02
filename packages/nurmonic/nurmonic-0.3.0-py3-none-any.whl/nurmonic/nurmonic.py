import os
import requests

class Nurmonic:
    def __init__(self, api_key=None):
        self.api_key = api_key if api_key is not None else os.environ.get('NURMONIC_KEY')
        self.base_url = 'https://nurmonic.xyz/chat/completions'

    def create_completion(self, messages, model, character=None):
        headers = {'Authorization': self.api_key}

        if model == 'nurmo-2' and character is None:
            raise ValueError("When using model 'nurmo-2', a character must be provided.")

        data = {'model': model, 'messages': messages}

        if model == 'nurmo-2':
            data['character'] = character

        response = requests.post(self.base_url, json=data, headers=headers)
        response_text = response.text

        try:
            response_data = response.json()
            if 'error' in response_data:
                if response_data['error'] == "Unknown model":
                    raise Exception(f"Unknown model named {model}")
                else:
                    raise Exception(response_data['error'])
        except:
            pass

        return response_text
