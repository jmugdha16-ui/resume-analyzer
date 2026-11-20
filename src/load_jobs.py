from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "DataEngineer.csv"
DB = ROOT / "data" / "jobs.db"

df = pd.read_csv(CSV)

# Step 3: sirf Data Engineer jobs rakho
jobs = df[df["Job Title"].str.contains("data engineer", case=False, na=False)].copy()
print("After filter:", len(jobs))

# Step 4: saaf karo
jobs["company"] = jobs["Company Name"].str.split("\n").str[0].str.strip()
jobs = jobs.rename(columns={
    "Job Title": "title",
    "Location": "location",
    "Job Description": "description",
})
jobs = jobs[["title", "company", "location", "description"]]
jobs = jobs.dropna(subset=["description"])
jobs["description"] = jobs["description"].str.strip()
jobs = jobs[jobs["description"].str.len() > 100]
jobs = jobs.drop_duplicates(subset=["description"]).reset_index(drop=True)
jobs.insert(0, "job_id", jobs.index + 1)
jobs["source"] = "glassdoor_us"
print("After cleaning:", jobs.shape)

# Step 5: SQLite me load karo
conn = sqlite3.connect(DB)
jobs.to_sql("jobs", conn, if_exists="replace", index=False)

# Step 6: pehli SQL queries
print(pd.read_sql("SELECT COUNT(*) AS total FROM jobs", conn))

print(pd.read_sql("""
    SELECT company, COUNT(*) AS n
    FROM jobs
    GROUP BY company
    ORDER BY n DESC
    LIMIT 10
""", conn))

print(pd.read_sql("""
    SELECT location, COUNT(*) AS n
    FROM jobs
    GROUP BY location
    ORDER BY n DESC
    LIMIT 10
""", conn))

conn.close()