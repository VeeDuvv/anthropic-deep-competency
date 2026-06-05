# Lab 13: RAG Pipeline with Claude

**Day 4 | 60 min | Hands-on**

---

## Learning Objectives

- Build a complete RAG (Retrieval-Augmented Generation) pipeline
- Implement document chunking strategies
- Use embeddings for semantic search
- Ground Claude's responses in retrieved context
- Evaluate RAG quality: relevance, faithfulness, coverage

## Prerequisites

- Labs 03-04 completed
- `pip install anthropic numpy`

---

## Setup

```bash
mkdir ~/lab-13 && cd ~/lab-13
pip install anthropic numpy
```

---

## Part 1: Document Chunking (10 min)

### 1.1 Create a Knowledge Base

Create `knowledge_base.py`:

```python
"""A simple document knowledge base about a fictional company."""

DOCUMENTS = {
    "company_overview": """TechFlow Inc. is a B2B SaaS company founded in 2020, headquartered in Austin, Texas.
The company provides workflow automation tools for mid-market enterprises (500-5000 employees).
As of 2025, TechFlow has 450 employees, 2,800 customers, and $85M ARR.
The company raised a $120M Series C in January 2025, led by Sequoia Capital.
TechFlow's mission is to eliminate repetitive work through intelligent automation.""",

    "product_features": """TechFlow's core product suite includes:
1. FlowBuilder - A visual workflow designer with drag-and-drop interface. Supports conditional logic,
   parallel execution, and custom integrations. Pricing starts at $50/user/month.
2. FlowConnect - Integration platform supporting 200+ connectors (Salesforce, Slack, Jira, etc.).
   Real-time sync and batch processing. $30/user/month add-on.
3. FlowInsight - Analytics dashboard showing workflow performance, bottleneck detection, and ROI
   calculation. Included in Enterprise plans ($80/user/month).
4. FlowAI - AI-powered workflow suggestions launched in Q3 2025. Analyzes existing workflows and
   suggests optimizations. Currently in beta for Enterprise customers.""",

    "engineering_practices": """TechFlow Engineering Team Structure:
- 180 engineers across 12 teams
- Monorepo using Bazel build system
- Primary languages: TypeScript (frontend), Go (backend services), Python (ML/data)
- Infrastructure: AWS (primary), with multi-region deployment (us-east-1, eu-west-1, ap-southeast-1)
- CI/CD: GitHub Actions with 15-minute deploy pipeline
- Testing: 85% unit test coverage requirement, integration tests run nightly
- On-call: Follow-the-sun rotation across Austin, London, and Singapore offices
- Architecture: Microservices with gRPC, event-driven with Kafka, PostgreSQL + Redis""",

    "security_compliance": """TechFlow Security & Compliance:
- SOC 2 Type II certified since 2023
- ISO 27001 certified since 2024
- GDPR compliant with EU data residency option
- HIPAA compliant (BAA available for healthcare customers)
- Data encryption: AES-256 at rest, TLS 1.3 in transit
- SSO support: SAML 2.0, OIDC, with MFA required for admin accounts
- Penetration testing: Annual third-party audit by CrowdStrike
- Bug bounty program through HackerOne (launched 2024)
- Data retention: Configurable per-customer, default 7 years
- Incident response: 15-minute acknowledgment SLA, 4-hour resolution for P1""",

    "customer_success": """TechFlow Customer Success Metrics:
- Net Promoter Score: 72 (measured quarterly)
- Customer retention rate: 94% (annual)
- Average contract value: $180,000/year
- Expansion revenue: 35% of total ARR
- Time to value: Average 6 weeks from contract to first workflow live
- Support: 24/7 for Enterprise, business hours for Growth plans
- Success team: 45 CSMs, 1:40 CSM-to-customer ratio for Enterprise
- Top verticals: Financial Services (28%), Healthcare (22%), Manufacturing (18%), Retail (15%), Other (17%)
- Case studies: Published 25 case studies, average 40% efficiency improvement""",

    "recent_news": """TechFlow Recent Announcements (2025):
- Jan 2025: Closed $120M Series C at $1.2B valuation (unicorn status)
- Mar 2025: Opened Singapore office, 30 employees for APAC expansion
- Apr 2025: Launched FlowConnect v3 with 50 new integrations
- Jun 2025: FlowAI beta launched for Enterprise customers
- Jul 2025: Partnership with Salesforce for native integration
- Aug 2025: Acquired DataBridge (data transformation startup) for $25M
- Sep 2025: Reached 3,000 customer milestone
- Oct 2025: Named to Forbes Cloud 100 list (#47)"""
}


def chunk_document(doc_name, text, chunk_size=500, overlap=50):
    """Split a document into overlapping chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_text = " ".join(words[start:end])
        chunks.append({
            "id": f"{doc_name}_chunk_{len(chunks)}",
            "source": doc_name,
            "text": chunk_text,
            "start_word": start,
            "end_word": min(end, len(words)),
        })
        start += chunk_size - overlap
    return chunks


def build_chunks():
    """Build all chunks from all documents."""
    all_chunks = []
    for name, text in DOCUMENTS.items():
        chunks = chunk_document(name, text, chunk_size=100, overlap=20)
        all_chunks.extend(chunks)
    return all_chunks


if __name__ == "__main__":
    chunks = build_chunks()
    print(f"Total chunks: {len(chunks)}")
    for chunk in chunks:
        print(f"  [{chunk['id']}] {chunk['text'][:80]}...")
```

Run it: `python3 knowledge_base.py`

---

## Part 2: Embedding + Retrieval (20 min)

### 2.1 Simple TF-IDF Retrieval

We'll start with a keyword-based approach (no external embedding API needed).

Create `retriever.py`:

```python
"""Simple TF-IDF retriever for the knowledge base."""

import math
import re
from collections import Counter
from knowledge_base import build_chunks


def tokenize(text):
    """Simple tokenization: lowercase, split on non-alphanumeric."""
    return re.findall(r'\b[a-z0-9]+\b', text.lower())


class SimpleRetriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.doc_freq = Counter()
        self.chunk_tokens = []

        # Build inverted index
        for chunk in chunks:
            tokens = set(tokenize(chunk["text"]))
            self.chunk_tokens.append(tokens)
            for token in tokens:
                self.doc_freq[token] += 1

        self.n_docs = len(chunks)

    def search(self, query, top_k=3):
        """Search chunks by TF-IDF similarity to query."""
        query_tokens = tokenize(query)
        scores = []

        for i, chunk in enumerate(self.chunks):
            chunk_text = chunk["text"].lower()
            score = 0
            for token in query_tokens:
                if token in self.chunk_tokens[i]:
                    # TF: frequency in chunk
                    tf = chunk_text.count(token) / len(chunk_text.split())
                    # IDF: inverse document frequency
                    idf = math.log(self.n_docs / (1 + self.doc_freq.get(token, 0)))
                    score += tf * idf
            scores.append((score, i))

        scores.sort(reverse=True)
        results = []
        for score, idx in scores[:top_k]:
            if score > 0:
                results.append({
                    "chunk": self.chunks[idx],
                    "score": score,
                })
        return results


if __name__ == "__main__":
    chunks = build_chunks()
    retriever = SimpleRetriever(chunks)

    queries = [
        "What is TechFlow's revenue?",
        "How does TechFlow handle security?",
        "What programming languages does the engineering team use?",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        results = retriever.search(query, top_k=3)
        for r in results:
            print(f"  [{r['score']:.4f}] {r['chunk']['source']}: {r['chunk']['text'][:100]}...")
```

Run it: `python3 retriever.py`

---

## Part 3: RAG Pipeline (20 min)

### 3.1 Retrieval-Augmented Generation

Create `rag.py`:

```python
"""Complete RAG pipeline: retrieve context, then generate answer."""

import anthropic
from knowledge_base import build_chunks
from retriever import SimpleRetriever

client = anthropic.Anthropic()

# Build the retriever
chunks = build_chunks()
retriever = SimpleRetriever(chunks)


def rag_query(question, top_k=5, show_context=True):
    """Answer a question using RAG."""

    # Step 1: Retrieve relevant chunks
    results = retriever.search(question, top_k=top_k)

    if not results:
        return "I couldn't find relevant information to answer this question."

    # Step 2: Format context
    context_parts = []
    for i, r in enumerate(results, 1):
        source = r["chunk"]["source"].replace("_", " ").title()
        context_parts.append(f"[Source {i}: {source}]\n{r['chunk']['text']}")

    context = "\n\n".join(context_parts)

    if show_context:
        print(f"Retrieved {len(results)} chunks:")
        for r in results:
            print(f"  [{r['score']:.4f}] {r['chunk']['source']}")
        print()

    # Step 3: Generate answer with context
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="""You are a helpful assistant that answers questions about TechFlow Inc.
Use ONLY the provided context to answer questions. If the context doesn't contain
enough information to fully answer the question, say so.

Rules:
- Cite your sources using [Source N] notation
- Be specific — use numbers and facts from the context
- If you're not sure about something, say "Based on the available information..."
- Do not make up information not present in the context""",
        messages=[
            {
                "role": "user",
                "content": f"""<context>
{context}
</context>

<question>
{question}
</question>

Answer the question using only the provided context. Cite sources.""",
            }
        ],
    )

    return response.content[0].text


def rag_without_context(question):
    """Answer without RAG for comparison."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Answer this question about TechFlow Inc.: {question}"}
        ],
    )
    return response.content[0].text


# Test the RAG pipeline
questions = [
    "What is TechFlow's annual recurring revenue and how many customers do they have?",
    "What security certifications does TechFlow hold?",
    "What happened with TechFlow in the second half of 2025?",
    "What is the pricing for FlowBuilder?",
    "What is TechFlow's employee count in their Singapore office?",
]

for q in questions:
    print(f"\n{'='*60}")
    print(f"Q: {q}")
    print(f"{'='*60}")

    print("\n--- RAG Answer ---")
    rag_answer = rag_query(q)
    print(rag_answer)

    print("\n--- Without RAG (hallucination risk) ---")
    plain_answer = rag_without_context(q)
    print(plain_answer[:300] + "..." if len(plain_answer) > 300 else plain_answer)
```

Run it: `python3 rag.py`

**Compare:** RAG answers should cite sources and stay grounded. Non-RAG answers may hallucinate details about a fictional company.

---

## Part 4: Evaluation (10 min)

### 4.1 RAG Quality Check

Create `eval_rag.py`:

```python
"""Evaluate RAG pipeline quality."""

import anthropic
from rag import rag_query

client = anthropic.Anthropic()

EVAL_CASES = [
    {
        "question": "What is TechFlow's ARR?",
        "expected_facts": ["$85M ARR"],
    },
    {
        "question": "When was TechFlow founded?",
        "expected_facts": ["2020"],
    },
    {
        "question": "What is TechFlow's customer retention rate?",
        "expected_facts": ["94%"],
    },
]

def evaluate_answer(question, answer, expected_facts):
    """Use Claude to evaluate RAG answer quality."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": f"""Evaluate this RAG answer for quality.

Question: {question}
Answer: {answer}
Expected facts: {expected_facts}

Score on three dimensions (1-5 each):
1. Faithfulness: Does the answer only contain facts from the sources? (no hallucination)
2. Relevance: Does the answer address the question?
3. Completeness: Does it include all expected facts?

Output ONLY a JSON object: {{"faithfulness": N, "relevance": N, "completeness": N, "notes": "..."}}""",
            },
            {"role": "assistant", "content": "{"},
        ],
    )
    return "{" + response.content[0].text

print("RAG Evaluation Results")
print("=" * 60)

for case in EVAL_CASES:
    answer = rag_query(case["question"], show_context=False)
    evaluation = evaluate_answer(case["question"], answer, case["expected_facts"])
    print(f"\nQ: {case['question']}")
    print(f"A: {answer[:150]}...")
    print(f"Eval: {evaluation}")
```

---

## Deliverables

- [ ] `knowledge_base.py` — document store with chunking
- [ ] `retriever.py` — TF-IDF based retrieval
- [ ] `rag.py` — complete RAG pipeline with source citations
- [ ] `eval_rag.py` — RAG quality evaluation

## Stretch Goals

1. Replace TF-IDF with Voyage AI embeddings for semantic search
2. Add a reranking step: retrieve 10 chunks, use Claude to rerank to top 3
3. Implement "agentic RAG" — the agent decides when to retrieve more context
