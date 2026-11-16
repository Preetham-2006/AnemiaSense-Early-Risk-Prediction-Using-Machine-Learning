import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "anemiasense.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            ward_number REAL,
            hemoglobin REAL NOT NULL,
            rbc REAL NOT NULL,
            hematocrit REAL NOT NULL,
            wbc REAL NOT NULL,
            platelets REAL NOT NULL,
            mcv REAL NOT NULL,
            mch REAL NOT NULL,
            mchc REAL NOT NULL,
            rdw REAL NOT NULL,
            prediction TEXT NOT NULL,
            probability REAL,
            risk_level TEXT NOT NULL,
            recommendations TEXT,
            abnormal_parameters TEXT,
            doctor_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Upgrade an older database created by the previous project version.
    existing = {
        row[1] for row in conn.execute("PRAGMA table_info(reports)").fetchall()
    }
    migrations = {
        "ward_number": "ALTER TABLE reports ADD COLUMN ward_number REAL",
        "abnormal_parameters": "ALTER TABLE reports ADD COLUMN abnormal_parameters TEXT",
        "doctor_message": "ALTER TABLE reports ADD COLUMN doctor_message TEXT",
    }
    for column, sql in migrations.items():
        if column not in existing:
            conn.execute(sql)

    conn.commit()
    conn.close()


def create_user(name, email, password):
    conn = get_db()
    try:
        cursor = conn.execute(
            "INSERT INTO users(name, email, password) VALUES (?, ?, ?)",
            (name.strip(), email.strip().lower(), generate_password_hash(password)),
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def verify_user(email, password):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        (email.strip().lower(),),
    ).fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        return dict(user)
    return None


def get_user(user_id):
    conn = get_db()
    row = conn.execute(
        "SELECT id, name, email, created_at FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def update_user(user_id, name, email):
    conn = get_db()
    try:
        conn.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (name.strip(), email.strip().lower(), user_id),
        )
        conn.commit()
        return get_user(user_id)
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def save_report(user_id, data):
    conn = get_db()
    cursor = conn.execute(
        """
        INSERT INTO reports (
            user_id, ward_number, hemoglobin, rbc, hematocrit, wbc,
            platelets, mcv, mch, mchc, rdw, prediction, probability,
            risk_level, recommendations, abnormal_parameters, doctor_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            data.get("ward_number"),
            data["hemoglobin"],
            data["rbc"],
            data["hematocrit"],
            data["wbc"],
            data["platelets"],
            data["mcv"],
            data["mch"],
            data["mchc"],
            data["rdw"],
            data["prediction"],
            data.get("probability"),
            data["risk_level"],
            "||".join(data.get("recommendations", [])),
            "||".join(data.get("abnormal_parameters", [])),
            data.get("doctor_message", ""),
        ),
    )
    conn.commit()
    report_id = cursor.lastrowid
    conn.close()
    return report_id


def _decode_report(row):
    report = dict(row)
    for field in ("recommendations", "abnormal_parameters"):
        raw = report.get(field) or ""
        report[field] = [x.strip() for x in raw.split("||") if x.strip()]
    return report


def get_reports(user_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM reports WHERE user_id = ? ORDER BY datetime(created_at) DESC, id DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return [_decode_report(row) for row in rows]


def get_latest_report(user_id):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM reports WHERE user_id = ? ORDER BY datetime(created_at) DESC, id DESC LIMIT 1",
        (user_id,),
    ).fetchone()
    conn.close()
    return _decode_report(row) if row else None
