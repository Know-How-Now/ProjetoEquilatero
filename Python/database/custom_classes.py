from faker import Faker
import datetime
fake = Faker()

# [START: SPONSOR DESCRIPTION] #
class Sponsor(object): #sponsor_id = range(10001,20000) // ex.: 12345
    def __init__(self, name, type_of, network=[''], **kwargs):
        self.name = name 
        self.type_of = type_of
        self.network = network 
        self.__dict__.update(kwargs)

    @staticmethod
    def from_dict(source):
        sponsor = Sponsor(source['name'], source['type_of'])
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
    def __init__(self, name, length=0, hashtags=[''], **kwargs):
        self.name = name
        self.length = length
        self.hashtags = hashtags
        self.__dict__.update(kwargs)

    @staticmethod
    def from_dict(source):
        track = Track(source['name'], source['length'])
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

class Sensor(object): #sensor_id = track_id + sensor_num // ex.: 28101+001
    def __init__(self, position=0, angle=0, humidity=0, temperature=0, **kwargs):
        self.position = position
        self.angle = angle
        self.humidity = humidity
        self.temperature = temperature
        self.__dict__.update(kwargs)

    @staticmethod
    def from_dict(source):
        sensor = Sensor(source['position'], source['angle'])
        if 'humidity' in source:
            sensor.humidity = source['humidity']
        if 'temperature' in source:
            sensor.temperature = source['temperature']
        return sensor

    def to_dict(self):
        sensor_dest = {
            'position': self.position,
            'angle': self.angle
        }
        if self.humidity:
            sensor_dest['humidity'] = self.humidity
        if self.temperature:
            sensor_dest['temperature'] = self.temperature
        return sensor_dest

    def __repr__(self):
        return 'Sensor(position={}, angle={}, humidity={}, temperature={})'.format(
            self.position, self.angle, self.humidity, self.temperature)
    # [END: SENSOR DESCRIPTION] #

# [START: PROFILE DESCRIPTION] # 
class Profile(object):  #profile_id = 5 + deficiência {range(0,6)} + sensor_id
    def __init__(self, sex, birthdate, hometown, current_location, profession, transport, motivation=[''], **kwargs):
        self.sex = sex
        self.birthdate = birthdate
        self.hometown = hometown
        self.current_location = current_location
        self.profession = profession
        self.transport = transport
        self.motivation = motivation
        self.__dict__.update(kwargs)

    @staticmethod
    def from_dict(source):
        profile = Profile(source['sex'], source['birthdate'], source['hometown'], source['current_location'], source['profession'], source['transport'])
        if 'motivation' in source:
            profile.motivation = source['motivation']
        return profile

    def to_dict(self):
        profile_dest = {
            'sex': self.sex,
            'birthdate': self.birthdate,
            'hometown': self.hometown,
            'current_location': self.current_location,
            'profession': self.profession,
            'transport': self.transport
        }
        if self.motivation:
            profile_dest['motivation'] = self.motivation
        return profile_dest

    def __repr__(self):
        return 'Profile(sex={}, birthdate={}, hometown={}, current_location={}, profession={}, transport={}, motivation={})'.format(
            self.sex, self.birthdate, self.hometown, self.current_location, self.profession, self.transport, self.motivation)
    # [END: PROFILE DESCRIPTION] #

# [START: INVESTMENT DESCRIPTION] #
class Investment(object): #investment_id = sponsor_id + item_id // ex.: 1000128101 ou 1000140001
    def __init__(self, ammount=0, allocated_to=[''], ebtida=[0], **kwargs):
        self.ammount = ammount
        self.allocated_to = allocated_to
        self.ebtida = ebtida
        self.__dict__.update(kwargs)

    @staticmethod
    def from_dict(source):
        investment = Investment(source['ammount'])
        if 'allocated_to' in source:
            investment.allocated_to = source['allocated_to']
        if 'ebtida' in source:
            investment.ebtida = source['ebtida']
        return investment

    def to_dict(self):
        investment_dest = {
            'ammount': self.ammount
        }
        if self.allocated_to:
            investment_dest['allocated_to'] = self.allocated_to
        if self.ebtida:
            investment_dest['ebtida'] = self.ebtida
        return investment_dest

    def __repr__(self):
        return 'Investment(ammount={}, allocated_to={}, ebtida={})'.format(
            self.ammount, self.allocated_to, self.ebtida)
    # [END: INVESTMENT DESCRIPTION] #

class Timestamp:
    def __init__(self, my_class):
        self.timestamp = str(fake.date_time_between(start_date='-1y', end_date='-1m'))
        self.my_class = my_class

    @staticmethod
    def from_dict(source):
        timestamp = Timestamp(source[''])
        if 'my_class' in source:
            timestamp.my_class = source['my_class']
        return timestamp
    
    def to_dict(self):
        timestamp_dest = {
            self.timestamp : self.my_class,
        }
        return timestamp_dest

    def __iter__(self):
        for key, value in self.my_class.items():
            yield key, value
        
    def __repr__(self):
        return '{}'.format(self.my_class)
    # [END: SENSOR DESCRIPTION] #
