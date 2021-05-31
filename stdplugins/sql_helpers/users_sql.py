from sqlalchemy import Column, String
from stdplugins.sql_helpers import SESSION, BASE


class userlist(BASE):
    __tablename__ = "userlist"
    userId = Column(String(14), primary_key=True)
    isBanned = Column(String(100))
    dailylimit = Column(String(5))

    def __init__(self, userId, isBanned, dailylimit):
        self.userId = userId
        self.isBanned = isBanned
        self.dailylimit = dailylimit

userlist.__table__.create(checkfirst=True)


def get_user(userId):
    try:
        return SESSION.query(userlist).filter(userlist.userId == str(userId)).one()
    except:
        return None
    finally:
        SESSION.close()

def add_user(userId):
    adder = userlist(str(userId), "False", "0")
    SESSION.add(adder)
    SESSION.commit()   

def remUser(userId):
    rem = SESSION.query(userlist).get(str(userId))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()   

def get_all_users():
    rem = SESSION.query(userlist).all()
    SESSION.close()
    return rem

def updateLimit(userId):
    presentLimit = int(SESSION.query(userlist).filter(userlist.userId == str(userId)).one().dailylimit)
    print(presentLimit)
    SESSION.query(userlist).filter(userlist.userId == str(userId)).update({userlist.dailylimit : str(presentLimit + 1)})
    SESSION.commit()  
    return True

def resetDailyLimit():
    SESSION.query(userlist).update({userlist.dailylimit : "0"})
    SESSION.commit()
    return True
