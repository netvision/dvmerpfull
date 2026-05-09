import sqlite3
conn = sqlite3.connect('lesson_plans.db')
conn.execute("UPDATE alembic_version SET version_num='b4b583b7c1e2'")
conn.commit()
