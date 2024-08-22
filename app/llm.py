import json
import requests

# NOTE: ollama must be running for this to work, start the ollama app or run `ollama serve`
model = "qwen2"


def request_ollama(messages):
    r = requests.post(
        "http://0.0.0.0:11434/api/chat",
        json={"model": model, "messages": messages, "stream": True},
        stream=True
    )
    r.raise_for_status()
    output = ""

    for line in r.iter_lines():
        body = json.loads(line)
        if "error" in body:
            raise Exception(body["error"])
        if body.get("done") is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            # the response streams one token at a time, print that as we receive it
            print(content, end="", flush=True)

        if body.get("done", False):
            message["content"] = output
            return message


def chat(txt: str):
    messages = []
    # 构建message
    message = {"role": "user", "content": txt}
    messages.append(message)

    result = request_ollama(messages)
    messages.append(result)


def main():
    while True:
        user_input = input("Enter a prompt: ")
        if not user_input:
            exit()
        chat(user_input)


if __name__ == "__main__":
    main()
