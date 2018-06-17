import random
import datetime
import custom_dictionaries as c_dict
import custom_classes as c_class
import query_functions as query
import sample_raw_data as raw_data
from tqdm import tqdm
from faker import Faker
fake = Faker()

#---------------------[ PROFILE SAMPLE DATA ]---------------------#
#---[ profile_id = 5 + deficiência {range(0,6)} + sensor_id // ex.: 50+28101001 ]---#
            #--------[ sex, age=0, group_size=0, control_id=0 ]--------#              

# [Function Start: Sample data FUNC for 'Profile'] 
def random_profile_data():
    sex = random.choice(['Male','Female'])
    birthdate = fake.date_time_between(start_date='-50y', end_date='-15y') #date only - not timestamp - FIX
    group_size = random.randint(1,5)
    control_id = random.randint(10001,99999) #create func to see if this control id already exists
    data = c_class.Profile(sex,birthdate,group_size,control_id).to_dict()
    return data

# [Function Start: Set/Update 'Profile' with generated data] 
def sample_profile_data(sample_data_ammount):
    print("Creating sample 'Profile' data...")
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        random_sensor_id = random.choice(query.get_collection_docs('Sensors'))
        id = '5{}{}'.format(random.randint(0,7),random_sensor_id).translate({ord(char): None for char in "'[]'"})
        if query.check_data_existance('Profiles',id) == True:
            continue
        else:
            profile_ref = query.db.collection('Profiles').document(id)
            profile_ref.set(c_class.Timestamp(random_profile_data()).to_dict())
            i = 1
            while i < 5:
                profile_ref.update(c_class.Timestamp(random_profile_data()).to_dict())
                pbar.update(+(1/4))
                i = i + 1
            data_created = data_created + 1
    print("\nSuccesfully sent all {} 'Profile' data samples to the Database!".format(sample_data_ammount))
#---------------------------------------------------------------------#

#---------------------[ GAMIFICATION SAMPLE DATA ]----------------------#
  #---[ gamification_id = user_id + sensor_id // ex.: 60+28101001 ]---#
#---[ title, experience=0, milestones=[''], achievements=[''], control_id=[0] ]---#

# [Function Start: Sample data FUNC for 'Gamification'] 
def random_gamification_data():
    title = fake.job() #create dict
    experience = random.randint(2000,9000)
    milestones = fake.words(6) #create dict;
    achievements = fake.words(3)
    control_id = random.randint(10001,99999) #add existance check - match other band
    data = c_class.Gamification(title,experience,milestones,achievements,control_id).to_dict()
    return data

# [Function Start: Set/Update 'Gamification' with generated data] 
def sample_gamification_data(sample_data_ammount):
    print("Creating 'Gamification' data...")
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        random_user_id = random.choice(query.get_collection_docs('Users'))
        random_sensor_id = random.choice(query.get_collection_docs('Sensors'))
        id = '{}{}'.format(random_user_id, random_sensor_id)
        if query.check_data_existance('Gamification',id) == True:
            continue
        else:
            gamification_ref = query.db.collection('Gamification').document(id)
            gamification_ref.set(c_class.Timestamp(random_gamification_data()).to_dict())
            i = 1
            while i < 5:
                gamification_ref.update(c_class.Timestamp(random_gamification_data()).to_dict())
                pbar.update(+(1/4))
                i = i + 1
            data_created = data_created + 1
    print("\nSuccesfully sent all {} 'Gamification' data samples to the Database!".format(sample_data_ammount))
#---------------------------------------------------------------------#

#---------------------[ INVESTMENT SAMPLE DATA ]---------------------#
#---[ investment_id = sponsor_id + item_id // ex.: 1000128101 ]---#
        #---[ ammount=0, allocated_to=[''], ebtida=[0] ]---# 

# [Function Start: Sample data FUNC for 'Investment'] 
def random_investment_data():
    ammount = random.randint(2001,10000)
    allocated_to = fake.words(6) #create dict;
    k = random.random()
    ebtida = ammount + (ammount*k)
    data = c_class.Investment(ammount,allocated_to,ebtida).to_dict()
    return data

# [Function Start: Set/Update 'Investor' with generated data] 
def sample_investment_data(sample_data_ammount):
    print("Creating sample 'Investment' data...")
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        random_sponsor_id = random.choice(query.get_collection_docs('Sponsors'))
        random_item_id = random.choice([random.choice(query.get_collection_docs('Tracks')), random.choice(query.get_collection_docs('Sensors')), random.randint(10001,99999)]) # add func to get control ids
        id = '{}{}'.format(random_sponsor_id, random_item_id)
        if query.check_data_existance('Investments',id) == True:
            continue
        else:
            investment_ref = query.db.collection('Investments').document(id)
            investment_ref.set(c_class.Timestamp(random_investment_data()).to_dict())
            i = 1
            while i < 5:
                investment_ref.update(c_class.Timestamp(random_investment_data()).to_dict())
                pbar.update(+(1/4))
                i = i + 1
            data_created = data_created + 1
    print("\nSuccesfully sent all {} 'Investment' data samples to the Database!".format(sample_data_ammount))
#---------------------------------------------------------------------#

#sample_profile_data(20)
#sample_gamification_data(20)
#sample_investment_data(10)
