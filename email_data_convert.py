"""Convert the project's sample email workbook into structured JSON."""

import json
import re
from pathlib import Path

from openpyxl import load_workbook


PROJECT_DIR = Path(__file__).resolve().parent
INPUT_FILE = PROJECT_DIR / "sample_email_data.xlsx"
OUTPUT_FILE = PROJECT_DIR / "emails.json"
FIELD_PATTERN = re.compile(r'^(from|to|subject|body)\s*"?\s*:\s?(.*)$', re.IGNORECASE)
OUTPUT_FIELDS = ("From", "To", "Subject", "Body")


def parse_email(email_sample: str) -> dict[str, str]:
    """Extract labelled From, To, Subject, and Body values from one email."""
    email = {field: "" for field in OUTPUT_FIELDS}
    active_field: str | None = None

    for line in email_sample.splitlines():
        match = FIELD_PATTERN.match(line)
        if match:
            active_field = match.group(1).title()
            email[active_field] = match.group(2)
        elif active_field:
            email[active_field] += "\n" + line

    return email


def convert_emails(input_file: Path = INPUT_FILE, output_file: Path = OUTPUT_FILE) -> int:
    """Read workbook rows and save the requested structured email JSON."""
    workbook = load_workbook(input_file, read_only=True, data_only=True)
    worksheet = workbook.active
    emails = []

    for row in worksheet.iter_rows(min_row=2, values_only=True):
        # Formatted blank rows may be returned as an empty or single-cell tuple.
        if len(row) < 2:
            continue

        email_id, email_sample = row[:2]
        if email_id is None or email_sample is None:
            continue

        normalized_id = int(email_id) if isinstance(email_id, float) and email_id.is_integer() else email_id
        emails.append({"emailId": normalized_id, **parse_email(str(email_sample))})

    output_file.write_text(json.dumps(emails, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(emails)


#def main() -> None:
count = convert_emails()
print(f"Converted {count} emails to {OUTPUT_FILE.name}")


#if __name__ == "__main__":
 #   main()
