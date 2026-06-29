# University Graph RAG using Neo4j and OpenRouter

## Overview

This project is a Graph Retrieval-Augmented Generation (Graph RAG) application built using **Python**, **Neo4j**, and **OpenRouter**.

The application accepts a natural language question from the user, converts it into a Cypher query using an LLM, executes the query on the Neo4j graph database, and generates a natural language answer based on the retrieved data.

---

# Features

* Natural Language Question Answering
* Automatic Cypher Query Generation
* Automatic Cypher Query Repair
* Graph Database using Neo4j
* AI-generated responses using OpenRouter
* University Sample Dataset

---

# Technologies Used

* Python 3.11
* Neo4j Graph Database
* OpenRouter API
* OpenAI Python SDK
* Pandas
* OpenPyXL

---

# Project Structure

```text
University-Graph-RAG/
│
├── graph_rag.py          # Main chatbot application
├── import_data.py        # Imports Excel data into Neo4j
├── DB Sheets.xlsx        # University dataset
├── requirements.txt      # Python dependencies
├── Dockerfile
├── README.md
└── .gitignore
```

---

# Step 1 : Clone the Repository

Open **Git Bash**, **PowerShell**, or **Command Prompt**.

Run the following command:

```bash
git clone https://github.com/Agnes-kirubakaran/University-Graph-RAG.git
```

Go inside the project folder:

```bash
cd University-Graph-RAG
```

---

# Step 2 : Install Python

Install Python 3.11 (or later).

Verify the installation:

```bash
python --version
```

Expected output:

```text
Python 3.11.x
```

---

# Step 3 : Install Required Python Packages

This project depends on several Python libraries.

Install all dependencies using:

```bash
pip install -r requirements.txt
```

This command installs:

* neo4j
* openai
* pandas
* openpyxl
* python-dotenv

Verify the installation:

```bash
pip list
```

---

# Step 4 : Install Neo4j Desktop

Download and install Neo4j Desktop.

Open Neo4j Desktop.

Create a new Local Database.

Example:

Database Name

```
UniversityDB
```

Username

```
neo4j
```

Password

```
your_password
```

Start the database.

After starting the database, note the following information:

```
URI
Username
Password
```

Example:

```
URI:
bolt://localhost:7687

Username:
neo4j

Password:
your_password
```

---

# Step 5 : Import Dataset into Neo4j

The project contains the Excel dataset:

```
DB Sheets.xlsx
```

Run:

```bash
python import_data.py
```

The script imports:

* Student
* Faculty
* Department
* Program
* Campus

into the Neo4j database.

After successful execution, all nodes and relationships will be created.

---

# Step 6 : Create a .env File

Inside the project folder, create a new file named:

```text
.env
```

Add the following values:

```env
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY

NEO4J_URI=bolt://localhost:7687

NEO4J_USER=neo4j

NEO4J_PASSWORD=YOUR_NEO4J_PASSWORD
```

Replace:

* YOUR_OPENROUTER_API_KEY
* YOUR_NEO4J_PASSWORD

with your own credentials.

---

# Step 7 : Update graph_rag.py

Ensure the project reads values from the `.env` file.

Example:

```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
```

This avoids storing sensitive credentials directly in the source code.

---

# Step 8 : Run the Application

Execute:

```bash
python graph_rag.py
```

If everything is configured correctly, you should see:

```
Neo4j Connected Successfully

OpenRouter Connected Successfully

UNIVERSITY GRAPH RAG CHATBOT
```

---

# Step 9 : Ask Questions

Example Questions:

```
List all students.

Show all departments.

Who is the faculty advisor of Student 401?

Which department has the highest number of students?

List all female faculty members.

How many students belong to each department?

Which program has the maximum students?

List faculty members working in their native campus.

Show students studying in campuses located in their native state.
```

---

# Troubleshooting

## Neo4j Connection Error

Check:

* Neo4j Desktop is running
* URI is correct
* Username is correct
* Password is correct

---

## OpenRouter Error

Verify:

* API key is valid
* Internet connection is available

---

## Python Module Error

Run:

```bash
pip install -r requirements.txt
```

again.

---

## No Data Returned

Run:

```bash
python import_data.py
```

to import the dataset into Neo4j.

---

# Docker (Optional)

Build Docker Image

```bash
docker build -t university-graph-rag .
```

Run Docker Container

```bash
docker run --env-file .env university-graph-rag
```

---

# Author

Agnes Kirubakaran
