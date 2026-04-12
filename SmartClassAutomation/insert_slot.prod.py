import auth # Ensure your firebase admin is initialized here
import datetime


def insert_time_slots(days_from_today: int = 21):
    """
    Inserts time slots into Firestore for a date N days from today.
    It fetches all configuration dynamically from Firebase.
    """
    db = auth.auth()
    target_date = datetime.date.today() + datetime.timedelta(days=days_from_today)
    target_date_str = target_date.strftime('%Y-%m-%d')
    
    time_slots = {}
    
    try:
        # Fetch configurations natively from Firebase
        config_ref = db.collection('slotConfigurations').document('globalSlots').get()
        if config_ref.exists:
            global_config = config_ref.to_dict()
            
            # Iso weekday gives 1 for Monday, 7 for Sunday (matching Dart)
            target_weekday = str(target_date.isoweekday())
            weekday_config = global_config.get(target_weekday, {})
            
            # Parse the json and sort exactly by the order field
            slot_items = []
            for slot_time, config in weekday_config.items():
                if isinstance(config, dict):
                    enabled_flag = config.get('enabled', True) # default to true if missing
                    order_val = config.get('order', 99)
                    try:
                        order_val = int(order_val)
                    except (ValueError, TypeError):
                        order_val = 99
                    
                    slot_items.append({
                        'time': slot_time,
                        'enabled': bool(enabled_flag),
                        'order': order_val
                    })
            
            # Sort securely by the order field
            slot_items.sort(key=lambda x: x['order'])
            
            # Reconstruct the time_slots dict (Python 3.7+ preserves insertion order)
            for item in slot_items:
                time_slots[item['time']] = item['enabled']
        else:
            print("⚠️ globalSlots document does not exist. No slots will be created.")
            return 'Failed: No global config'
            
    except Exception as e:
        print(f"⚠️ Could not fetch global slots config. Error: {e}")
        return 'Failed: Exception fetching config'

    if not time_slots:
        print("⚠️ Extracted time_slots dictionary is empty. Skipping.")
        return 'Failed: No valid slots parsed'

    print(time_slots)
    # Reference to the Firestore document for N+21 days
    slot_doc_ref = (
        db.collection('timeSlots')
          .document(target_date_str)
          .collection('availability')
          .document('slots')
    )

    # Set dynamic time slots in Firestore
    slot_doc_ref.set(time_slots)
    print(f"✅ Time slots inserted successfully for {target_date_str} based on global configuration.")
    return 'Time slots updated successfully'

if __name__ == "__main__":
    insert_time_slots()

