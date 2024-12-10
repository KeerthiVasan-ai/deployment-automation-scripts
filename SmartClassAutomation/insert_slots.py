import auth
import datetime

def insertTimeSlots():

    db = auth.auth()
    today = datetime.date.today()

    # for i in range(21):

    current_date = today + datetime.timedelta(21)
    isTargetDay = is_target_day(current_date)
    time_slots = generate_time_slots(isTargetDay)
    current_date_string = current_date.strftime('%Y-%m-%d')
    current_date_doc_ref = db.collection('timeSlots')\
                            .document(current_date_string)\
                            .collection('availability')\
                            .document('slots')
    current_date_doc_ref.set(time_slots)
    print(current_date)
    return 'Time slots updated successfully'

def is_target_day(date):
    return date.weekday() in (1, 2, 3)

def generate_time_slots(isTargetDay):
    if isTargetDay:
        return {'08:30AM': True,
                '09:15AM': True,
                '10:00AM': True,
                '10:55AM': True,
                '11:40AM': True,
                '01:30PM': False,
                '02:15PM': False,
                '03:00PM': False,
                '03:45PM': False
                }
    else:
        return {
            '08:30AM': True,
            '09:15AM': True,
            '10:00AM': True,
            '10:55AM': True,
            '11:40AM': True,
            '01:30PM': True,
            '02:15PM': True,
            '03:00PM': True,
            '03:45PM': True
            }

if __name__ == "__main__":
    insertTimeSlots()
