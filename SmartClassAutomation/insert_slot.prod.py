import auth
import datetime


def insert_time_slots(days_from_today: int = 21):
    """
    Inserts time slots into Firestore for a date N days from today.
    """
    db = auth.auth()
    target_date = datetime.date.today() + datetime.timedelta(days=days_from_today)
    target_date_str = target_date.strftime('%Y-%m-%d')
    
    isTarget = is_target_day(target_date)
    
    time_slots = generate_time_slots(isTarget)

    # Reference to the Firestore document
    slot_doc_ref = (
        db.collection('timeSlots')
          .document(target_date_str)
          .collection('availability')
          .document('slots')
    )

    # Set time slots in Firestore
    slot_doc_ref.set(time_slots)
    print(f"✅ Time slots inserted for {target_date_str}")
    return 'Time slots updated successfully'

def is_target_day(date):
    return date.weekday() in (0, 1, 2, 3)

def generate_time_slots(isTarget):
    """
    Returns the default time slots dictionary.
    """
    if(isTarget):
        return {
            '08:30AM': True,
            '09:30AM': True,
            '10:40AM': True,
            '11:40AM': True,
            '01:30PM': False,
            '02:30PM': False,
            '03:30PM': False,
        }
    else: 
        return {
            '08:30AM': True,
            '09:30AM': True,
            '10:40AM': True,
            '11:40AM': True,
            '01:30PM': True,
            '02:30PM': True,
            '03:30PM': True,
        }


if __name__ == "__main__":
    insert_time_slots()
