from google import genai
from google.genai import types


client = genai.Client()

CONTENTS = "How does water temperature affect clam growth?"
FILE_SEARCH_STORE_NAME = "fileSearchStores/oyster-bqyx5yps5cij"
SYSTEM_INSTRUCTION = """
Only answer questions related to the contents of the file search store in 1-3 paragraphs.
If the question is not related to the contents of the file search store, say "I'm sorry,
I can only answer questions related to the contents of the file search store."
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

print(response.text)
print(unique_titles)
# TODO: MAX TOKENS
# TODO: SAFETY