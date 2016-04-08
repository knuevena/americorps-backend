from user import User
from db import Base, Session
from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker
from datetime import datetime
from attendee import Attendee
from werkzeug.security import generate_password_hash, check_password_hash
from flask import json
from sqlalchemy import exc
import organization


class OrgMember(User):
    __tablename__ = "orgmembers"
    __mapper_args__ = {'polymorphic_identity': 'orgmember'}
    id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    # the OrgMember will have all User fields
    org = Column(Integer, ForeignKey('organizations.id'))  # object or id?
    poc = Column(Boolean, nullable=False)

    @classmethod
    def fromdict(cls, d):
        allowed = ('name', 'email', 'passwordhash', 'phone', 'last_active', 'birthdate',
                   'bio', 'gender', 'org', 'poc')
        df = {k: v for k, v in d.items() if k in allowed}
        return cls(**df)

    def asdict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_

    def __init__(self, name, email, passwordhash, phone, poc, birthdate=None,
                 bio=None, gender=None, org=None):
        self.name = name
        self.email = email
        self.set_password(passwordhash)
        if phone > 15 :
            raise ValueError("phone number is too long")
        elif phone < 10:
            raise ValueError("phone number is too short")
        elif phone.isDigit() == False:
            raise ValueError("phone number must be a string of digits")
        else:
            self.phone = phone
        self.poc = poc
        self.last_active = datetime.now()
        self.birthdate = birthdate
        self.bio = bio
        self.gender = gender
        self.org = org

    def set_password(self, password):
        self.passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)

        # create a volunteer from a json blob

    def getOrgMember(self, id):
        s = Session()
        content = s.query(OrgMember).filter_by(id=id).first()
        s.close()
        if content:
            return content
        else:
            raise ValueError("user does not exist")

    def confirmAttendee(self, event, user):
        s = Session()
        attendee = s.query(Attendee).filter_by(event).filter_by(user).first()
        if attendee:
            attendee.confirmed = True
            s.commit()
            s.close()
            return True
        else:
            return False

    def validateHour(self, event, user):
        s = Session()
        attendee = s.query(Attendee).filter_by(event).filter_by(user).first()
        if attendee:
            attendee.hoursValidated = True
            s.commit()
            s.close()
            return True
        else:
            return False


def link_org(orgmember):
    s = Session()
    o2_org = orgmember.org
    org_m = s.query(OrgMember).filter_by(email=orgmember.email).first()
    s.close()
    if org_m:
        org_id = org_m.id
    else :
        raise exc.InvalidRequestError("query failed")
    json2 = json.dumps({'poc': org_id})
    print(json2)
    organization.updateOrg(o2_org, json2)
    return

def createMember(json):
    o = OrgMember.fromdict(json)
    s = Session()
    try:
        s.add(o)
        s.commit()
    except:
        return False
    finally:
        s.close()
        o2 = OrgMember.fromdict(json)
        link_org(o2)
        return True
