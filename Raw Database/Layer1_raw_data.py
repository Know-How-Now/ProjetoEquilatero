##################------------------- LAYER 1: DESCRIPTIVE DATA --------------------####################

# [START: LIBRARY IMPORTS] #
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import firestore as cloudfirestore
from google.cloud import exceptions as exception
import string
import random
# [END: LIBRARY IMPORTS] #

# [START: GLOBAL VARIABLES] #
cred = credentials.Certificate('/Users/cbmelo/Documents/Projects/CESAR/Primerio_Periodo/Equilatero/Alpha/Database/Raw Database/Equilatero_Raw_Database_serviceAccount.json')  #('/Usuarios/lucianomelo/Desktop/equilatero-parceirosk.json')   #('/home/cbmelo/Downloads/equilateroparceiroBeta.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
transaction = db.transaction()
batch = db.batch()
# [END: GLBOAL VARIABLES] #

# [START: SPONSOR DESCRIPTION] #
class Sponsor(object): #sponsor_id = range(10001,20000) // ex.: 12345
    def __init__(self, name, type_of, network=['']):
        self.name = name 
        self.type_of = type_of
        self.network = network 

    @staticmethod
    def from_dict(source):
        sponsor = (source['name'], source['type_of'], source)
        if 'network' in source: 
            sponsor.network = source['network']
        return sponsor

    def to_dict(self):
        sponsor_dest = {
            'name': self.name,
            'type_of': self.type_of
        }
        if self.network:
            sponsor_dest['network'] = self.network
        return sponsor_dest

    def __repr__(self):
        return 'Sponsor(name={}, type_of={}, network={})'.format(
            self.name, self.type_of, self.network)
    # [END: SPONSOR DESCRIPTION] #

# [START: TRACK DESCRIPTION] #
class Track(object): #track_id = 2 + ddd + num_trilha // ex.: 28101 (trilha, regiao 81, numero 01)
    def __init__(self, name, length=0, hashtags=['']):
        self.name = name
        self.length = length
        self.hashtags = hashtags

    @staticmethod
    def from_dict(source):
        track = Track(source['nome'], source['length'])
        if 'hashtags' in source:
            track.hashtags = source['hashtags']
        return track

    def to_dict(self):
        track_dest = {
            'name': self.name,
            'length': self.length
        }
        if self.hashtags:
            track_dest['hashtags'] = self.hashtags
        return track_dest

    def __repr__ (self):
        return 'Track(name={}, length={}, hashtags={})'.format(
            self.name, self.length, self.hashtags)
    # [END: TRACK DESCRIPTION] #

# [START: SENSOR DESCRIPTION] #
class Sensor(object): #sensor_id = track_id + sensor_num // ex.: 28101+001
    def __init__(self, timestamp, position=0, angle=0, humidity=[0], temperature=[0]):
        self.timestamp = timestamp
        self.position = position
        self.angle = angle
        self.humidity = humidity
        self.temperature = temperature

    @staticmethod
    def from_dict(source):
        sensor = Sensor(source['timestamp'], source['position'], source['angle'])
        if 'humidity' in source:
            sensor.humidity = source['humidity']
        if 'temperature' in source:
            sensor.temperature = source['temperature']
        return sensor

    def to_dict(self):
        sensor_dest = {
            'timestamp': self.timestamp,
            'position': self.position,
            'angle': self.angle
        }
        if self.humidity:
            sensor_dest['humidity'] = self.humidity
        if self.temperature:
            sensor_dest['temperature'] = self.temperature
        return sensor_dest

    def __repr__(self):
        return 'Sensor(timestamp={}, position={}, angle={}, humidity={}, temperature={})'.format(
            self.timestamp, self.position, self.angle, self.humidity, self.temperature)
    # [END: SENSOR DESCRIPTION] #

# [START: USER PROFILE -- LEFT WRIST] # 
class Profile(object): #profile_id = 5 + deficiência {range(0,6)} + sensor_id // ex.: 50+28101001 or 5628101001
    def __init__(self, gender, age=0, group_size=0, control_id=0):
        self.gender = gender
        self.age = age
        self.group_size = group_size
        self.control_id = control_id

    @staticmethod
    def from_dict(source):
        profile = Profile(source['gender'], source['age'], source['group_size'], source['control_id'])
        return profile

    def to_dict(self):
        profile_dest = {
            'gender': self.gender,
            'age': self.age,
            'group_size': self.group_size,
            'control_id': self.control_id
        }
        return profile_dest

    def __repr__(self):
        return 'Profile(gender={}, age={}, group_size={}, control_id={})'.format(
            self.gender, self.age, self.group_size, self.control_id)
    # [END: USER PROFILE -- LEFT WRIST] #

# [START: USER DESCRIPTION] # 
class User(object): #user_id = range(60 ++)
    def __init__(self, name, gender, age=0, contact=''):
        self.name = name
        self.gender = gender
        self.age = age
        self.contact = contact

    @staticmethod
    def from_dict(source):
        user = User(source['name'], source['gender'])
        if 'age' in source:
            user.name = source['age']
        if 'contact' in source:
            user.contact = source['contact']
        return user

    def to_dict(self):
        user_dest = {
            'name': self.name,
            'gender': self.gender
        }
        if self.age:
            user_dest['age']
        if self.contact:
            user_dest['contact']
        return user_dest

    def __repr__(self):
        return 'User(name={}, gender={}, age={}, contact={})'.format(
            self.name, self.gender, self.age, self.contact)
    # [END: USER DESCRIPTION] #

# [START: GAMIFICATION PROFILE -- RIGHT WRIST] #
class Gamification(object): #gamification_id = user_id + sensor_id // ex.: 60+28101001 or 1000+28101001, or 9999+28101001
    def __init__(self, title, experience=0, group_size=[0], milestones=[''], achievements=[''], control_id=[0]):
        self.title = title
        self.experience = experience
        self.group_size = group_size
        self.milestones = milestones
        self.achievements = achievements
        self.control_id = control_id

    @staticmethod
    def from_dict(source):
        gamification = Gamification(source['title'])
        if 'experience' in source:
            gamification.experience = source['experience']
        if 'group_size' in source:
            gamification.group_size = source['group_size']
        if 'milestones' in source:
            gamification.milestones = source['milestones']
        if 'checkpoints' in source:
            gamification.achievements = source['achievements']
        if 'control_id' in source:
            gamification.control_id = source['control_id']
        return gamification

    def to_dict(self):
        gamification_dest = {
            'title': self.title
        }
        if self.experience:
            gamification_dest['experience'] = self.experience
        if self.group_size:
            gamification_dest['group_size'] = self.group_size
        if self.milestones:
            gamification_dest['milestones'] = self.milestones
        if self.achievements:
            gamification_dest['achievements'] = self.achievements
        if self.control_id:
            gamification_dest['control_id'] = self.control_id
        return gamification_dest

    def __repr__(self):
        return 'Gamification(title={}, experience={}, group_size={} milestones={}, achievements={}, control_id={})'.format(
            self.title, self.experience, self.group_size, self.milestones, self.achievements, self.control_id)
    # [END: GAMIFICATION PROFILE -- RIGHT WRIST] #

# [START: INVESTMENT DESCRIPTION] #
class Investment(object): #investment_id = sponsor_id + item_id // ex.: 1000128101 ou 1000140001
    def __init__(self, timestamp=[''], ammount=[0], allocated_to=[''], ebtida=[0]):
        self.timestamp = timestamp
        self.ammount = ammount
        self.allocated_to = allocated_to
        self.ebtida = ebtida

    @staticmethod
    def from_dict(source):
        investment = Investment(source['timestamp'])
        if 'ammount' in source: 
            investment.ammount = source['ammount']
        if 'allocated_to' in source:
            investment.allocated_to = source['allocated_to']
        if 'ebtida' in source:
            investment.ebtida = source['ebtida']
        return investment

    def to_dict(self):
        investment_dest = {
            'timestamp': self.timestamp
        }
        if self.ammount:
            investment_dest['ammount']
        if self.allocated_to:
            investment_dest['allocated_to']
        if self.ebtida:
            investment_dest['ebtida']
        return investment_dest

    def __repr__(self):
        return 'Investment(timestamp={}, ammount={}, allocated_to={}, ebtida={})'.format(
            self.timestamp, self.ammount, self.allocated_to, self.ebtida)
    # [END: INVESTMENT DESCRIPTION] #