# personal

Excellent — this is exactly how you should frame your **Copilot-guided build** for maximum precision. Below is a **two-file setup**:

1. `COPILOT_INSTRUCTIONS.md` → Tells GitHub Copilot *how to behave* (its persona, architecture decisions, priorities).
2. `INSTRUCTIONS.md` → Tells **you + Copilot** *what to build step-by-step* (your project plan).

This combination will help Copilot scaffold your **Agentic Knowledge Graph Builder for Financial Data Products** using **LangChain/LangGraph, SQLAlchemy, and Neo4j**, directly connecting to **Databricks Delta tables (EDL)** instead of CSVs.

---

# 🧭 `COPILOT_INSTRUCTIONS.md`

> Place this file at the root of your repo. Copilot reads it as guidance for code generation and architectural consistency.

````markdown
# GitHub Copilot Custom Instructions
You are assisting in building a project called **Agentic Knowledge Graph Builder for Financial Data Products**.

## 🎯 Goal
Build a structured-only, agentic knowledge graph system that connects **financial data products** (Customers, Agreements, Payments, Collateral) stored in **Databricks Delta tables** via SQLAlchemy, into a unified **Neo4j knowledge graph**, using **LangGraph + LangChain + OpenAI APIs**.

The system should be modular, agentic, and easily extensible.

---

## 🧩 Architecture Overview

**Core Components**
- Agents for:
  - Intent understanding
  - Table/schema discovery via SQLAlchemy (Databricks)
  - Schema proposal & refinement
  - Graph builder (Neo4j)
  - Query interface (NL → Cypher)
- LangGraph orchestrates the workflow between agents.
- Streamlit UI for demo and hackathon presentation.

**Flow**
1. User provides intent (e.g. “connect customer, agreements, payments”).
2. System inspects Databricks tables (via SQLAlchemy) → extracts schema.
3. Schema proposal agent infers node and relationship types.
4. Graph builder agent creates nodes/edges in Neo4j.
5. Query agent converts NL to Cypher for exploration.

---

## 🧠 Key Libraries & Setup

- `langchain`, `langgraph`, `openai`, `neo4j`, `sqlalchemy`, `pandas`, `streamlit`, `python-dotenv`
- Connect to **Databricks** via:
  ```python
  engine = create_engine("databricks+connector://token:<DATABRICKS_TOKEN>@<HOST>:443/<CATALOG>.<SCHEMA>")
````

* Access Delta table schema with SQLAlchemy reflection.
* Insert data into Neo4j using the `neo4j` Python driver.

---

## 🧱 Folder Structure (Copilot must maintain)

```
agentic-kg-finance/
│── README.md
│── docker-compose.yml
│── .env.example
│
├── app/
│   ├── requirements.txt
│   ├── config.py
│   │
│   ├── agents/
│   │   ├── intent_agent.py
│   │   ├── table_discovery_agent.py
│   │   ├── schema_proposal_agent.py
│   │   ├── graph_builder_agent.py
│   │   └── query_agent.py
│   │
│   ├── workflows/
│   │   └── structured_pipeline.py
│   │
│   ├── ui.py
│   └── utils/
│       ├── databricks_connector.py
│       └── neo4j_helper.py
```

---

## ⚙️ Copilot Implementation Guidelines

* Each agent should be implemented as a **class with a `run()` method**.
* Use **dependency injection** for shared configs (Databricks/Neo4j connections).
* Add **docstrings** explaining agent purpose and input/output clearly.
* Code must use **async/await** where useful for API calls.
* Follow **clean architecture principles**:

  * Agents in `agents/`
  * Orchestration in `workflows/`
  * External connections in `utils/`
* Use **logging**, not prints, for internal debugging.
* Always include **type hints** for function signatures.

---

## 🧩 LangGraph Integration

Copilot should use `StateGraph` from `langgraph.graph` to connect the following agent nodes:

```
IntentAgent → TableDiscoveryAgent → SchemaProposalAgent → GraphBuilderAgent → QueryAgent
```

Each node should pass context/state (intent, schema info, etc.) forward.

---

## 🧪 Example Prompt Behavior

When user says:

> "Build a KG linking customers, agreements, and payments."

Expected flow:

1. `IntentAgent` → extracts “connect customers, agreements, payments”.
2. `TableDiscoveryAgent` → queries Databricks catalog for table metadata.
3. `SchemaProposalAgent` → infers relationships (CUSTOMER_HAS_AGREEMENT, AGREEMENT_HAS_PAYMENT).
4. `GraphBuilderAgent` → inserts nodes/edges into Neo4j.
5. `QueryAgent` → enables Cypher/NL queries.

---

## 🚀 Copilot Output Quality Targets

* Use **modular**, reusable functions.
* Generate minimal, readable, production-quality code.
* Avoid mockups or print-based logic unless explicitly testing.
* Prefer explicit connection handling (no globals).
* Include fallback logic for missing FKs or inconsistent schemas.
* Code must be **runnable in Docker**.

---

## 🔒 Security & Credentials

* Load secrets from `.env`
* Never hardcode Databricks or Neo4j credentials.
* Respect the config file structure (`config.py`).

---

## ✅ Deliverables

Copilot should generate:

1. Functional pipeline that connects to Databricks → infers schemas → builds Neo4j KG.
2. Streamlit app for end-user query and visualization.
3. Reusable agents and workflow logic.

````

---

# 🧭 `INSTRUCTIONS.md`

> This file defines *your build plan and step-by-step tasks for Copilot*.

```markdown
# 🏗️ Agentic Knowledge Graph Builder (Financial Data Products)

This document defines the **build plan** for constructing the project using GitHub Copilot.  
Each step is atomic — ask Copilot to implement one file or function at a time.

---

## 🔹 Step 1: Setup Environment

- Create `agentic-kg-finance/` project folder.
- Add `.env.example`:
  ```env
  OPENAI_API_KEY=your_key_here
  DATABRICKS_HOST=<your_host>
  DATABRICKS_TOKEN=<your_token>
  DATABRICKS_CATALOG=<catalog>
  DATABRICKS_SCHEMA=<schema>
  NEO4J_URI=bolt://neo4j:7687
  NEO4J_USER=neo4j
  NEO4J_PASSWORD=password
````

* Add `requirements.txt`:

  ```
  langchain
  langgraph
  openai
  neo4j
  sqlalchemy
  pandas
  streamlit
  python-dotenv
  ```

---

## 🔹 Step 2: Implement Configuration

* Create `app/config.py` to load `.env` and expose environment variables.
* Add a function to return Databricks SQLAlchemy engine and Neo4j driver.

---

## 🔹 Step 3: Create Databricks Connector Utility

File: `app/utils/databricks_connector.py`

* Use SQLAlchemy’s reflection:

  ```python
  from sqlalchemy import create_engine, inspect
  engine = create_engine(f"databricks+connector://token:{token}@{host}:443/{catalog}.{schema}")
  inspector = inspect(engine)
  tables = inspector.get_table_names()
  columns = inspector.get_columns(table_name)
  ```
* Return a dictionary of `{table_name: [column metadata]}`.

---

## 🔹 Step 4: Create Neo4j Helper

File: `app/utils/neo4j_helper.py`

* Initialize Neo4j driver.
* Add helper functions:

  * `create_node(label, properties)`
  * `create_relationship(parent_label, child_label, parent_id, child_id, rel_type)`
  * `run_cypher(query)`

---

## 🔹 Step 5: Implement Agents

1. **IntentAgent**

   * Extract goal and entities from natural language prompt.
2. **TableDiscoveryAgent**

   * Map discovered entities (from IntentAgent) to Databricks table names.
3. **SchemaProposalAgent**

   * Infer possible relationships and graph schema based on metadata.
4. **GraphBuilderAgent**

   * Create nodes/relationships in Neo4j.
5. **QueryAgent**

   * Translate NL queries → Cypher (use OpenAI API).

---

## 🔹 Step 6: Implement LangGraph Workflow

File: `app/workflows/structured_pipeline.py`

* Create a `StateGraph` with:

  ```
  IntentAgent → TableDiscoveryAgent → SchemaProposalAgent → GraphBuilderAgent → QueryAgent
  ```
* Pass shared state between nodes.
* Log outputs for debugging.

---

## 🔹 Step 7: Add Streamlit UI

File: `app/ui.py`

* Input: user intent / natural language question.
* Buttons:

  * “Build KG”
  * “Query KG”
* Display:

  * Agent responses
  * Cypher queries
  * JSON / tabular output.

---

## 🔹 Step 8: Dockerize

File: `docker-compose.yml`

* Services:

  * `neo4j`
  * `app` (Python + Streamlit)
* Mount `/app` for hot reload.
* Include `.env`.

---

## 🔹 Step 9: Test Plan

* Test intent parsing with mock prompts.
* Test schema discovery with real Databricks tables.
* Test Neo4j insertions and Cypher queries.
* Ensure full pipeline runs end-to-end.

---

## 🔹 Step 10: Demo Script

1. Start Docker.
2. In Streamlit, type:
   *“I want to build a KG connecting customers, agreements, and payments.”*
3. System fetches Databricks table metadata → proposes schema → builds Neo4j graph.
4. Ask:
   *“Which customers have overdue payments?”*
5. System generates Cypher and displays result.

---

## 🔹 Step 11: Hackathon Submission Prep

Include:

* README with architecture diagram and description.
* Screenshot of Streamlit UI and Neo4j graph view.
* Summary of agent flow.

```

---

Would you like me to add a **sample `.env.example`** and **databricks connector string template** pre-filled with placeholders for your EDL so you can drop it directly into your environment?
```
