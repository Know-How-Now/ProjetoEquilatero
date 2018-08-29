#---------------------[ USER SAMPLE DATA ]---------------------#
        #---[ user_id = range(60 ++) // ex.: 9999 ]---#
          #---[ name, sex, age=0, contact='' ]---#

# [Function Start: Set/Update 'User' with generated data] 
def sample_user_data(sample_data_ammount):
    print("Creating sample 'User' data...")
    data_created = 0
    pbar = tqdm(total=sample_data_ammount)
    while data_created < sample_data_ammount:
        id = '1001'
        #id = '{}'.format(int(query.get_collection_docs('Users')[-1])+1).translate({ord(char): None for char in "'[]'"})
        if query.check_data_existance('Users',id) == True:
            continue
        else:
            sex = random.choice(['Male','Female'])
            birthdate = fake.date_time_between(start_date='-50y', end_date='-15y') #date only - not timestamp - FIX
            user_ref = query.db.collection('Users').document(id)
            user_ref.set(c_class.User(name, sex, birthdate, contact).to_dict())
            pbar.update(+1)
            data_created = data_created + 1
    print("\nSuccesfully sent all {} 'User' data samples to the Database!".format(sample_data_ammount))
#---------------------------------------------------------------------#
