import ollama


# response = ollama.embeddings(model='nomic-embed-text', prompt='The sky is blue because of rayleigh scattering')
# print(response.embedding)


res = ollama.chat(model="llama3.1:8b", stream=False, messages=[{"role": "user","content": "why the sky is blue"}], options={"temperature":0})
print(res.message.content)