import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import re
import json

# Initialize Firebase
cred = credentials.Certificate("D:\\deployment-automation-scripts\\SmartClassAutomation\\smartreserve.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Log file path
log_file_path = "old_bookings_log_date_specific_06_07.txt"

# Date setup
current_year = datetime.now().year
last_year = current_year - 1

# Match date format DD-MM-YYYY
date_pattern = re.compile(r"\d{2}-\d{2}-\d{4}")

def log_and_delete_old_bookings():
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"\n===== Log Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====\n")

        date_docs = db.collection("bookingDetails").list_documents()

        for date_doc_ref in date_docs:
            date_str = date_doc_ref.id

            if not date_pattern.match(date_str):
                log_file.write(f"Skipped (Invalid Date Format): {date_str}\n")
                continue

            try:
                booking_date = datetime.strptime(date_str, "%d-%m-%Y")
            except ValueError:
                log_file.write(f"Skipped (Unparsable Date): {date_str}\n")
                continue

            # Check for Jan–June of the previous year
            # if booking_date.year == last_year and 1 <= booking_date.month <= 6:
            print(f"Checking old bookings for: {date_str}")
            bookings = date_doc_ref.collection("booking").get()

            for booking_doc in bookings:
                booking_id = booking_doc.id
                booking_data = booking_doc.to_dict()

                log_file.write(f"\nDeleting Booking:\n")
                log_file.write(f"Path: bookingDetails/{date_str}/booking/{booking_id}\n")
                log_file.write(f"Data: {json.dumps(booking_data, indent=2)}\n")

                # Delete the booking
                date_doc_ref.collection("booking").document(booking_id).delete()
                print(f"Deleted: {date_str}/{booking_id}")

        log_file.write(f"===== Log End: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====\n")

log_and_delete_old_bookings()
