# services/employee_service.py
import sqlite3

from services.database import get_connection

def fetch_employees():
    """Fetches all active employees along with their basic contract and salary data."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Left joins ensure employees show up even if they don't have a contract yet
    query = "SELECT * FROM employee"
    
    try:
        cursor.execute(query)
        # Returns a list of sqlite3.Row objects which behave like dictionaries
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error during fetch: {e}")
        return []
    finally:
        conn.close()