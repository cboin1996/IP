from twilio.rest import Client
import os
import json
class Messager:
    pathToSelf = os.path.dirname(os.path.realpath(__file__))
    pathToSettings = os.path.join(pathToSelf, 'acct.json')
    # loads settings from acct.json used to send a message.
    def __init__(self):
        self.twilSettings = {}
        self.ssid_key = "acct sid"
        self.auth_ssid_key = "auth token"
        self.twil_num_key = "twilio number"
        self.user_num_key = "personal number"
        with open(self.pathToSettings, 'r') as in_file:
            self.twilSettings = json.loads(in_file.read())
            if self.twilSettings is None:
                self.initialize_settings(self.pathToSettings)


    def initialize_settings(self, path):
        settings = {}
        for setting in [self.ssid_key, self.auth_ssid_key, self.twil_num_key, self.user_num_key]:
            settings[setting] = input(f"Enter your {setting}: ")
        with open(path, 'w') as f:
            json.dump(settings, f)
            print("Settings configured.")

    def createSMS(self, messageBody):
        client = Client(self.twilSettings["acct_sid"], self.twilSettings["auth_token"])

        message = client.messages \
                        .create(
                                body=messageBody,
                                from_=self.twilSettings["twil_num"],
                                to=self.twilSettings["pers_num"]
                                )

if __name__=="__main__":
    content = input("Enter your text message content: ")
    messager = Messager()
    messager.createSMS(content)
