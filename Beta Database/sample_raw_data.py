import random
import datetime
import custom_dictionaries as c_dict
import custom_classes as c_class
import query_functions as query
from tqdm import tqdm
from faker import Faker
fake = Faker('pt_BR')

#---------------------[ SPONSOR SAMPLE DATA ]--------------------#
    #---[ sponsor_id = range(10001,20000) // ex.: 12345 ]---#
            #---[ #name, type_of, network=[''] ]---#

# [Function Start: Set/Update 'Sponsor' with generated data] 
def sample_sponsor_data(sample_data_ammount):
    print("Creating sample 'Sponsor' data...")
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        id = '{}'.format(int(query.get_collection_docs('Sponsors')[-1])+1).translate({ord(char): None for char in "'[]'"})
        if query.check_data_existance('Sponsors',id) == True:
            continue
        else:
            name = fake.company()
            type_of = fake.job()
            network = []
            for i in range(2):
                network.append(fake.ascii_company_email())
            sponsor_ref = query.db.collection('Sponsors').document(id)
            sponsor_ref.set(c_class.Sponsor(name, type_of, network).to_dict())
            pbar.update(+1)
            data_created = data_created + 1
    print("\nSuccesfully sent all {} 'Sponsor' data samples to the Database!".format(sample_data_ammount))
#---------------------------------------------------------------------#

#---------------------[ TRACK SAMPLE DATA ]----------------------#
    #---[ track_id = 2 + ddd + num_trilha // ex.: 28101 ]---#
            #---[ name, length=0, hashtags=[''] ]---#

# [Function Start: Set/Update 'Track' with generated data] 
def sample_track_data(sample_data_ammount):
    print("Creating sample 'Track' data...")
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        id = '2{}{}'.format(random.choice(c_dict.ddd_list), random.randint(1,99)).translate({ord(char): None for char in "'[]'"})
        if query.check_data_existance('Tracks',id) == True:
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
            track_ref = query.db.collection('Tracks').document(id)
            track_ref.set(c_class.Track(name, length, hashtags).to_dict())
            pbar.update(+1)
            data_created = data_created + 1
    print("\nSuccesfully sent all {} 'Track' data samples to the Database!".format(sample_data_ammount))
#---------------------------------------------------------------------#

#---------------------[ SENSOR SAMPLE DATA ]----------------------#
  #---[ sensor_id = track_id + sensor_num // ex.: 28101+001 ]---#
    #---[ position=0, angle=0, humidity=0, temperature=0 ]---#

# [Function Start: Sample data FUNC for 'Sensor'] 
def random_sensor_data():
    max_position = query.get_track_length('Tracks', random.choice(query.get_collection_docs('Tracks')))
    max_position_int = int(max_position)
    position = random.randrange(2000,max_position_int)
    angle = random.vonmisesvariate(180,0)*(180/3.14)
    humidity = [random.randint(0,100)]
    temperature = [random.randint(15,40)]
    data = c_class.Sensor(position,angle,humidity,temperature).to_dict()
    return data

# [Function Start: Set/Update 'Sensor' with generated data] 
def sample_sensor_data(sample_data_ammount):
    print("Creating sample 'Sensor' data...")
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        random_track_id = random.choice(query.get_collection_docs('Tracks'))
        id = '{}{}'.format(random_track_id, random.randint(101,999)).translate({ord(char): None for char in "'[]'"})
        if query.check_data_existance('Sensors',id) == True:
            continue
        else:
            sensor_ref = query.db.collection('Sensors').document(id)
            sensor_ref.set(c_class.Timestamp(random_sensor_data()).to_dict())
            i = 1
            while i < 5:
                sensor_ref.update(c_class.Timestamp(random_sensor_data()).to_dict())
                pbar.update(+(1/4))
                i = i + 1
            data_created = data_created + 1
    print("\nSuccesfully sent all {} 'Sensor' data samples to the Database!".format(sample_data_ammount))
#---------------------------------------------------------------------#

#---------------------[ PROFILE SAMPLE DATA ]---------------------#
#---[ profile_id = 5 + deficiência {range(0,6)} + sensor_id // ex.: 50+28101001 ]---#
            #--------[ sex, birthdate, profession, transport, motivation ]--------#              

# [Function Start: Sample data FUNC for 'Profile'] 
def random_profile_data():
    sex = random.choice(['Male','Female'])
    birthdate = fake.date_time_between(start_date='-50y', end_date='-15y') #date only - not timestamp - FIX
    profession = fake.job()
    transport = random.choice(['Carro','Onibus','Van','Bicicleta','Outro'])
    motivation = random.choice(['Motivo1','Motivo2','Motivo3','Motivo4','Motivo4'])
    data = c_class.Profile(sex,birthdate,profession,transport,motivation).to_dict()
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

#sample_sponsor_data(20)
#sample_track_data(10)
#sample_sensor_data(50)
#sample_profile_data(20)
#sample_investment_data(10)
