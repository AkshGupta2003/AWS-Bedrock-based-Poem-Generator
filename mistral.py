from pyexpat import model
import boto3
import json

prompt_data = """
You are a creative writing model, your task is to write a poem in the style of William Shakespeare on machine learning.

# Writing Style
* Use Early Modern English vocabulary and poetic tone.
* Maintain iambic pentameter rhythm when possible.
* Include themes of **love, fate, nature, beauty, and time**.
* Use literary devices such as **metaphor, simile, personification, and rhyme**.
* End each poem with a **reflective or emotional conclusion**.

# Examples
## Example 1

User: Write a poem about love.
"Love’s gentle flame, though kindled swift, doth stay,\nThrough tempests wild and nights of bitter grief;\nFor hearts entwined, though torn, find yet a way,\nTo weave their wounds into a sweet belief."

## Example 2

User: Write a poem about time.
"O cruel Time, that steals the bloom of youth,\nThy silent hand makes mock of mortal pride;\nYet in thy theft, thou leav’st eternal truth,\nFor beauty lost in flesh in verse shall bide."
"""

bedrock=boto3.client(service_name="bedrock-runtime")
payload = {
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_data
                }
            ]
        }
    ],
    "max_tokens": 512,
    "temperature": 0.5
}

body = json.dumps(payload)
model_id = "arn:aws:bedrock:eu-north-1:957113178795:inference-profile/eu.mistral.pixtral-large-2502-v1:0"
response = bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json"
)

response_body = json.loads(response.get("body").read())
response_text = response_body["choices"][0]["message"]["content"]
print(response_text)