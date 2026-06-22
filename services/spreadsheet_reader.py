"""Excel/Spreadsheet import-export helpers for employee data.

This module keeps spreadsheet logic out of the GUI.
Supported import formats: .xlsx, .xls, .ods, .csv
Supported export formats: .xlsx, .csv
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Tuple

import pandas as pd

from services.database import get_connection
from services.employee_service import fetch_employees


# Database columns used by the employee table.
EMPLOYEE_COLUMNS: List[str] = [
    "matricule",
    "first_name",
    "last_name",
    "first_name_arabic",
    "last_name_arabic",
    "national_id",
    "date_of_birth",
    "place_of_birth",
    "place_of_birth_arabic",
]

# Friendly export headers. Import accepts these plus the aliases below.
EXPORT_HEADERS: Dict[str, str] = {
    "matricule": "Matricule",
    "first_name": "First Name",
    "last_name": "Last Name",
    "first_name_arabic": "First Name Arabic",
    "last_name_arabic": "Last Name Arabic",
    "national_id": "National ID",
    "date_of_birth": "Date Of Birth",
    "place_of_birth": "Place Of Birth",
    "place_of_birth_arabic": "Place Of Birth Arabic",
}

# Header aliases make imports tolerant to English/French/common DB names.
HEADER_ALIASES: Dict[str, str] = {
    # Matricule / employee code
    "matricule": "matricule",
    "employee_code": "matricule",
    "employee code": "matricule",
    "code": "matricule",
    "code employee": "matricule",
    "code employe": "matricule",
    "code employé": "matricule",

    # Latin names
    "first_name": "first_name",
    "first name": "first_name",
    "firstname": "first_name",
    "prenom": "first_name",
    "prénom": "first_name",
    "last_name": "last_name",
    "last name": "last_name",
    "lastname": "last_name",
    "nom": "last_name",
    "family name": "last_name",

    # Arabic names
    "first_name_arabic": "first_name_arabic",
    "first name arabic": "first_name_arabic",
    "prenom arabe": "first_name_arabic",
    "prénom arabe": "first_name_arabic",
    "first name ar": "first_name_arabic",
    "الاسم": "first_name_arabic",
    "الاسم بالعربية": "first_name_arabic",
    "last_name_arabic": "last_name_arabic",
    "last name arabic": "last_name_arabic",
    "nom arabe": "last_name_arabic",
    "last name ar": "last_name_arabic",
    "اللقب": "last_name_arabic",
    "اللقب بالعربية": "last_name_arabic",

    # Identity and birth data
    "national_id": "national_id",
    "national id": "national_id",
    "nin": "national_id",
    "n id": "national_id",
    "n° identification nationale": "national_id",
    "numero identification nationale": "national_id",
    "numéro identification nationale": "national_id",
    "date_of_birth": "date_of_birth",
    "date of birth": "date_of_birth",
    "dob": "date_of_birth",
    "birth date": "date_of_birth",
    "date naissance": "date_of_birth",
    "date de naissance": "date_of_birth",
    "place_of_birth": "place_of_birth",
    "place of birth": "place_of_birth",
    "birth place": "place_of_birth",
    "lieu naissance": "place_of_birth",
    "lieu de naissance": "place_of_birth",
    "place_of_birth_arabic": "place_of_birth_arabic",
    "place of birth arabic": "place_of_birth_arabic",
    "lieu naissance arabe": "place_of_birth_arabic",
    "lieu de naissance arabe": "place_of_birth_arabic",
    "مكان الميلاد": "place_of_birth_arabic",
}


class SpreadsheetImportError(Exception):
    """Raised when a spreadsheet cannot be read or validated."""


def _normalise_header(value: Any) -> str:
    """Convert a spreadsheet header to a comparable key."""
    text = str(value or "").strip().lower()
    text = text.replace("\ufeff", "")
    text = re.sub(r"[\n\r\t]+", " ", text)
    text = re.sub(r"[_\-./]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    direct_key = text.replace(" ", "_")
    return HEADER_ALIASES.get(text) or HEADER_ALIASES.get(direct_key) or direct_key


def _clean_value(value: Any) -> str:
    """Return a clean string, preserving IDs without adding '.0'."""
    if value is None or pd.isna(value):
        return ""

    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    text = str(value).strip()
    if text.lower() in {"nan", "nat", "none"}:
        return ""
    return text


def _clean_date(value: Any) -> str:
    """Normalise date values to yyyy-MM-dd for QDate compatibility."""
    if value is None or pd.isna(value):
        return ""

    if isinstance(value, (datetime, pd.Timestamp)):
        return value.strftime("%Y-%m-%d")

    text = _clean_value(value)
    if not text:
        return ""

    # Try common Algerian/French and ISO formats.
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass

    # Let pandas try as a final fallback, but keep the original text if unsure.
    parsed = pd.to_datetime(text, errors="coerce", dayfirst=True)
    if not pd.isna(parsed):
        return parsed.strftime("%Y-%m-%d")
    return text


def _read_dataframe(file_path: str) -> pd.DataFrame:
    """Load a spreadsheet file into a DataFrame based on extension."""
    if not os.path.exists(file_path):
        raise SpreadsheetImportError(f"File not found: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()

    try:
        if extension == ".csv":
            return pd.read_csv(file_path, dtype=object)
        if extension in {".xlsx", ".xls", ".ods"}:
            return pd.read_excel(file_path, dtype=object)
    except Exception as exc:
        raise SpreadsheetImportError(f"Could not read spreadsheet:\n{exc}") from exc

    raise SpreadsheetImportError(
        "Unsupported file type. Please use .xlsx, .xls, .ods, or .csv."
    )


def read_employees_from_spreadsheet(file_path: str) -> Tuple[List[Dict[str, str]], List[str]]:
    """Read and normalise employee rows from a spreadsheet.

    Returns:
        (employees, warnings)
    """
    df = _read_dataframe(file_path)
    warnings: List[str] = []

    if df.empty:
        raise SpreadsheetImportError("The spreadsheet is empty.")

    # Rename columns to DB column names where possible.
    column_map: Dict[Any, str] = {}
    for col in df.columns:
        key = _normalise_header(col)
        if key in EMPLOYEE_COLUMNS and key not in column_map.values():
            column_map[col] = key

    df = df.rename(columns=column_map)

    found_columns = [col for col in EMPLOYEE_COLUMNS if col in df.columns]
    if not found_columns:
        accepted = ", ".join(EXPORT_HEADERS.values())
        raise SpreadsheetImportError(
            "No valid employee columns were found. Expected headers like:\n"
            f"{accepted}"
        )

    employees: List[Dict[str, str]] = []
    for excel_index, row in df.iterrows():
        employee: Dict[str, str] = {column: "" for column in EMPLOYEE_COLUMNS}

        for column in EMPLOYEE_COLUMNS:
            if column not in df.columns:
                continue
            if column == "date_of_birth":
                employee[column] = _clean_date(row.get(column))
            else:
                employee[column] = _clean_value(row.get(column))

        # Skip fully empty spreadsheet rows.
        if not any(employee.values()):
            continue

        # Keep DB NOT NULL fields safe even when the sheet misses Arabic names.
        employee["first_name"] = employee["first_name"] or ""
        employee["last_name"] = employee["last_name"] or ""
        employee["first_name_arabic"] = employee["first_name_arabic"] or ""
        employee["last_name_arabic"] = employee["last_name_arabic"] or ""

        # A row without any identifier/name is not useful.
        if not any(
            employee[key]
            for key in ("matricule", "first_name", "last_name", "national_id")
        ):
            warnings.append(f"Row {excel_index + 2}: skipped empty/unusable row.")
            continue

        employees.append(employee)

    if not employees:
        raise SpreadsheetImportError("No employee rows could be imported.")

    return employees, warnings


def _find_existing_employee_id(conn, employee: Dict[str, str]) -> Optional[int]:
    """Find an existing employee by National ID first, then by Matricule."""
    national_id = employee.get("national_id", "").strip()
    matricule = employee.get("matricule", "").strip()

    if national_id:
        row = conn.execute(
            "SELECT id FROM employee WHERE national_id = ? LIMIT 1",
            (national_id,),
        ).fetchone()
        if row:
            return row["id"]

    if matricule:
        row = conn.execute(
            "SELECT id FROM employee WHERE matricule = ? LIMIT 1",
            (matricule,),
        ).fetchone()
        if row:
            return row["id"]

    return None


def _employee_db_values(employee: Dict[str, str]) -> Tuple[Any, ...]:
    """Build DB-safe values.

    SQLite UNIQUE allows multiple NULL values but not multiple empty strings.
    So blank national_id is stored as NULL, preventing imports from failing
    when several employees have no NIN yet.
    """
    values: List[Any] = []
    for column in EMPLOYEE_COLUMNS:
        value = employee.get(column, "")
        if column == "national_id" and not str(value).strip():
            values.append(None)
        else:
            values.append(value)
    return tuple(values)


def import_employees_from_spreadsheet(file_path: str) -> Dict[str, Any]:
    """Import employees from spreadsheet into the SQLite database.

    Existing employees are updated when the same National ID or Matricule is found.
    New employees are inserted otherwise.
    """
    employees, warnings = read_employees_from_spreadsheet(file_path)

    inserted = 0
    updated = 0
    skipped = 0

    conn = get_connection()
    try:
        for employee in employees:
            try:
                existing_id = _find_existing_employee_id(conn, employee)
                values = _employee_db_values(employee)

                if existing_id:
                    conn.execute(
                        """
                        UPDATE employee
                        SET matricule = ?,
                            first_name = ?,
                            last_name = ?,
                            first_name_arabic = ?,
                            last_name_arabic = ?,
                            national_id = ?,
                            date_of_birth = ?,
                            place_of_birth = ?,
                            place_of_birth_arabic = ?
                        WHERE id = ?
                        """,
                        values + (existing_id,),
                    )
                    updated += 1
                else:
                    conn.execute(
                        """
                        INSERT INTO employee (
                            matricule,
                            first_name,
                            last_name,
                            first_name_arabic,
                            last_name_arabic,
                            national_id,
                            date_of_birth,
                            place_of_birth,
                            place_of_birth_arabic
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        values,
                    )
                    inserted += 1
            except Exception as exc:
                skipped += 1
                warnings.append(
                    f"Skipped {employee.get('first_name', '')} {employee.get('last_name', '')}: {exc}"
                )

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    return {
        "inserted": inserted,
        "updated": updated,
        "skipped": skipped,
        "warnings": warnings,
    }


def export_employees_to_spreadsheet(file_path: str, employees: Optional[Iterable[Any]] = None) -> int:
    """Export employee data to .xlsx or .csv.

    Args:
        file_path: Destination path.
        employees: Optional iterable of sqlite3.Row/dict objects. If omitted, exports all DB employees.

    Returns:
        Number of rows exported.
    """
    if employees is None:
        employees = fetch_employees()

    rows: List[Dict[str, str]] = []
    for employee in employees:
        row: Dict[str, str] = {}
        for column in EMPLOYEE_COLUMNS:
            try:
                value = employee[column]
            except Exception:
                value = getattr(employee, column, "")
            row[EXPORT_HEADERS[column]] = _clean_value(value)
        rows.append(row)

    df = pd.DataFrame(rows, columns=[EXPORT_HEADERS[column] for column in EMPLOYEE_COLUMNS])
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".csv":
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        return len(rows)

    if extension in {"", ".xlsx"}:
        if extension == "":
            file_path += ".xlsx"
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Employees")
            worksheet = writer.sheets["Employees"]

            # Make columns readable in Excel.
            for column_cells in worksheet.columns:
                column_letter = column_cells[0].column_letter
                max_length = max(len(str(cell.value or "")) for cell in column_cells)
                worksheet.column_dimensions[column_letter].width = min(max(max_length + 2, 14), 35)

            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions

        return len(rows)

    raise SpreadsheetImportError("Export supports only .xlsx and .csv files.")


def create_employee_import_template(file_path: str) -> str:
    """Create a blank employee import template."""
    empty_row = {EXPORT_HEADERS[column]: "" for column in EMPLOYEE_COLUMNS}
    df = pd.DataFrame([empty_row], columns=list(empty_row.keys()))
    if not file_path.lower().endswith(".xlsx"):
        file_path += ".xlsx"
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Employees_Template")
    return file_path
