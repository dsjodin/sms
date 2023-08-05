import requests

class SMSAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_sms(self, recipient, content):
        response = requests.post(f"{self.base_url}/sendsms", json={
            "recipient": recipient,
            "content": content
        })

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: received status code {response.status_code}")

    def poll_for_messages(self, plate_number=None):
        while True:
            response = requests.get(f"{self.base_url}/receivesms")
            if response.status_code == 200:
                messages = response.json()
                if messages:
                    if plate_number:
                        return [message for message in messages if message['plate_number'] == plate_number]
                    else:
                        return messages
            else:
                raise Exception(f"Error: received status code {response.status_code}")
