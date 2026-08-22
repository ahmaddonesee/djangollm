# from openai import OpenAI
# import openai,os

# api_key = os.getenv("OPENAI_API_KEY",None)
# # 
# openai.api_key = api_key

# client = OpenAI()
# # client = OpenAI(api_key=api_key)




# def ask_llm(question, document_content):

#     prompt = f"""You are an assistant that answers questions using the provided document. Document:
#     {document_content}
#     Question:
#     {question}
#     Answer the question based only on the document.
#     """
#     response = client.responses.create(model="gpt-5.6-luna",input=prompt)
    
#     return response.output_text