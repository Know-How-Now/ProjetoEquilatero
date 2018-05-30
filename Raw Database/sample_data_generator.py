import faker
import random
import string

fake = faker.Faker()


# [SPONSOR DATA] #
#sponsor_id = range(10001,20000) // ex.: 12345
    #name, type_of, network=['']):

def sample_sponsor():
    id = random.randint(10001,20000)
    name = fake.company()
    network = []
    for i in range(2):
        network.append(fake.name())
    print(network)
sample_sponsor()

#------------------------

# [TRACK DATA] #
#track_id = 2 + ddd + num_trilha // ex.: 28101 (trilha, regiao 81, numero 01)
    #name, length=0, hashtags=['']):

#def sample_track():

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