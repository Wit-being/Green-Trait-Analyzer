import sqlite3
import json

conn = sqlite3.connect("green_users.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM user_traits")
rows = cursor.fetchall()
for row in rows:
    print(f"User ID: {row[0]}")
    print(
        f"Scores: empathy={row[1]}, narcissism={row[2]}, growth_mindset={row[3]}, emotional_maturity={row[4]}, openness_to_difference={row[5]}"
    )
    print(f"Answers: {json.loads(row[6])}")
    print(f"Timestamp: {row[7]}\n")
conn.close()
