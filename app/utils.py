from . import WasteCollection, db
def schedule_collection(user_id, date, time):
    # Check for existing schedules on the same date and time
    conflicts = WasteCollection.query.filter_by(date=date, time=time).count()
    if conflicts == 0:
        new_collection = WasteCollection(user_id=user_id, date=date, time=time, status='scheduled')
        db.session.add(new_collection)
        db.session.commit()
        return True
    return False
