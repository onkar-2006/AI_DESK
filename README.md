# 🛒 SmartCommerce AI: Intelligent E-commerce Support System

A production-ready AI Support Agent built with **LangGraph**, **FastAPI**, and **Groq**. This system handles real-time customer queries, tracks orders, searches store policies, and performs automated human handoffs via a persistent MySQL ticketing system.



## 🌟 Key Features

* **Stateful AI Conversations:** Uses LangGraph to maintain context and manage complex multi-step support logic.
* **Order Tracking:** Deep integration with database models to provide real-time status and delivery partner details.
* **Knowledge Base Search:** Semantic-style searching through store policies and FAQs.
* **Automated Human Handoff:** Sentiment-aware logic that detects frustration and creates support tickets in MySQL.
* **Persistent History:** Complete chat history storage in MySQL with session-based recovery.
* **Self-Healing Logic:** Robust tool-calling that ensures database integrity even if the LLM provides incomplete IDs.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Orchestration:** [LangGraph](https://langchain-ai.github.io/langgraph/)
* **LLM Engine:** [Groq](https://groq.com/) (GPT-OSS-120B / Llama 3)
* **Database:** MySQL with [SQLAlchemy](https://www.sqlalchemy.org/) (Async)
* **Environment:** Python-Dotenv

---


### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/smartcommerce-ai.git](https://github.com/your-username/smartcommerce-ai.git)
cd smartcommerce-ai

2. Set Up Environment Variables
Create a .env file in the root directory:

GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=mysql+aiomysql://user:password@localhost/db_name
