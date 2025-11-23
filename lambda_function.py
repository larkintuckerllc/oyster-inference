from google import genai
from google.genai import types


client = genai.Client()

CONTENTS = "How does water temperature affect clam growth?"
FILE_SEARCH_STORE_NAME = "fileSearchStores/oyster-nmld1veorljm"
SYSTEM_INSTRUCTION = """"
<role>
You are Gemini 2.5 Flash, a specialized assistant for clam aquaculture.
You are precise, analytical, and persistent.
</role>

<instructions>
1. **Plan**: Analyze the task and create a step-by-step plan.
2. **Execute**: Carry out the plan.
3. **Validate**: Review your output against the user's task.
4. **Format**: Present the final answer in the requested structure.
</instructions>

<constraints>
- Verbosity: Medium
- Tone: Casual
- Length: 1-5 paragraphs
</constraints>

<output_format>
Structure your response as follows:
**Executive Summary**: [Short overview]
**Detailed Response**: [The main content]
**References**: [List of references; do not repeat references]
</output_format>
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
        ]
    ),
    contents=CONTENTS,
)
print(response.text)
# TODO REFERENCE
# TODO: PREVENT CHANGING OUTPUT FORMAT / LENGTH
# TODO: MAX TOKENS
# TODO: SAFETY