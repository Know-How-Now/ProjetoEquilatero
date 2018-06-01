import Layer1_raw_data as raw_db
import faker
import random
import pandas as pd
from tqdm import tqdm
import custom_dictionaries as c_dict

fake = faker.Faker()

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
        id = '2{}{}'.format(random.sample(c_dict.ddd_list, 1), random.randint(1,99)).translate({ord(char): None for char in "'[]'"})
        if raw_db.check_data_existance('Track',id) == True:
            continue
        else:
            length = random.randint(2000,8100,100)
            hashtags = []
            for i in range(5):
                hashtags.append(random.sample()) ###edit this to add c_dict data
            track_ref = raw_db.db.collection('Tracks')
            track_ref.document(id).set(
                raw_db.Sponsor(name,length,hashtags).to_dict())
            data_created = data_created + 1
            pbar.update(+1)
    print('\nSuccesfully sent all {} Track data samples to the Database!'.format(sample_data_ammount))


#----------------------------

# [SENSOR DATA] #
#sensor_id = track_id + sensor_num // ex.: 28101+001
    #timestamp, position=0, angle=0, humidity=[0], temperature=[0]):

#def sample_sensor():

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

sample_sponsor_data(100)
