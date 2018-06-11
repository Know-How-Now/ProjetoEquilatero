import random
import datetime
import pandas as pd
from faker import Faker
from tqdm import tqdm
import custom_dictionaries as c_dict
import Layer1_raw_data as raw_db

fake = Faker()
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
            max_position = raw_db.get_track_length('Tracks',random_track_id)
            max_position_int = int(max_position)
            position = random.randrange(2000,max_position_int)
            angle = random.vonmisesvariate(180,0)*(180/3.14)
            humidity = [random.randint(0,100)]
            temperature = [random.randint(15,40)]
            sensor_ref = raw_db.db.collection('Sensors').document(id)
            sensor_ref.set(raw_db.Sensor(position,angle,humidity,temperature,).to_dict())
            pbar.update(+1)
            data_created = data_created + 1
    print('\nSuccesfully sent all {} Sensor data samples to the Database!'.format(sample_data_ammount))

#----------------------------

# [Behavioral DATA] #
#profile_id = 5 + deficiência {range(0,6)} + sensor_id // ex.: 50+28101001 or 5628101001
    #gender, age=0, group_size=0, control_id=0):
def sample_profile_data(sample_data_ammount):
    print('Creating sample Profile data...')
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        random_sensor_id = random.choice(raw_db.get_collection_docs('Sensors'))
        id = '5{}{}'.format(random.randint(0,7),random_sensor_id).translate({ord(char): None for char in "'[]'"})
        if raw_db.check_data_existance('Profiles',id) == True:
            continue
        else:
            sex = random.choice(['Male','Female'])
            birthdate = fake.date_time_between(start_date='-50y', end_date='-15y') #date only - not timestamp - FIX
            group_size = random.randint(1,5)
            control_id = random.randint(10001,99999) #create func to see if this control id already exists
            profile_ref = raw_db.db.collection('Profiles').document(id)
            profile_ref.set(raw_db.Profile(sex,birthdate,group_size,control_id).to_dict())
            pbar.update(+1)
            data_created = data_created + 1
    print('\nSuccesfully sent all {} Profile data samples to the Database!'.format(sample_data_ammount))

#----------------------------

# [USER DATA] #
#user_id = range(60 ++)
    #name, gender, age=0, contact=''):
def sample_user_data(sample_data_ammount):
    print('Creating sample User data...')
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        id = '{}'.format(random.randint(60,9999))
        if raw_db.check_data_existance('Users',id) == True:
            continue
        else:
            name = fake.name()
            sex = random.choice(['Male','Female'])
            birthdate = fake.date_time_between(start_date='-50y', end_date='-15y') #date only - not timestamp - FIX
            contact = fake.safe_email()
            user_ref = raw_db.db.collection('Users').document(id)
            user_ref.set(raw_db.User(name,sex,birthdate,contact).to_dict())
            pbar.update(+1)
            data_created = data_created + 1
    print('\nSuccesfully sent all {} User data samples to the Database!'.format(sample_data_ammount))

#----------------------------

# [GAMIFICATION DATA] #
#gamification_id = user_id + sensor_id // ex.: 60+28101001 or 1000+28101001, or 9999+28101001
    #title, experience=0, milestones=[''], achievements=[''], control_id=[0])
def sample_gamification_data(sample_data_ammount):
    print('Creating Gamification data...')
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        random_user_id = random.choice(raw_db.get_collection_docs('Users'))
        random_sensor_id = random.choice(raw_db.get_collection_docs('Sensors'))
        id = '{}{}'.format(random_user_id, random_sensor_id)
        if raw_db.check_data_existance('Gamification',id) == True:
            continue
        else:
            title = fake.job() #create dict
            experience = random.randint(2000,9000)
            milestones = fake.words(6, ext_word_list=None) #create dict;
            achievements = fake.words(3, ext_word_list=None)
            control_id = random.randint(10001,99999) #add existance check - match other band
            gamification_ref = raw_db.db.collection('Gamification').document(id)
            gamification_ref.set(raw_db.Gamification(title,experience,milestones,achievements,control_id).to_dict())
            pbar.update(+1)
            data_created = data_created + 1
    print('\nSuccesfully sent all {} Gamification data samples to the Database!'.format(sample_data_ammount))

#----------------------------

# [INVESTMENT DATA] #
#investment_id = sponsor_id + item_id // ex.: 1000128101 ou 1000140001
    #timestamp=[''], ammount=[0], allocated_to=[''], ebtida=[0]):   
def sample_investment_data(sample_data_ammount):
    print('Creating Investment data...')
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        # IN PROGRESSSS
        random_sponsor_id = 1 #random.choice(raw_db.get_collection_docs('Users'))
        random_item_id = 1 #random.choice(raw_db.get_collection_docs('Sensors'))
        id = '{}{}'.format(random_user_id, random_sensor_id)
        if raw_db.check_data_existance('Investments',id) == True:
            continue
        else:
            ammount = 1 ###############
            allocated_to = 1 #############
            ebtida = 1 ####################
            investment_ref = raw_db.db.collection('Investments').document(id)
            investment_ref.set(raw_db.Gamification(ammount,allocated_to,ebtida).to_dict())
            pbar.update(+1)
            data_created = data_created + 1
    print('\nSuccesfully sent all {} Investment data samples to the Database!'.format(sample_data_ammount))


#-----------------------------

#sample_sponsor_data(100)
#sample_track_data(50)
#sample_sensor_data(10)
#sample_profile_data(10)
#sample_user_data(20)
#sample_gamification_data(10)
#sample_investment_data(10)
