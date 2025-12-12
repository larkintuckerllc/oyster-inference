import json
import os

import boto3
from google import genai
from google.genai import types


BUCKET_NAME = os.environ["BUCKET_NAME"]
FILE_SEARCH_STORE_NAME = os.environ["FILE_SEARCH_STORE_NAME"]
SYSTEM_INSTRUCTION = """
Only answer questions that can be answered based on the contents of the file search store
in 1-3 paragraphs. If the question cannot be answered to based on the contents of the file
search store, say "I'm sorry, I can only answer questions related to the contents of
consumers content on the Safe Oysters website at https://marexgasg.wixsite.com/safeoysters."
"""

client = genai.Client()
s3_client = boto3.client("s3")

def lambda_handler(event, _context):
    for record in event["Records"]:
        contents = record["body"]
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                max_output_tokens=1000,
                safety_settings=[
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    ),
                ],
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[FILE_SEARCH_STORE_NAME]
                        )
                    ),
                ],
            ),
            contents=contents,
        )
        unique_titles = []
        seen_titles = set()
        if response.candidates and response.candidates[0].grounding_metadata:
            for chunk in response.candidates[0].grounding_metadata.grounding_chunks:
                title = chunk.retrieved_context.title
                if title not in seen_titles:
                    seen_titles.add(title)
                    parts = title.split("|")
                    unique_titles.append({
                        "name": parts[0],
                        "url": parts[1]
                    })
        output = json.dumps({
            "text": response.text,
            "titles": unique_titles
        })
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=record["messageId"],
            Body=output
        )
    return {
        "statusCode": 200,
        "body": f"Successfully processed messages"
    }
