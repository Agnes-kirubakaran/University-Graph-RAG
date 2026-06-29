from neo4j import GraphDatabase
from openai import OpenAI
import json



OPENROUTER_API_KEY = "YOUR_API_KEY"

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "YOUR_PASSWORD"

MODEL = "openai/gpt-4o-mini"



client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)



driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


SCHEMA = """
University Graph Database

Labels:

Student
Faculty
Department
Program
Campus

Relationships:

(Student)-[:BELONGS_TO]->(Department)

(Student)-[:ENROLLED_IN]->(Program)

(Student)-[:ADVISED_BY]->(Faculty)

(Department)-[:LOCATED_IN]->(Campus)

(Program)-[:OFFERED_BY]->(Department)

(Faculty)-[:WORKS_IN]->(Department)

Properties:

Student:
rollNo
name
departmentID
programID
dob
doj
country
state
city
facultyAdvisor
gender

Faculty:
employeeID
name
education
country
state
city
expertise
experience
gender

Department:
departmentID
departmentName
campusID

Program:
programID
programName
duration
departmentID

Campus:
campusID
campusName
location

ID Formats:

Student:
STU0001

Faculty:
FAC001

Department:
DEPT01

Program:
PROG01

Campus:
CAM001

Gender Values (case-sensitive, use exactly as shown):
Male
Female

Never use 'male' or 'female' (lowercase). Always use 'Male' or 'Female'.

Rules:

1. Return ONLY Cypher query.
2. No explanation.
3. No markdown.
4. Use relationship traversal whenever possible.
5. Use count() for aggregation.
6. Use ORDER BY DESC LIMIT 1 for highest questions.
7. Use exact property names.
8. Use exact labels and relationships.
9. Always return specific properties, never return full nodes.
   Wrong:  RETURN s
   Correct: RETURN s.name AS studentName
   Wrong:  RETURN f
   Correct: RETURN f.name AS facultyName
"""


def fix_cypher(cypher):
    # Fix gender case
    cypher = cypher.replace("'female'", "'Female'")
    cypher = cypher.replace("'male'", "'Male'")
    cypher = cypher.replace('"female"', '"Female"')
    cypher = cypher.replace('"male"', '"Male"')

    # Fix bare node returns
    cypher = cypher.replace("RETURN s\n", "RETURN s.name AS studentName\n")
    cypher = cypher.replace("RETURN s ", "RETURN s.name AS studentName ")
    cypher = cypher.replace("RETURN s,", "RETURN s.name AS studentName,")
    if cypher.endswith("RETURN s"):
        cypher = cypher[:-8] + "RETURN s.name AS studentName"

    cypher = cypher.replace("RETURN f\n", "RETURN f.name AS facultyName\n")
    cypher = cypher.replace("RETURN f ", "RETURN f.name AS facultyName ")
    if cypher.endswith("RETURN f"):
        cypher = cypher[:-8] + "RETURN f.name AS facultyName"

    cypher = cypher.replace("RETURN d\n", "RETURN d.departmentName AS departmentName\n")
    cypher = cypher.replace("RETURN d ", "RETURN d.departmentName AS departmentName ")
    if cypher.endswith("RETURN d"):
        cypher = cypher[:-8] + "RETURN d.departmentName AS departmentName"

    cypher = cypher.replace("RETURN p\n", "RETURN p.programName AS programName\n")
    cypher = cypher.replace("RETURN p ", "RETURN p.programName AS programName ")
    if cypher.endswith("RETURN p"):
        cypher = cypher[:-8] + "RETURN p.programName AS programName"

    cypher = cypher.replace("RETURN c\n", "RETURN c.campusName AS campusName\n")
    cypher = cypher.replace("RETURN c ", "RETURN c.campusName AS campusName ")
    if cypher.endswith("RETURN c"):
        cypher = cypher[:-8] + "RETURN c.campusName AS campusName"

    return cypher


def generate_cypher(question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SCHEMA
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    cypher = response.choices[0].message.content.strip()
    cypher = cypher.replace("```cypher", "")
    cypher = cypher.replace("```", "")
    cypher = cypher.strip()
    cypher = fix_cypher(cypher)

    return cypher


def execute_query(question, cypher_query):

    records = []

    max_retries = 3
    current_query = cypher_query

    for attempt in range(max_retries):

        try:

            print(f"\nAttempt {attempt+1}")

            with driver.session() as session:

                result = session.run(current_query)

                records = [dict(record) for record in result]

            print("Query Executed Successfully")

            if len(records) == 0:

                print("No records returned. Trying repair...")

                repair_response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": f"""
You are a Neo4j expert.

Schema:

{SCHEMA}

The query executed successfully but returned no records.

Check whether:
1. Wrong ID format used.
2. Wrong gender case used (must be 'Male' or 'Female').
3. Wrong property used.
4. Wrong relationship direction used.

Return ONLY corrected Cypher.
Never return full nodes - always return specific properties.
"""
                        },
                        {
                            "role": "user",
                            "content": f"""
Question:

{question}

Query:

{current_query}
"""
                        }
                    ],
                    temperature=0
                )

                repaired_query = repair_response.choices[0].message.content.strip()
                repaired_query = repaired_query.replace("```cypher", "")
                repaired_query = repaired_query.replace("```", "")
                repaired_query = repaired_query.strip()
                repaired_query = fix_cypher(repaired_query)

                if repaired_query != current_query:

                    print("\nTrying repaired query...")
                    print(repaired_query)

                    with driver.session() as session:

                        result = session.run(repaired_query)

                        records = [dict(record) for record in result]

            return records

        except Exception as e:

            error_message = str(e)

            print("\nQuery Failed")
            print(error_message)

            if attempt == max_retries - 1:

                raise Exception(error_message)

            print("\nAsking AI to repair query...")

            repair_response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": f"""
You are a Neo4j Cypher expert.

Schema:

{SCHEMA}

Fix the query.

Rules:
1. Return ONLY Cypher.
2. No explanation.
3. No markdown.
4. Use valid Neo4j syntax.
5. Never return full nodes - always return specific properties.
"""
                    },
                    {
                        "role": "user",
                        "content": f"""
Original Query:

{current_query}

Neo4j Error:

{error_message}
"""
                    }
                ],
                temperature=0
            )

            current_query = repair_response.choices[0].message.content.strip()
            current_query = current_query.replace("```cypher", "")
            current_query = current_query.replace("```", "")
            current_query = current_query.strip()
            current_query = fix_cypher(current_query)

            print("\nRepaired Query:")
            print(current_query)

    return records


def generate_answer(question, records):

    if len(records) == 0:
        return "No matching data found."

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are a university assistant.

Rules:

1. Answer ONLY using database result.
2. Do not invent information.
3. Keep answer clear and concise.
4. If multiple rows exist, summarize properly.
"""
            },
            {
                "role": "user",
                "content": f"""
Question:

{question}

Database Result:

{json.dumps(records, indent=2)}
"""
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


def chatbot():

    print("\n" + "="*60)
    print("UNIVERSITY GRAPH RAG CHATBOT")
    print("="*60)
    print("Type 'exit' to quit\n")

    while True:

        question = input("Ask Question: ").strip()

        if question.lower() in ["exit", "quit"]:
            break

        try:

            print("\n====================")
            print("Generated Cypher")
            print("====================")

            cypher_query = generate_cypher(question)

            print(cypher_query)

            if not (
                cypher_query.upper().startswith("MATCH")
                or cypher_query.upper().startswith("OPTIONAL MATCH")
                or cypher_query.upper().startswith("WITH")
            ):
                print("\nInvalid query generated.")
                continue

            print("\n====================")
            print("Database Result")
            print("====================")

            records = execute_query(
                question,
                cypher_query
            )

            print(json.dumps(records, indent=2))

            print("\n====================")
            print("Final Answer")
            print("====================")

            answer = generate_answer(
                question,
                records
            )

            print(answer)

            print("\n" + "-"*60 + "\n")

        except Exception as e:

            print("\nERROR:")
            print(str(e))
            print("\n" + "-"*60 + "\n")


def main():

    try:

        driver.verify_connectivity()

        print("Neo4j Connected Successfully")
        print("OpenRouter Connected Successfully")

        chatbot()

    except Exception as e:

        print("Startup Error:")
        print(str(e))

    finally:

        driver.close()


if __name__ == "__main__":
    main()