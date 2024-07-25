import auth
import datetime

def insertTimeSlots():

    db = auth.auth()
    today = datetime.date.today()

    previous_day = today - datetime.timedelta(days=1)
    previous_day_date_string = previous_day.strftime('%Y-%m-%d')
    print(previous_day_date_string)

    time_slots = generate_time_slots()
    current_date = today + datetime.timedelta(21)
    current_date_string = current_date.strftime('%Y-%m-%d')
    current_date_doc_ref = db.collection('timeSlots')\
                                .document(current_date_string)\
                                .collection('availability')\
                                .document('slots')
    current_date_doc_ref.set(time_slots)

    return 'Time slots updated successfully'

# Implement your logic to generate time slots
def generate_time_slots():
    return {'08:30AM': True,
            '09:15AM': True,
            '10:00AM': True,
            '10:55AM': True,
            '11:40AM': True,
            '01:30PM': True,
            '02:15PM': True,
            '03:00PM': True,
            '03:45PM': True}

if __name__ == "__main__":
    insertTimeSlots()
