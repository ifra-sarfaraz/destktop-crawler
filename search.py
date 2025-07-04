from sklearn.metrics.pairwise import cosine_similarity
import re

def search_query(query, index, method="tfidf", use_stemming=False):
    vectorizer = index['vectorizer']
    docs = index['docs']
    matrix = index['matrix']
    q_vector = vectorizer.transform([query])
    scores = cosine_similarity(matrix, q_vector).flatten()
    ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
    results = []
    for score, doc in ranked[:5]:
        content = doc['content'].lower()
        query_count = len(re.findall(rf'\b{re.escape(query.lower())}\b', content))
        results.append({
            "path": doc['path'],
            "score": float(score),
            "snippet": doc['content'][:200],
            "query_count": query_count
        })
    return results