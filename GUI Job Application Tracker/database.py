import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "applications.db"))

def create_database():

    conn = sqlite3.connect(DB_PATH)
    print(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        position TEXT,
        status TEXT,
        basis TEXT,
        date_added TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("PRAGMA table_info(applications)")
    columns = [row[1] for row in cursor.fetchall()]
    if "basis" not in columns and "notes" in columns:
        cursor.execute("ALTER TABLE applications RENAME COLUMN notes TO basis")
    if "date_added" not in columns:
        cursor.execute("ALTER TABLE applications ADD COLUMN date_added TEXT")

    conn.commit()
    conn.close()


# ✅ CALL IT HERE (outside the function
create_database()

def add_to_database(company, position, status, basis):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO applications
    (company, position, status, basis, date_added)
    VALUES (?, ?, ?, ?, ?)
    """,
    (company, position, status, basis, date_time))

    conn.commit()

    def view_all():

     conn = sqlite3.connect("applications.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM applications"
    )

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()
    view_all()

def view_all():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications")

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()
    view_all()

def get_all_applications():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications")
        rows = cursor.fetchall()
        conn.close()
        return rows


def get_application_summary():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT status, COUNT(*) FROM applications GROUP BY status"
    )
    status_counts = dict(cursor.fetchall())

    conn.close()

    return {
        "total": total,
        "Applied": status_counts.get("Applied", 0),
        "Interview": status_counts.get("Interview", 0),
        "Offer": status_counts.get("Offer", 0),
        "Rejected": status_counts.get("Rejected", 0),
        "Active": status_counts.get("Active", 0)
    }


def search_database(company_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT company, position, status, basis
    FROM applications
    WHERE company LIKE ?
    """, (f"%{company_name}%",))
    rows = cursor.fetchall()

    conn.close()

    return rows
def update_status(company_name, new_status):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE applications
    SET status = ?
    WHERE company = ?
    """, (new_status, company_name))

    conn.commit()

    conn.close()


def update_application(application_id, company, position, status, basis):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE applications
        SET company = ?, position = ?, status = ?, basis = ?
        WHERE id = ?
        """,
        (company, position, status, basis, application_id)
    )

    conn.commit()
    conn.close()


def delete_application(application_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM applications
        WHERE id = ?
        """,
        (application_id,)
    )

    deleted_rows = cursor.rowcount

    conn.commit()
    conn.close()
    return deleted_rows

def search_applications(search_term):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM applications
        WHERE company LIKE ?
        OR position LIKE ?
        OR status LIKE ?
        """,
        (
            f"%{search_term}%",
            f"%{search_term}%",
            f"%{search_term}%"
        )
    )

    rows = cursor.fetchall()

    conn.commit()
    conn.close()
    return rows
    view_all()