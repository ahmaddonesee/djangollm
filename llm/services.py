import requests
from django.conf import settings
import json
import os


api_key=os.getenv("OPENAI_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"




def ask_question(question, document_content):

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    prompt = f"""
You are a document search assistant.

Your job is to answer the user's search query using ONLY the
information contained in the uploaded documents.

USER SEARCH:
{question}

UPLOADED DOCUMENTS:
{document_content}

Instructions:
1. Find information in the documents that is relevant to the search.
2. Give a direct and useful answer.
3. If the search term is a topic such as "Django", explain the
   relevant information about Django found in the documents.
4. Do not ask the user what they want to do.
5. Do not suggest unrelated tasks.
6. If there is no relevant information, say:
   "No relevant information was found in the documents."
7. Mention the file name when possible.
"""

    data = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=data,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]


# def ask_question(question, document_content):
#   headers={
#     "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
#     "Content-Type": "application/json",
#   }
#   data=json.dumps({
#     # "model": "nex-agi/nex-n2.5-mini:free",
#     "model": "openrouter/free",
#     "messages": [
#         {
#           "role": "user",
#           "content": question
#         },
#         {
#           "role": "user",
#           "content": document_content
#         }
#       ],
#     "reasoning": {"enabled": True}
#   })
#   response = requests.post(OPENROUTER_URL, headers=headers, data=data)
#   response.raise_for_status()
#   result = response.json()
#   answer = result["choices"][0]["message"]["content"]
#   return answer




