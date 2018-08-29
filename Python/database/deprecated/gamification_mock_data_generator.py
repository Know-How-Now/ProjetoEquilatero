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


