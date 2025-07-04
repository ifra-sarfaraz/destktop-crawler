import os
from docx import Document
from pdfminer.high_level import extract_text

def read_txt(path):
    return open(path, "r", encoding="utf-8").read()

def read_pdf(path):
    return extract_text(path)

def read_docx(path):
    return "\n".join(p.text for p in Document(path).paragraphs)

def crawl_dir(directory):
    docs = []
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            try:
                if file.endswith(".txt"):
                    text = read_txt(path)
                elif file.endswith(".pdf"):
                    text = read_pdf(path)
                elif file.endswith(".docx"):
                    text = read_docx(path)
                else:
                    continue
                docs.append({"path": path, "content": text})
            except Exception as e:
                print(f"Error reading {path}: {e}")
                continue
    return docs
