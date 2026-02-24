import os
import json
from flask import Flask
from google.cloud import tasks_v2

app = Flask(__name__)

# --- CONFIGURATION ---
PROJECT_ID = "methodical-ace-482313-m2"       # <-- Change this!
LOCATION = "us-central1"             # <-- Change this!
QUEUE_ID = "billing-queue"
WEBHOOK_URL = "https://webhook.site/00194eb7-606a-47f1-9bdf-ad41c3050c84" # <-- Paste your webhook.site URL here!

client = tasks_v2.CloudTasksClient()
parent = client.queue_path(PROJECT_ID, LOCATION, QUEUE_ID)

@app.route("/generate-bills", methods=["POST"])
def generate_bills():
    print("🚨 SCHEDULER WOKE US UP! Generating 20 user bills...")
    
    # Simulate generating 20 user payments
    for i in range(1, 21):
        payload = {"user_id": f"User_{i}", "amount_due": 14.99, "plan": "Netflix Premium"}
        
        # Construct the task request
        task = {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": WEBHOOK_URL,
                "headers": {"Content-type": "application/json"},
                "body": json.dumps(payload).encode(),
            }
        }
        
        # Throw it into the Cloud Tasks queue!
        client.create_task(request={"parent": parent, "task": task})
        print(f"Added User_{i} to the queue.")

    return "20 Bills successfully queued!", 200

if __name__ == "__main__":
    app.run(port=8080)