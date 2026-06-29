import pandas as pd
from neo4j import GraphDatabase

# =========================
# CONFIG
# =========================

EXCEL_FILE = "Neo4j_Database_Sheets.xlsx"

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "userpassword"

# =========================
# CONNECT
# =========================

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

# =========================
# READ EXCEL
# =========================

print("Reading Excel...")

campus_df = pd.read_excel(EXCEL_FILE, sheet_name="Campus Master")
dept_df = pd.read_excel(EXCEL_FILE, sheet_name="Department Master")
program_df = pd.read_excel(EXCEL_FILE, sheet_name="Program Master")
faculty_df = pd.read_excel(EXCEL_FILE, sheet_name="Faculty Master")
student_df = pd.read_excel(EXCEL_FILE, sheet_name="Student")

# =========================
# CLEAR DATABASE
# =========================

with driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")

print("Old data deleted.")

# =========================
# CAMPUS
# =========================

with driver.session() as session:

    for _, row in campus_df.iterrows():

        session.run("""
        CREATE (:Campus{
            campusID:$id,
            campusName:$name,
            location:$loc
        })
        """,
        id=str(row["Campus ID"]),
        name=str(row["Campus Name"]),
        loc=str(row["Location"])
        )

print("Campus Imported")

# =========================
# DEPARTMENT
# =========================

with driver.session() as session:

    for _, row in dept_df.iterrows():

        session.run("""
        CREATE (:Department{
            departmentID:$id,
            departmentName:$name,
            campusID:$campus
        })
        """,
        id=str(row["Department ID"]),
        name=str(row["Department Name"]),
        campus=str(row["Campus ID"])
        )

print("Department Imported")

# =========================
# PROGRAM
# =========================

with driver.session() as session:

    for _, row in program_df.iterrows():

        session.run("""
        CREATE (:Program{
            programID:$id,
            programName:$name,
            duration:$duration,
            departmentID:$dept
        })
        """,
        id=str(row["Program ID"]),
        name=str(row["Program Name"]),
        duration=int(row["Duration (Years)"]),
        dept=str(row["Department ID"])
        )

print("Program Imported")

# =========================
# FACULTY
# =========================

with driver.session() as session:

    for _, row in faculty_df.iterrows():

        session.run("""
        CREATE (:Faculty{
            employeeID:$id,
            name:$name,
            education:$education,
            country:$country,
            state:$state,
            city:$city,
            expertise:$expertise,
            experience:$experience,
            gender:$gender
        })
        """,
        id=str(row["Employee ID"]),
        name=str(row["Name"]),
        education=str(row["Education"]),
        country=str(row["Country"]),
        state=str(row["State"]),
        city=str(row["City"]),
        expertise=str(row["Expertise"]),
        experience=int(row["Experience (Years)"]),
        gender=str(row["Gender"])
        )

print("Faculty Imported")

# =========================
# STUDENTS
# =========================

with driver.session() as session:

    for _, row in student_df.iterrows():

        session.run("""
        CREATE (:Student{
            rollNo:$roll,
            name:$name,
            departmentID:$dept,
            programID:$program,
            dob:$dob,
            doj:$doj,
            country:$country,
            state:$state,
            city:$city,
            facultyAdvisor:$advisor,
            gender:$gender
        })
        """,
        roll=str(row["Roll Number"]),
        name=str(row["Name"]),
        dept=str(row["Department ID"]),
        program=str(row["Program ID"]),
        dob=str(row["Date of Birth"]),
        doj=str(row["Date of Joining"]),
        country=str(row["Native Country"]),
        state=str(row["Native State"]),
        city=str(row["Native City"]),
        advisor=str(row["Faculty Advisor"]),
        gender=str(row["Gender"])
        )

print("Students Imported")

# =========================
# RELATIONSHIPS
# =========================

with driver.session() as session:

    session.run("""
    MATCH (s:Student),(d:Department)
    WHERE s.departmentID=d.departmentID
    CREATE (s)-[:BELONGS_TO]->(d)
    """)

    session.run("""
    MATCH (s:Student),(p:Program)
    WHERE s.programID=p.programID
    CREATE (s)-[:ENROLLED_IN]->(p)
    """)

    session.run("""
    MATCH (s:Student),(f:Faculty)
    WHERE s.facultyAdvisor=f.name
    CREATE (s)-[:ADVISED_BY]->(f)
    """)

    session.run("""
    MATCH (d:Department),(c:Campus)
    WHERE d.campusID=c.campusID
    CREATE (d)-[:LOCATED_IN]->(c)
    """)

    session.run("""
    MATCH (p:Program),(d:Department)
    WHERE p.departmentID=d.departmentID
    CREATE (p)-[:OFFERED_BY]->(d)
    """)

    session.run("""
    MATCH (s:Student)-[:ADVISED_BY]->(f:Faculty)
    MATCH (s)-[:BELONGS_TO]->(d:Department)
    WITH DISTINCT f,d
    CREATE (f)-[:WORKS_IN]->(d)
    """)

print("Relationships Created")

# =========================
# VERIFY
# =========================

with driver.session() as session:

    result = session.run("""
    MATCH (n)
    RETURN labels(n)[0] AS label,
           count(*) AS total
    """)

    print("\nNode Counts\n")

    for row in result:
        print(row["label"], ":", row["total"])

driver.close()

print("\nImport Completed Successfully")
