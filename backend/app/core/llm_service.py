from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_llm(question, context):

    prompt = f"""
You are an engineering assistant.

Answer the question using ONLY the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content