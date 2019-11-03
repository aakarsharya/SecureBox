from db import Database

def register(boxID, phoneNumber, email, password):
        if not Database.exists():
            Database.create_table(wait=True)
        newItem = Database(boxID, m_PhoneNumber=phoneNumber, m_Email=email, m_Password=password)
        newItem.save()
    
def deleteTrackingID(boxID, trackingID):
    deleteItem = Database.get(boxID)
    deleteItem.m_Orders.remove(trackingID)
    deleteItem.save()

def addTrackingID(boxID, trackingID):
    addItem = Database.get(boxID)
    addItem.m_Orders.append(trackingID)
    addItem.save()

def setLockStatus(boxID, status):
    item = Database.get(boxID)
    item.m_Locked = status
    item.save()

def getLockStatus(boxID):
    item = Database.get(hash_key=boxID, attributes_to_get=Database.m_Locked)
    return item.m_Locked