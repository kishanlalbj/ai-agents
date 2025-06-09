import ollama

# Ollama lib calls ollama apis behind the scenes.

response = ollama.list() # lists models

print(response)

res1 = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": " what is your name and why is sky blue ?"
            }
        ]
)

print(res1.message.content)


res2 = ollama.generate(
    model="llama3.2",
    prompt="Why is sky blue ?"
)

print(ollama.show("llama3.2"))

ollama.create(
    model="aquaman",
    from_="llama3.2",
    system="You are named is Aquaman a very smart assistant who knows everything about oceans. you are very succinct",
)

res3 = ollama.generate(
    model="aquaman",
    prompt="what s your name ?"
)

print(res3.response)

ollama.delete("aquaman")

