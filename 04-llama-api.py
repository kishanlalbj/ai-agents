import requests
import json


url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3.2",
    "prompt": "Tell me a short story and make it funny"
}

response = requests.post(url, json=data, stream=True)

if response.status_code == 200:
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")
            result = json.loads(decoded_line)
            generated_story = result.get("response", "")
            print(generated_story, end="", flush=True)
else:
    print("Something went wrong")
    print(response.text)
    print(response.status_code)
    print(response.reason)
