import csv
import os
from datetime import datetime


HISTORY_FILE = "scan_history.csv"


def save_scan(score, final_status, missing_fields):

    # Get current date and time
    scan_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    # Convert missing fields list into text
    if missing_fields:
        missing_text = ", ".join(missing_fields)
    else:
        missing_text = "None"


    # Check if CSV file already exists
    file_exists = os.path.isfile(HISTORY_FILE)


    # Open CSV file
    with open(
        HISTORY_FILE,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)


        # Create headings if file is new
        if not file_exists:

            writer.writerow([
                "Scan Date & Time",
                "Compliance Score",
                "Status",
                "Missing Requirements"
            ])


        # Save scan data
        writer.writerow([
            scan_time,
            f"{score:.0f}%",
            final_status,
            missing_text
        ])


def get_history():

    # If history file doesn't exist
    if not os.path.exists(HISTORY_FILE):
        return []


    history = []


    # Read CSV file
    with open(
        HISTORY_FILE,
        mode="r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            history.append(row)


    # Return latest scans first
    return history[::-1]