from event import Event
from db import Session
import unittest
from organization import Organization
from datetime import datetime
from sqlalchemy import exc
# event contains: id, name, address, city, state, zip, about, start_at, posted_at, duration, interests, skills, org
class EventTests(unittest.TestCase):

    #checks if the events fields are initialized correctly
    def test_init(self):
        race = Event('Race for the Cure', 'Mass Ave', 'Boston', 'MA', '02115', 
            'Running a marathon to raise money for cancer research', 
            '04/02/2016 13:00', '03/27/2016 24:00:00', 2, 'cancer', 'running', 1)
        self.assertTrue(race.name == 'Race for the Cure' and
                        race.address == 'Mass Ave' and
                        race.city == 'Boston' and
                        race.state == 'MA' and
                        race.zip == '02115' and
                        race.about == 'Running a marathon to raise money for cancer research' and
                        race.start_at == '04/02/2016 13:00' and
                        race.posted_at == '03/27/2016 24:00:00' and
                        race.duration == 2 and
                        race.interests == 'cancer' and
                        race.skills == 'running' and
                        race.org == 1)

    #test object write to the database.    
    def test_db_write(self):
        race = Event('Race for the Cure', 'Mass Ave', 'Boston', 'MA', '02115',
                   'Running a marathon to raise money for cancer research', '04/02/2016 13:00', '03/27/2016 24:00:00',
                   2, 'cancer', 'running', 1)
        s = Session()
        try:
            s.add(race)
            s.commit()
            s.close()
            self.assertTrue(True)
        except exc.SQLAlchemyError:
            self.assertTrue(False)


    # checks if the event was added to the database after initialization
    def test_query(self):
        session = Session()
        race = Event('Race for the Cure', 'Mass Ave', 'Boston', 'MA', '02115',
                   'Running a marathon to raise money for cancer research', '04/02/2016 13:00', '03/27/2016 24:00:00',
                   2, 'cancer', 'running', 1)
        qrace = session.query(Event).filter_by(name='Race for the Cure').first()
        self.assertTrue(race.name == qrace.name and
                        race.address == qrace.address and
                        race.city == qrace.city and
                        race.state == qrace.state and
                        race.zip == qrace.zip and
                        race.about == qrace.about and
                        race.start_at == qrace.start_at and
                        race.posted_at == qrace.posted_at and
                        race.duration == qrace.duration and
                        race.interests == qrace.interests and
                        race.skills == qrace.skills)

    # # race.zip is a string of letters - should be 5 ints
    # def test_zip_letters(self):
    #     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', 'abcdef',
    #                'Running a marathon to raise money for cancer research', '04/02/2016 13:00', '03/27/2016 24:00:00',
    #                2, 'cancer', 'running', 'Race for the Cure')
    #     self.assertRaises(ValueError, 'zip-codes must be a string of 5 integers')

    # # race.zip is too long - should be 5 ints
    # def test_zip_length(self):
    #     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', '123456789',
    #                'Running a marathon to raise money for cancer research', '04/02/2016 13:00', '03/27/2016 24:00:00',
    #                2, 'cancer', 'running', 'Race for the Cure')
    #     self.assertRaises(ValueError, 'zip-codes must be a string of 5 integers')

    # # race.start_at is a string of letters - should be in the form mm/dd/yyyy, hh:mm
    # def test_startAt_letters(self):
    #     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', '02115',
    #                'Running a marathon to raise money for cancer research', 'oops', '03/27/2016 24:00:00',
    #                2, 'cancer', 'running', 'Race for the Cure')
    #     self.assertRaises(ValueError, 'start time must be in the form mm/dd/yyyy hh:mm')

    # # race.start_at is improperly formatted - should be in the form mm/dd/yyyy, hh:mm
    # def test_startAt_format(self):
    #     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', '02115',
    #                'Running a marathon to raise money for cancer research', 'April 12, 2016 1pm', '03/27/2016 24:00:00',
    #                2, 'cancer', 'running', 'Race for the Cure')
    #     self.assertRaises(ValueError, 'start time must be in the form mm/dd/yyyy hh:mm')

    # # race.start_at cannot be in the past
    # def test_startAt_past(self):
    #     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', '02115',
    #                'Running a marathon to raise money for cancer research', 'April 12, 2014 1pm', '03/27/2016 24:00:00',
    #                2, 'cancer', 'running', 'Race for the Cure')
    #     self.assertRaises(ValueError, 'start time must be in the form mm/dd/yyyy hh:mm')

    # # race.posted_at is a string of letters - should be in the form mm/dd/yyyy, hh:mm:ss
    # def test_postedAt_letters(self):
    #     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', '02115',
    #                'Running a marathon to raise money for cancer research', '04/02/2016 13:00', 'oops',
    #                2, 'cancer', 'running', 'Race for the Cure')
    #     self.assertRaises(ValueError, 'post time must be in the form mm/dd/yyyy hh:mm:ss')

    # # race.posted_at is improperly formatted - should be in the form mm/dd/yyyy, hh:mm:ss
    # def test_postedAt_format(self):
    #     race = Event(1, 'Race for the cure', 'Mass Ave', 'Boston', 'MA', '02115',
    #                'Running a marathon to raise money for cancer research', '04/02/2016 13:00', 'March 27, 2016 12am',
    #                2, 'cancer', 'running', 'Race for the Cure')
    #     self.assertRaises(ValueError, 'post time must be in the form mm/dd/yyyy hh:mm:ss')

    # These tests require the Interest and Skills Enumerations to be created

    # # race.interests should exist in the interests table
    # def test_interests_exists(self):
    #     session = Session()
    #     self.assertEqual(self.race.interests, session.query(Interests).filter_by(name=self.race.interests).first())
    #     session.close()
    #
    # # race.skills should exist in the skills table
    # def test_skills_exists(self):
    #     session = Session()
    #     self.assertEqual(self.race.skills, session.query(Skills).filter_by(name=self.race.skills).first())
    #     session.close()

     # something wonky seems to be going on with calling an org id.
    def test_org_exists(self):
        session = Session()
        race = Event('Race for the Cure', 'Mass Ave', 'Boston', 'MA', '02115', 
            'Running a marathon to raise money for cancer research', 
            '04/02/2016 13:00', '03/27/2016 24:00:00', 2, 'cancer', 'running', 1)
        org = Organization('Cancer Research Center', '350 Mass Ave', 'Boston', 'MA', '02115', 'Looking for a Cure!', 'admin@ccr.org', '6177793535', 'cancer')
        query = session.query(Organization).filter_by(id=race.org).first()
        self.assertTrue(org.name == query.name and
                        org.address == query.address and
                        org.city == query.city)

if __name__ == '__main__':
    unittest.main()





