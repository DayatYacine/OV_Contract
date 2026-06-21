import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "hr_contracts.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matricule TEXT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    first_name_arabic TEXT NOT NULL,
    last_name_arabic TEXT NOT NULL,
    national_id TEXT UNIQUE,
    date_of_birth TEXT,   -- Stored as 'DD-MM-YYYY'
    place_of_birth TEXT,  -- Communes / Wilayas format
    place_of_birth_arabic TEXT  -- Communes / Wilayas format
);

CREATE TABLE IF NOT EXISTS contract (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    contract_type TEXT CHECK(contract_type IN ('CDD', 'CDI', 'D', 'DP')),
    start_date TEXT NOT NULL,
    end_date TEXT, -- Can be NULL for CDI, D, DP
    salary_grid_id INTEGER,
    FOREIGN KEY(employee_id) REFERENCES employees(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS salary_grid (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category INTEGER NOT NULL CHECK(category BETWEEN 1 AND 20),
    class_level INTEGER NOT NULL CHECK(class_level BETWEEN 1 AND 10),
    base_salary_amount REAL NOT NULL,
    UNIQUE(category, class_level) -- Prevents duplicate entries for the same cell
);

CREATE TABLE IF NOT EXISTS step_progression_rules (
    current_class INTEGER PRIMARY KEY CHECK(current_class BETWEEN 1 AND 9),
    years_required INTEGER NOT NULL, -- E.g., 3 years for Class 1->2, 2 years for Class 3->4
    raise_multiplier REAL DEFAULT 1.0
);

CREATE TABLE IF NOT EXISTS bonus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    default_amount REAL DEFAULT 0.0  -- Standard baseline value
);

CREATE TABLE IF NOT EXISTS contract_bonus (
    contract_id INTEGER,
    bonus_id INTEGER,
    custom_amount REAL,              -- Overrides default_amount if a specific contract pays differently
    PRIMARY KEY (contract_id, bonus_id),
    FOREIGN KEY(contract_id) REFERENCES contract(id) ON DELETE CASCADE,
    FOREIGN KEY(bonus_id) REFERENCES bonus(id) ON DELETE CASCADE
);
"""

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = NO;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database file and executes the schema script."""
    conn = get_connection()
    try:
        # executescript allows running multiple SQL statements separated by semicolons
        conn.executescript(SCHEMA)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
    finally:
        conn.close()