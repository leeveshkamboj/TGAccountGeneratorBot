from sqlalchemy import Column, String
from stdplugins.sql_helpers import SESSION, BASE


class hits(BASE):
    __tablename__ = "hits"
    hit = Column(String(200), primary_key=True)

    def __init__(self, hit):
        self.hit = hit


hits.__table__.create(checkfirst=True)


def hitExists(hit):
    try:
        if SESSION.query(hits).filter(hits.hit == str(hit)).one():
            return True
    except:
        return False
    finally:
        SESSION.close()

def addHit(hit):
    adder = hits(str(hit))
    SESSION.add(adder)
    SESSION.commit()


def remHit(hit):
    rem = SESSION.query(hits).get(str(hit))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def get_all_hits():
    rem = SESSION.query(hits).all()
    SESSION.close()
    return rem