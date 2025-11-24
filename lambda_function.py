from google import genai
from google.genai import types


client = genai.Client()

CONTENTS = "How does water temperature affect clam growth?"
FILE_SEARCH_STORE_NAME = "fileSearchStores/oyster-nmld1veorljm"
SYSTEM_INSTRUCTION = """
Only answer questions related to the contents of the file search store in 1-3 paragraphs.
If the question is not related to the contents of the file search store, say "I'm sorry, I can only answer questions related to the contents of the file search store."
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[FILE_SEARCH_STORE_NAME]
                )
            )
        ],
    ),
    contents=CONTENTS,
)
print(response.text)
# TODO: MAX TOKENS
# TODO: SAFETY