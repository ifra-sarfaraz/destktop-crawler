import os
import json
from collections import defaultdict
from docx import Document
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer

def read_file(filepath):
    if filepath.endswith(".txt"):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    elif filepath.endswith(".docx"):
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs])
    elif filepath.endswith(".pdf"):
        reader = PdfReader(filepath)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    else:
        return ""

def build_index(folder_path):
    docs = []
    paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if not file.endswith(('.txt', '.docx', '.pdf')):
                continue
            filepath = os.path.join(root, file)
            try:
                content = read_file(filepath)
                docs.append(content)
                paths.append({"path": filepath, "content": content})
            except Exception as e:
                print(f"Skipping {filepath}: {e}")

    # Create TF-IDF vectorizer and matrix
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(docs)
    index = {
        'vectorizer': vectorizer,
        'docs': paths,
        'matrix': matrix
    }
    return index

def save_index(index, filename):
    # Save docs separately since vectorizer and matrix can't be serialized directly
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({'docs': index['docs']}, f)

def load_index(filename):
    # Load docs and rebuild vectorizer and matrix
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    docs = [doc['content'] for doc in data['docs']]
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(docs)
    return {
        'vectorizer': vectorizer,
        'docs': data['docs'],
        'matrix': matrix
    }