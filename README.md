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

```bash

### 2. Clone the Repository

git clone [https://github.com/your-username/smartcommerce-ai.git](https://github.com/your-username/smartcommerce-ai.git)
cd smartcommerce-ai

### 2 Set Up Environment Variables
Create a .env file in the root directory:


GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=mysql+aiomysql://user:password@localhost/db_name

###  3. Install Dependencies
Bash
pip install -r requirements.txt

### 4. Run the Server
Bash
uvicorn main:app --reload

## 🤖 Agent Workflow

The AI follows a specific logic flow to ensure accuracy and reliability:

Chatbot Node: Receives input and decides whether to respond or call a tool based on the System Prompt.

Sentiment Analyzer: Evaluates the user's mood. If "Angry," it triggers a state flag for handoff.

Tool Node: Executes Python functions (DB lookups, Ticket creation).

Loopback: After a tool runs, the agent returns to the Chatbot node to explain the result to the user.


## Method,Endpoint,Description

POST,/chat,"Main interaction point. Send user_id, session_id, and query."
GET,/tickets,Retrieve all active support tickets created by the AI.


# 📂 Project Structure
Plaintext

├── agent/
│   ├── graph.py          # LangGraph workflow definition
│   ├── state.py          # TypedDict state definitions
│   └── tools.py          # Database-connected AI tools
├── database.py           # Async SQLAlchemy engine & session
├── models.py             # MySQL Tables (User, Order, Ticket, etc.)
├── main.py               # FastAPI application & Chat routes
├── schemas.py            # Pydantic request/response models
└── .env                  # Configuration (Secrets)


