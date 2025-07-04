from openai import OpenAI
import re
import os

def generate_rag_answer(docs, query):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    client = OpenAI(api_key=api_key)
    context = "\n".join([doc.get('snippet', doc.get('content', '')) for doc in docs])
    query_count = len(re.findall(rf'\b{re.escape(query.lower())}\b', context.lower()))
    prompt = (
        f"Query: {query}\n"
        f"Context: {context}\n"
        f"Task: Provide a concise answer stating how many times the word '{query}' appears in the provided context (case-insensitive) and summarize the context related to '{query}'."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes text and provides concise answers."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        answer = "Error generating answer from LLM."
    return f"{answer} (Found {query_count} occurrences of '{query}' in context)"