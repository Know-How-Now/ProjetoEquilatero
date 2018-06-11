import random
import datetime
import pandas as pd
from tqdm import tqdm
import custom_dictionaries as c_dict
import Layer1_raw_data as raw_db

fake = faker.Faker()
#db_timestamp = firebase_admin.firestore.FieldValue.serverTimestamp()
#firestore.SERVER_TIMESTAMP

# [SPONSOR DATA] #
#sponsor_id = range(10001,20000) // ex.: 12345
    #name, type_of, network=['']):

def sample_sponsor_data(sample_data_ammount):
    print('Creating sample Sponsor data...')
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        id = str(random.randint(10001,20000))
        if raw_db.check_data_existance('Sponsors',id) == True:
            continue
        else:
            name = fake.company()
            type_of = fake.job()
            network = []
            for i in range(2):
                network.append(fake.ascii_company_email())
            sponsor_ref = raw_db.db.collection('Sponsors')
            sponsor_ref.document(id).set(
                raw_db.Sponsor(name,type_of,network).to_dict())
            data_created = data_created + 1
            pbar.update(+1)
    print('\nSuccesfully sent all {} Sponsor data samples to the Database!'.format(sample_data_ammount))

#------------------------

# [TRACK DATA] #
#track_id = 2 + ddd + num_trilha // ex.: 28101 (trilha, regiao 81, numero 01)
    #name, length=0, hashtags=['']):

def sample_track_data(sample_data_ammount):
    print('Creating sample Track data...')
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        id = '2{}{}'.format(random.choice(c_dict.ddd_list), random.randint(1,99)).translate({ord(char): None for char in "'[]'"})
        if raw_db.check_data_existance('Track',id) == True:
            continue
        else:
            name = fake.street_name()
            length = random.randint(2000,10000)
            hashtags = []
            while len(hashtags) < len(c_dict.track_trait_choices):
                random_trait = random.choice(c_dict.track_trait_choices)
                random_characteristic = random.choice(random_trait) 
                if random_characteristic in hashtags:
                    continue
                else:
                    hashtags.append(random_characteristic)
            track_ref = raw_db.db.collection('Tracks')
            track_ref.document(id).set(
                raw_db.Track(name,length,hashtags).to_dict())
            data_created = data_created + 1
            pbar.update(+1)
    print('\nSuccesfully sent all {} Track data samples to the Database!'.format(sample_data_ammount))

#----------------------------

# [SENSOR DATA] #
#sensor_id = track_id + sensor_num // ex.: 28101+001
    #timestamp, position=0, angle=0, humidity=[0], temperature=[0]):

def sample_sensor_data(sample_data_ammount):
    print('Creating sample Sensor data...')
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        random_track_id = random.choice(raw_db.get_collection_docs('Tracks'))
        id = '{}{}'.format(random_track_id, random.randint(101,999)).translate({ord(char): None for char in "'[]'"})
        if raw_db.check_data_existance('Sensor',id) == True:
            continue
        else:
            for i in range(0,1):
                timestamp = fake.date_time_between(start_date='-1y', end_date='now')
                timestamp_str = str(timestamp)
                max_position = raw_db.get_track_length('Tracks',random_track_id)
                max_position_int = int(max_position)
                position = random.randrange(2000,max_position_int) #non-interger?? erro - fix
                angle = random.vonmisesvariate(180,0)*(180/3.14)
                humidity = [random.randint(0,100)]
                temperature = [random.randint(15,40)]

                data = raw_db.Sensor(position,angle,humidity,temperature).to_dict()

                sensor_ref = raw_db.db.collection('Sensors').document(id)
                #sensor_timestamp_ref = sensor_ref.collection('Date').document(timestamp_str)
                sensor_ref.set(raw_db.Timestamp(timestamp_str).to_dict()) ##broken
                pbar.update(+.1)
                i = i + 1
            data_created = data_created + 1
    print('\nSuccesfully sent all {} Sensor data samples to the Database!'.format(sample_data_ammount))

sample_sensor_data(5)

#----------------------------

# [PROFILE DATA] #
#profile_id = 5 + deficiência {range(0,6)} + sensor_id // ex.: 50+28101001 or 5628101001
    #gender, age=0, group_size=0, control_id=0):

#def sample_sensor():

#----------------------------

# [USER DATA] #
#user_id = range(60 ++)
    #name, gender, age=0, contact=''):

#def sample_data():

#----------------------------


# [GAMIFICATION DATA] #
#gamification_id = user_id + sensor_id // ex.: 60+28101001 or 1000+28101001, or 9999+28101001
    #title, experience=0, group_size=[0], milestones=[''], achievements=[''], control_id=[0])

#def sample_gamification():

#----------------------------

# [INVESTMENT DATA] #
#investment_id = sponsor_id + item_id // ex.: 1000128101 ou 1000140001
    #timestamp=[''], ammount=[0], allocated_to=[''], ebtida=[0]):   

#def sample_investment():

#-----------------------------

#sample_sponsor_data(100)
#sample_track_data(50)
