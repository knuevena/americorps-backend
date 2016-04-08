from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from db import Base, Session
from datetime import datetime
from flask import json
from orgmember import OrgMember

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(30), nullable=False)
    state = Column(String(15), nullable=False)
    zip = Column(String(5), nullable=False)
    mission = Column(String(255), nullable=False)
    poc = Column(Integer, ForeignKey('orgmembers.id'), nullable=True)

    @classmethod
    def fromdict(cls, d):
        allowed = ('name', 'address', 'city', 'state', 'zip', 'mission')
        df = {k: e for k,e in d.items() if k in allowed}
        return cls(**df)

    # all these fields are strings
    def __init__(self, name, address, city, state,
                 zip, mission, poc=None):

        # make sure th zip code is valid
        if len(zip) != 5 or not(zip.isdigit()):
            raise ValueError("a zip code must be 5 digits")
        else:
            self.zip = zip

        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.mission = mission
        self.poc = poc
        self.last_activity = datetime.now()


    def __repr__(self):
        return "Organization(%s, %s)" % (self.id, self.name)


def updateOrg(org_id, update_data):
    session = Session()
    try:
        session.query(Organization).filter_by(id=org_id).update(json.loads(update_data))
    except:
        session.rollback()
        print("here?")
        raise ValueError("id not found")
    finally:
        session.close()
        
# create an event from a json string
def createOrganization(json1):
    e = Organization.fromdict(json1)
    print(e)
    s = Session()
    try:
        s.add(e)
        s.commit()
    except:
        print("here")
        return False
    finally:
        s.close()
        return True
