import json
import boto3
import botocore.config
from datetime import datetime


def poem_generator_using_bedrock(poem_title: str)-> str:
    prompt_data = f"""
    You are a creative writing model, your task is to write a poem in the style of William Shakespeare on {poem_title}.

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
    try:
        bedrock=boto3.client(service_name="bedrock-runtime", region_name="eu-north-1",
                        config=botocore.config.Config(read_timeout=300,retries={'max_attempts':3}))

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

        return response_text
    
    except Exception as e:
        print(f"Error in generating the poem: {e}" )
        return ""

def save_poem_details_s3(s3_key, s3_bucket, generate_poem):
    s3 = boto3.client("s3")

    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body = generate_poem )
        print("Code saved to s3")

    except Exception as e:
        print("Error when saving the code to s3")


def lambda_handler(event, context):
    
    event = json.loads(event['body'])
    poem_title=event['poem_title']

    generate_poem = poem_generator_using_bedrock(poem_title=poem_title)

    if generate_poem:
        current_time=datetime.now().strftime('%H%M%S')
        s3_key=f"poem-output/{current_time}.txt"
        s3_bucket='aws-poem-generator'
        save_poem_details_s3(s3_key,s3_bucket,generate_poem)

    else:
        print("No poem was generated")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

