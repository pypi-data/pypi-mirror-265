import requests
import json
from uuid import uuid4

RED_TEAM_CONVERSATION_END_TOKEN = "<|done|>"

class AttackBot:
    def __init__(self, context_description, attack_description, vv_api_key):
        self.attack_description = attack_description
        self.context_description = context_description
        self.memory = []
        self.conversation_id = str(uuid4())
        self.vv_api_key = vv_api_key

    def chat(self, msg):
        url = "https://us-central1-agent-evals.cloudfunctions.net/auto-red-team"
        data = {
            "memory": json.dumps(self.memory),
            "api_key": self.vv_api_key,
            "message": msg,
            "context": self.context_description,
            "attack": self.attack_description,
            "conv_id": self.conversation_id,
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.memory.append({"role": "user", "content": msg})
            self.memory.append({"role": "assistant", "content": response.text})
            return response.text
        else:
            raise Exception("Server error: " + response.text)

    def objective_achieved(self):
        if not self.memory or len(self.memory) == 0:
            return False
        last_message = self.memory[-1]
        if last_message["role"] == "assistant" and RED_TEAM_CONVERSATION_END_TOKEN in last_message["content"]:
            return True
        return False
