import sqlite3


def create_database():

    conn = sqlite3.connect("applications.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        position TEXT,
        status TEXT,
        notes TEXT
    )
    """)

    conn.commit()
    conn.close()


# ✅ CALL IT HERE (outside the function
create_database()

def add_to_database(company, position, status, notes):

    conn = sqlite3.connect("applications.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO applications
    (company, position, status, notes)
    VALUES (?, ?, ?, ?)
    """,
    (company, position, status, notes))

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

    conn = sqlite3.connect("applications.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications")

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()
    view_all()

def get_all_applications():
        conn = sqlite3.connect("applications.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications")
        rows = cursor.fetchall()
        conn.close()
        return rows

def search_database(company_name):
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT company, position, status, notes
    FROM applications
    WHERE company LIKE ?
    """, (f"%{company_name}%",))
    rows = cursor.fetchall()

    conn.close()

    return rows
def update_status(company_name, new_status):

    conn = sqlite3.connect("applications.db")

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE applications
    SET status = ?
    WHERE company = ?
    """, (new_status, company_name))

    conn.commit()

    conn.close()

def delete_application(company_name):
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM applications
    WHERE company = ?
    """, (company_name,))

    deleted_rows = cursor.rowcount

    conn.commit()
    conn.close()
    return deleted_rows