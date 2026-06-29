# University Graph RAG using Neo4j and OpenRouter

## Overview

This project is a **Graph Retrieval-Augmented Generation (Graph RAG)** application built using **Python**, **Neo4j**, and **OpenRouter**.

The application allows users to ask questions in natural language. The system converts the question into a Cypher query using an LLM, executes the query on the Neo4j Graph Database, retrieves the required information, and generates a natural language response.

---

# Features

- Natural Language Question Answering
- Automatic Cypher Query Generation
- Automatic Cypher Query Repair
- Graph Database using Neo4j
- AI-generated Responses
- University Sample Dataset
- Graph RAG Pipeline

---

# Technologies Used

- Python 3.11
- Neo4j Graph Database
- OpenRouter API
- OpenAI Python SDK
- Pandas
- OpenPyXL

---

# Project Structure

```
University-Graph-RAG/
│
├── graph_rag.py              # Main chatbot application
├── import_data.py            # Import Excel data into Neo4j
├── DB Sheets.xlsx            # University dataset
├── requirements.txt          # Python dependencies
├── Dockerfile
├── README.md
└── .gitignore
```

---

# Prerequisites

Before running this project, install the following software:

- Python 3.11 or later
- Git
- Neo4j Desktop
- Docker Desktop (Optional)

---

# Step 1 : Clone the Repository

Open Git Bash, PowerShell, or Command Prompt.

Run:

```bash
git clone https://github.com/Agnes-kirubakaran/University-Graph-RAG.git
```

Go inside the project folder.

```bash
cd University-Graph-RAG
```

---

# Step 2 : Install Python

Download Python from

https://www.python.org/downloads/

Verify installation:

```bash
python --version
```

Expected Output

```
Python 3.11.x
```

---

# Step 3 : Install Git

Download Git from

https://git-scm.com/downloads

Verify installation.

```bash
git --version
```

Expected Output

```
git version 2.xx.x.windows.x
```

---

# Step 4 : Install Neo4j Desktop

Download Neo4j Desktop

https://neo4j.com/download/

Install Neo4j Desktop.

Open Neo4j Desktop.

Create a New Local Database.

Example

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

Click **Start Database**.

After starting the database, note the following:

```
URI
Username
Password
```

Example

```
URI
bolt://localhost:7687

Username
neo4j

Password
your_password
```

---

# Step 5 : Create an OpenRouter Account

Go to

https://openrouter.ai

Click **Sign Up**.

Create an account using

- Google Account

or

- Email Address

Verify your account.

---

# Step 6 : Generate an OpenRouter API Key

After logging in,

Open Dashboard.

Click

**Keys**

or

**API Keys**

Click

**Create Key**

Give any name.

Example

```
UniversityGraphRAG
```

Copy the generated API Key.

Example

```
sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Keep the API key private.

Do not upload it to GitHub.

---

# Step 7 : Create a .env File

Inside the project folder create a new file named

```
.env
```

Add the following values.

```env
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY

NEO4J_URI=bolt://localhost:7687

NEO4J_USER=neo4j

NEO4J_PASSWORD=YOUR_PASSWORD
```

Replace

- YOUR_OPENROUTER_API_KEY
- YOUR_PASSWORD

with your own credentials.

---

# Step 8 : Install Python Dependencies

Install all required Python packages.

```bash
pip install -r requirements.txt
```

This installs

- neo4j
- openai
- pandas
- openpyxl
- python-dotenv

Verify installation.

```bash
pip list
```

---

# Step 9 : Import Dataset into Neo4j

The project includes the dataset

```
DB Sheets.xlsx
```

Run

```bash
python import_data.py
```

This script imports

- Student
- Faculty
- Department
- Program
- Campus

into Neo4j.

Wait until the import completes successfully.

---

# Step 10 : Configure graph_rag.py

Ensure your application loads the credentials from the `.env` file.

Example

```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
```

---

# Step 11 : Run the Application

Run

```bash
python graph_rag.py
```

If everything is configured correctly you should see

```
Neo4j Connected Successfully

OpenRouter Connected Successfully

UNIVERSITY GRAPH RAG CHATBOT
```

---

# Step 12 : Ask Questions

Example Questions

```
List all students.

Show all departments.

Who is the faculty advisor of Student 401?

List all faculty members.

How many students belong to each department?

Which department has the highest number of students?

List all female faculty members.

Which program has the maximum number of students?

Show students studying in campuses located in their native state.

List faculty members working in campuses located in their native place.
```

---

# Docker (Optional)

## Build Docker Image

```bash
docker build -t university-graph-rag .
```

## Run Docker Container

```bash
docker run --env-file .env university-graph-rag
```

---

# Troubleshooting

## Neo4j Connection Error

Check:

- Neo4j Desktop is running
- URI is correct
- Username is correct
- Password is correct

---

## OpenRouter Error

Check:

- API key is valid
- Internet connection is available

---

## Python Module Error

Run

```bash
pip install -r requirements.txt
```

again.

---

## No Data Returned

Run

```bash
python import_data.py
```

again to import the dataset.

---

# Notes

- Ensure Neo4j Desktop is running before executing the application.
- Replace the placeholder API key and Neo4j password with your own credentials.
- Never upload your API key or passwords to GitHub.
- Keep your `.env` file private.

---

# Future Improvements

- Docker Deployment
- Jenkins CI/CD Pipeline
- Graph Visualization
- Web-based User Interface
- Cloud Deployment

---

# Author

**Agnes Kirubakaran**

University Graph RAG using Neo4j and OpenRouter.
