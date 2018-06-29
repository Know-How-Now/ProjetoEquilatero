# [START LIBRARY IMPORTS] #
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import firestore as cloudfirestore
from google.cloud import exceptions as exception
import string
import random
# [END LIBRARY IMPORTS] #

# [START GLOBAL DEF] #
cred = credentials.Certificate('/home/cbmelo/Downloads/equilateroAdminBeta.json')  #('/Users/lucianomelo/Desktop/equilatero-adminsk.json')   #('/home/cbmelo/Downloads/equilateroAdminBeta.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
transaction = db.transaction()
batch = db.batch()
# [END GLBOAL DEF] #

# [START Admin_DEF] #
class Admin(object):
    def __init__(self, name, adminid, contact, artowned = [u'']):
        self.name = name
        self.adminid = adminid
        self.contact = contact
        self.artowned = artowned

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE] #
        admin = Admin(source[u'name'], source[u'adminid'], source[u'contact'])
        if u'artowned' in source:
            admin.artowned = source[u'artowned']
        return admin
    # [END_EXCLUDE] #

    def to_dict(self):
        # [START_EXCLUDE] #
        admin_dest = {
            u'name': self.name,
            u'adminid': self.adminid,
            u'contact': self.contact
        }
        if self.artowned:
            admin_dest[u'artowned'] = self.artowned
        return admin_dest
    # [END_EXCLUDE] #

    def __repr__(self):
        return u'Admin(name={}, adminid={}, contact={}, artowned={})'.format(
            self.name, self.adminid, self.contact, self.artowned)
    # [END Region_DEF] #

# [START Artefato_DEF] #
class Artefato(object):
    def __init__(self, artid, owner, currentuser = u'', lastuser = u'', lastregion = u'', positions = [0.0]):
        self.artid = artid
        self.owner = owner
        self.currentuser = currentuser
        self.lastuser = lastuser
        self.lastregion = lastregion
        self.positions = positions

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE] #
        artefato = Artefato(source[u'artid'], source[u'owner'])
        if u'currentuser' in source:
            artefato.currentuser = source[u'currentuser']
        if u'lastuser' in source:
            artefato.lastuser = source[u'lastuser']
        if u'lastregion' in source:
            artefato.lastregion = source[u'lastregion']
        if u'positions' in source:
            artefato.positions = source[u'positions']
        return artefato
    # [END_EXCLUDE] #

    def to_dict(self):
        # [START_EXCLUDE] #
        artefato_dest = {
            u'artid': self.artid,
            u'owner': self.owner
        }
        if self.currentuser:
            artefato_dest[u'currentuser'] = self.currentuser
        if self.lastuser:
            artefato_dest[u'lastuser'] = self.lastuser
        if self.lastregion:
            artefato_dest[u'lastregion'] = self.lastregion
        if self.positions:
            artefato_dest[u'positions'] = self.positions
        return artefato_dest
    # [END_EXCLUDE] #

    def __repr__(self):
        return u'Artefato(artid={}, owner={}, currentuser={} lastuser={}, lastregion={}, positions={})'.format(
            self.artid, self.owner, self.currentuser, self.lastuser, self.lastregion, self.positions)
    # [END Artefato_DEF] #

# [START Region_DEF] #
class Region(object):
    def __init__(self, name, regionid, week = 0.0, month = 0.0, population = 0, rank = 0):
        self.name = name
        self.regionid = regionid
        self.week = week
        self.month = month
        self.population = population
        self.rank = rank

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE] #
        region = Region(source[u'name'], source[u'regionid'])
        if u'week' in source:
            region.week = source[u'week']
        if u'month' in source:
            region.month = source[u'month']
        if u'population' in source:
            region.population = source[u'population']
        if u'rank' in source:
            region.rank = source[u'rank']
        return region
    # [END_EXCLUDE] #

    def to_dict(self):
        # [START_EXCLUDE] #
        region_dest = {
            u'name': self.name,
            u'regionid': self.regionid
        }
        if self.week:
            region_dest[u'week'] = self.week
        if self.month:
            region_dest[u'month'] = self.month
        if self.population:
            region_dest[u'population'] = self.population
        if self.rank:
            region_dest[u'rank'] = self.rank
        return region_dest
    # [END_EXCLUDE] #

    def __repr__ (self):
        return u'Region(name={}, regionid={}, week={}, month={}, population={}, rank={})'.format(
            self.name, self.regionid, self.week, self.month, self.population, self.rank)
    # [END Region_DEF] #

# [START Sensor_DEF] #
class Sensor(object):
    def __init__(self, sensorid, regionid, position = 0.0, avgattempt = 0.0, state = False, connections = [0]):
        self.sensorid = sensorid
        self.regionid = regionid
        self.position = position
        self.avgattempt = avgattempt
        self.state = state
        self.connections = connections

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE] #
        sensor = Sensor(source[u'sensorid'], source[u'regionid'])
        if u'position' in source:
            sensor.position = source[u'position']
        if u'avgattempt' in source:
            sensor.avgattempt = source[u'avgattempt']
        if u'state' in source:
            sensor.state= source[u'state']
        if u'connection' in source:
            sensor.connections= source[u'connections']
        return sensor
    # [END_EXCLUDE] #

    def to_dict(self):
        # [START_EXCLUDE] #
        sensor_dest = {
            u'sensorid': self.sensorid,
            u'regionid': self.regionid
        }
        if self.position:
            sensor_dest[u'position'] = self.position
        if self.avgattempt:
            sensor_dest[u'avgattempt'] = self.avgattempt
        if self.state:
            sensor_dest[u'state'] = self.state
        if self.connections:
            sensor_dest[u'connections'] = self.connections
        return sensor_dest
    # [END_EXCLUDE] #

    def __repr__(self):
        return u'Sensor(sensorid={}, regionid={}, position={}, avgattempt={}, state={}, connections={})'.format(
            self.sensorid, self.regionid, self.position, self.avgattempt, self.state, self.connections)
    # [END Sensor_DEF] #

# [START User_DEF] #
class User(object):
    def __init__(self, name, userid, condition = False, age = 0, recent = 0.0, highest = 0.0):
        self.name = name
        self.userid = userid
        self.condition = condition
        self.age = age
        self.recent = recent
        self.highest = highest

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        user = User(source[u'name'], source[u'userid'], source[u'condition'])
        if u'age' in source:
            user.age = source[u'age']
        if u'recent' in source:
            user.recent = source[u'recent']
        if u'highest' in source:
            user.highest = source[u'highest']
        return user
    # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        user_dest = {
            u'name': self.name,
            u'userid': self.userid,
            u'condition': self.condition
        }
        if self.age:
            user_dest[u'age'] = self.age
        if self.recent:
            user_dest[u'recent'] = self.recent
        if self.highest:
            user_dest[u'highest'] = self.highest
        return user_dest
    # [END_EXCLUDE]

    def __repr__(self):
        return u'User(name={}, userid={}, condition={}, age={}, recent={}, highest={})'.format(
            self.name, self.userid, self.condition, self.age, self.recent, self.highest)
    # [END User_DEF] #

# [START GENERATE UNIQUE ID FOR id_type] #
def generate_unique_id(id_type):
    unique_id = id_type +''.join(random.choice(string.digits) for _ in range(5))
    print(unique_id)
    # ADICIONAR CHECKAGEM DE ID UNICO #
    # [END GENERATE UNIQUE ID FOR id_type] #

# [START ADD SAMPLE Admin DATA] #
def add_sample_admin_data():
    # [REFERENCE collection (AND/OR document)]
    admin_ref = db.collection(u'admins')
    # [ADD MULTIPLE EXAMPLES FOR Admin]
    admin_ref.document(u'100000001').set(
        Admin(u'Cliente', u'100000001', u'cliente@clientemail.com', [u'400000001', u'400000002']).to_dict())
    admin_ref.document(u'100000002').set(
        Admin(u'Guia', u'100000002', u'guia@guiamail.com', [u'400000003', u'400000004']).to_dict())
    admin_ref.document(u'100000003').set(
        Admin(u'CESAR', u'100000003', u'cesar@is.cool', [u'400000005']).to_dict())
    admin_ref.document(u'100000004').set(
        Admin(u'KHOW', u'100000004', u'khow@is.cooler', [u'400000006']).to_dict())
    # [END OF Admin DATA SAMPLE]

# [START ADD SAMPLE Artefato DATA] #
def add_sample_artefato_data(): #artid, owner, currentuser, lastuser, lastregion, positions=[0.0]):
    # [REFERENCE collection (AND/OR document)]
    artefato_ref = db.collection(u'artefatos')
    # [ADD MULTIPLE EXAMPLES FOR Artefato]
    artefato_ref.document(u'200000006').set(
        Artefato(u'200000006', u'100000004', u'500000001', u'500000006', u'300000003', [100, 200, 400]).to_dict())
    artefato_ref.document(u'200000005').set(
        Artefato(u'200000005', u'100000003', u'500000002', u'500000005', u'300000002', [90, 150, 300]).to_dict())
    artefato_ref.document(u'200000004').set(
        Artefato(u'200000004', u'100000002', u'500000003', u'500000004', u'300000001', [4090]).to_dict())
    artefato_ref.document(u'200000003').set(
        Artefato(u'200000003', u'100000002', u'500000004', u'500000003', u'300000001', [100, 200, 400]).to_dict())
    artefato_ref.document(u'200000002').set(
        Artefato(u'200000002', u'100000001', u'500000005', u'500000002', u'300000002', [1900, 7610]).to_dict())
    artefato_ref.document(u'200000001').set(
        Artefato(u'200000001', u'100000001', u'500000006', u'500000003', u'300000001', [100]).to_dict())
    # [END OF Artefato DATA SAMPLE]

# [START ADD SAMPLE Region DATA] #
def add_sample_region_data():
    # [REFERENCE collection (AND/OR document)]
    regions_ref = db.collection(u'regions')
    # [ADD MULTIPLE EXAMPLES FOR Region]
    regions_ref.document(u'300000001').set(
        Region(u'Cha_de_Cruz', u'300000001', 42.0, 168.0, 6, 1).to_dict())
    regions_ref.document(u'300000003').set(
        Region(u'Jardim_Botanico', u'300000003', 18.0, 88.0, 2, 3).to_dict())
    regions_ref.document(u'300000002').set(
        Region(u'Horto', u'300000002', 24.0, 132.0, 4, 2).to_dict())
    # [END OF Region DATA SAMPLE]

# [START ADD SAMPLE Sensor DATA] #
def add_sample_sensor_data():
    # [REFERENCE collection (AND/OR document)]
    sensor_ref = db.collection(u'sensores')
    # [ADD MULTIPLE EXAMPLES FOR Artefato]
    sensor_ref.document(u'400000001').set(
        Sensor(u'400000001', u'300000001', 1000, 4, True, [6]).to_dict())
    sensor_ref.document(u'400000002').set(
        Sensor(u'400000002', u'300000001', 2000, 6, True, [6]).to_dict())
    sensor_ref.document(u'400000003').set(
        Sensor(u'400000003', u'300000001', 3000, 5, True, [6]).to_dict())
    sensor_ref.document(u'400000004').set(
        Sensor(u'400000004', u'300000002', 1000, 3, True, [6]).to_dict())
    sensor_ref.document(u'400000005').set(
        Sensor(u'400000005', u'300000002', 2000, 7, True, [6]).to_dict())
    sensor_ref.document(u'400000006').set(
        Sensor(u'400000006', u'300000002', 3000, 12, True, [6]).to_dict())
    sensor_ref.document(u'400000007').set(
        Sensor(u'400000007', u'300000003', 1000, 5, True, [6]).to_dict())
    sensor_ref.document(u'400000008').set(
        Sensor(u'400000008', u'300000003', 2000, 6, True, [6]).to_dict())
    sensor_ref.document(u'400000009').set(
        Sensor(u'400000009', u'300000003', 3000, 6, True, [6]).to_dict())
    sensor_ref.document(u'400000010').set(
        Sensor(u'400000010', u'300000003', 4000, 36, False, [2]).to_dict())
    # [END OF User Sensor SAMPLE]

# [START ADD SAMPLE User DATA] #
def add_sample_user_data():
    # [REFERENCE collection (AND/OR document)]
    users_ref = db.collection(u'users')
    # [ADD MULTIPLE EXAMPLES FOR User]
    users_ref.document(u'500000001').set(
        User(u'Leonardo', u'500000001', True, 21, 1.2, 3.8).to_dict())
    users_ref.document(u'500000002').set(
        User(u'Matheus', u'500000002', False, 18, 3.6, 9.6).to_dict())
    users_ref.document(u'500000003').set(
        User(u'Bernardo', u'500000003', False, 28, 4.8, 7.2).to_dict())
    users_ref.document(u'500000004').set(
        User(u'Arthur', u'500000004', False, 18, 2.4, 8.4).to_dict())
    users_ref.document(u'500000005').set(
        User(u'Beatriz', u'500000005', True, 19, 7.2, 10.8).to_dict())
    users_ref.document(u'500000006').set(
        User(u'Jacqueline', u'500000006', False, 18, 6.0, 4.8).to_dict())
    # [END OF User DATA SAMPLE]

# [START SPLITTING INCOMING DATA] #
def split_incoming_data(source, size):
    return [source[i:i + size] for i in range(0, len(source), size)]
    # [END OF SPLITTING INCOMING DATA] #

# [START UPDATE SINGLE ITEM IN SAMPLE Sensor DATA] #
def update_single_sensor():
    # [REFERENCE collection (AND/OR document)]
    sensor_ref = db.collection(u'sensors').document(u'400000010')
    # [UPDATE SINGLE ITEM]
    sensor_ref.update({u'state': False})
    # [END OF ITEM UPDATE IN Sensor SAMPLE] #

# [START UPDATE MULTIPLE ITEMS IN SAMPLE User ARTEFATO DATA] #
def update_sensores(collection,document, item1, item2, data1, data2):
    # [REFERENCE collection (AND/OR document)]
    doc_ref = db.collection(collection).document(document)
    # [UPDATE MULTIPLE ITEMS]
    doc_ref.update({
        item1 : data1,
        item2 : data2
    }, cloudfirestore.CreateIfMissingOption(True))
    # [END OF ITEMS UPDATE IN User SAMPLE] #

# [START update_nested] #
def update_nested_create_if_missing(collection, document):
    # [REFERENCE collection (AND/OR document)]
    admins_ref = db.collection(collection).document(document)
    admins_ref.set({
        u'name': u'Cliente',
        u'artowned': {
            u'200000001',
            u'200000002'
        },
        u'contact': u'cliente@clientemail.com'
    })
    admins_ref.update({
        u'age': u'T-Access',
        u'artowned.200000002': u'200000022'
    }, cloudfirestore.CreateIfMissingOption(True))
    # [END update_nested] #

# [START check IF User EXISTS] #
def check_data_existance(collection, document):
    # [REFERENCE collection (AND/OR document)]
    doc_ref = db.collection(collection).document(document)
    # [CHECK IF REFERENCE EXISTS]
    try:
        doc = doc_ref.get()
        print(u'Document exits: {}'.format(doc.to_dict()))
        return doc.to_dict()
    except exception.NotFound:
        #print(u'No such document!')
        return False
    # [END OF check] #

# [START transaction update ] #
def update_data_transaction_result(collection, document, snap):
    # [REFERENCE collection (AND/OR document)]
    doc_ref = db.collection(collection).document(document)
    @cloudfirestore.transactional
    def update_in_transaction(transaction, doc_ref,snap):
        snapshot = doc_ref.get(transaction=transaction)
        new_data = snapshot.get(snap) + 1
        data_existance = check_data_existance(collection, document)
        if data_existance == new_data:
            print('Document is already up to date...')
            return False
        elif data_existance != new_data:
            transaction.update(doc_ref, {
                snap : new_data
            })
    result = update_in_transaction(transaction, doc_ref, snap)
    if result:
        print(result)
        print(u'Data updated.')
        return True
    else:
        print(u'Data could not be updated.')
        return False
    # [END UPDATE DATA TRANSACTION] #

# [START ADD BATCH DATA IN MULTIPLE collection (AND/OR document)] #
def add_batch_sample():
    # [REFERENCE collection (AND/OR document)]
    # [SET NEW recent DATA FOR users (collection) > Ux00001 (document)]
    users_ref = db.collection(u'users').document(u'500000001')
    batch.set(users_ref, {u'recent': 1.8})
    # [REFERENCE collection (OR document)]
    # [UPDATE Sensor document]
    sensor_ref = db.collection(u'sensors').document(u'400000009')
    batch.update(sensor_ref, {u'state': False})
    # [REFERENCE collection (OR document)]
    # [DELETE Sensor document]
    sensor_ref = db.collection(u'sensors').document(u'400000011')
    batch.delete(sensor_ref)
    # [COMMIT BATCH OF CHANGES]
    batch.commit()
    # [END OF BATCH COMMIT DATA IN MULTIPLE collection (or document)] #

# [START .get SAMPLE QUERY WITH .where FILTER]
def get_deficientes_users():
    # [REFERENCE collection (AND/OR document)]
    docs = db.collection(u'users').where(u'condition', u'==', True).get()
    for doc in docs:
        user = User.from_dict(doc.to_dict())
        doc_data = [user.name, user.userid, user.condition, user.age, user.recent, user.highest]
        print(u'{}'.format(doc_data))
        print(u'{}, {}'.format(user.name, user.recent))
    # [END OF .get SIMPLE QUERY WITH FILTER]

# [START .get ALL DATA IN colletion] #
def get_deficiente_data(collection,order_by):
    # [REFERENCE collection (AND/OR document)]
    doc_ref = db.collection(collection)
    docs = doc_ref.order_by(
        order_by, direction=cloudfirestore.Query.DESCENDING).get()
    # [SEARCH FOR ALL DATA IN collection & Order_by... ]\
    if collection == u'artefatos':
        for doc in docs:
            artefato = Artefato.from_dict(doc.to_dict())
            doc_data = [artefato.artid, artefato.currentuser, artefato.lastuser,
                             artefato.lastregion, artefato.positions]
            print(u'{}'.format(doc_data))
    if collection == u'regions':
        for doc in docs:
            region = Region.from_dict(doc.to_dict())
            doc_data = [region.name, region.regionid, region.week, region.month, region.population, region.rank]
            print(u'{}'.format(doc_data))
    if collection == u'users':
        for doc in docs:
            user = User.from_dict(doc.to_dict())
            doc_data = [user.name, user.userid, user.condition, user.age, user.recent, user.highest]
            print(u'{}'.format(doc_data))
    # data_source = doc.to_dict()
    # print('Data source: {}\nSensor ID: {}'.format(data_source, sensor.sensorid))
    #[END GET ALL DATA IN collection & Order_by...]

# [START .get ALL DATA IN document] #
def get_document_data(collection,document):
    # [REFERENCE collection (AND/OR document)]
    doc_ref = db.collection(collection).document(document)
    doc = doc_ref.get()
    if collection == u'admins':
        admin = Admin.from_dict(doc.to_dict())
        doc_data = [admin.name, admin.adminid, admin.contact, admin.artowned]
        print(u'{}'.format(doc_data))
    if collection == u'artefatos':
        artefato = Artefato.from_dict(doc.to_dict())
        doc_data = [artefato.artid, artefato.currentuser, artefato.lastuser,
                         artefato.lastregion, artefato.positions]
        print(u'{}'.format(doc_data))
    if collection == u'regions':
        region = Region.from_dict(doc.to_dict())
        doc_data = [region.name, region.regionid, region.week, region.month, region.population, region.rank]
        print(u'{}'.format(doc_data))
    if collection == u'sensores':
        sensor = Sensor.from_dict(doc.to_dict())
        doc_data = [sensor.sensorid, sensor.regionid, sensor.position, sensor.avgattempt,
                       sensor.state, sensor.connections]
        print(u'{}'.format(doc_data))
    if collection == u'users':
        user = User.from_dict(doc.to_dict())
        doc_data = [user.name, user.userid, user.condition, user.age, user.recent, user.highest]
        print(u'{}'.format(doc_data))
    # data_source = doc.to_dict()
    # print('Data source: {}\nSensor ID: {}'.format(data_source, sensor.sensorid))
    # [END .get ALL DATA IN document] #

# [START .get ALL DATA IN colletion] #
def get_collection_data(collection,order_by):
    # [REFERENCE collection (AND/OR document)]
    doc_ref = db.collection(collection)
    docs = doc_ref.order_by(
        order_by, direction=cloudfirestore.Query.DESCENDING).get()
    # [SEARCH FOR ALL DATA IN collection & Order_by... ]
    if collection == u'admins':
        for doc in docs:
            admin = Admin.from_dict(doc.to_dict())
            doc_data = [admin.name, admin.adminid, admin.contact, admin.artowned]
            print(u'{}'.format(doc_data))
    if collection == u'artefatos':
        for doc in docs:
            artefato = Artefato.from_dict(doc.to_dict())
            doc_data = [artefato.artid, artefato.currentuser, artefato.lastuser,
                             artefato.lastregion, artefato.positions]
            print(u'{}'.format(doc_data))
    if collection == u'regions':
        for doc in docs:
            region = Region.from_dict(doc.to_dict())
            doc_data = [region.name, region.regionid, region.week, region.month, region.population, region.rank]
            print(u'{}'.format(doc_data))
    if collection == u'sensores':
        for doc in docs:
            sensor = Sensor.from_dict(doc.to_dict())
            doc_data = [sensor.sensorid, sensor.regionid, sensor.position, sensor.avgattempt,
                           sensor.state, sensor.connections]
            print(u'{}'.format(doc_data))
    if collection == u'users':
        for doc in docs:
            user = User.from_dict(doc.to_dict())
            doc_data = [user.name, user.userid, user.condition, user.age, user.recent, user.highest]
            print(u'{}'.format(doc_data))
            print([doc_data[0],doc_data[-1]])
            #return name_metro
    # data_source = doc.to_dict()
    # print('Data source: {}\nSensor ID: {}'.format(data_source, sensor.sensorid))
    #[END GET ALL DATA IN collection & Order_by...]

# [START .get collection WITH CONDITIONAL] #
def get_simple_query_collection_data(collection, data, comparative, value):
    doc_ref = db.collection(collection)
    docs = doc_ref.where(data,comparative,value).get()
    if collection == u'admins':
        for doc in docs:
            admin = Admin.from_dict(doc.to_dict())
            doc_data = [admin.name, admin.adminid, admin.contact, admin.artowned]
            print(u'{}'.format(doc_data))
    if collection == u'artefatos':
        for doc in docs:
            artefato = Artefato.from_dict(doc.to_dict())
            doc_data = [artefato.artid, artefato.currentuser, artefato.lastuser,
                             artefato.lastregion, artefato.positions]
            print(u'{}'.format(doc_data))
    if collection == u'regions':
        for doc in docs:
            region = Region.from_dict(doc.to_dict())
            doc_data = [region.name, region.regionid, region.week, region.month, region.population, region.rank]
            print(u'{}'.format(doc_data))
    if collection == u'sensores':
        for doc in docs:
            sensor = Sensor.from_dict(doc.to_dict())
            doc_data = [sensor.sensorid, sensor.regionid, sensor.position, sensor.avgattempt,
                           sensor.state, sensor.connections]
            print(u'{}'.format(doc_data))
    if collection == u'users':
        for doc in docs:
            user = User.from_dict(doc.to_dict())
            doc_data = [user.name, user.userid, user.condition, user.age, user.recent, user.highest]
            print(u'{}'.format(doc_data))
    # [END .get collection WITH CONDITIONAL] #

# [START .get collection WITH TWO CONDITIONALS] #
def get_compound_query_collection_data(collection, data, comparative, value, data2, comp2, value2):
    doc_ref = db.collection(collection)
    docs = doc_ref.where(data, comparative, value).get()
    docs2 = doc_ref.where(data2, comp2, value2).get()
    data_set1 = []
    data_set2 = []
    if collection == u'admins':
        for doc in docs:
            admin = Admin.from_dict(doc.to_dict())
            doc_data = [admin.name, admin.adminid, admin.contact, admin.artowned]
            data_set1.append(tuple(doc_data))
        for doc in docs2:
            admin = Admin.from_dict(doc.to_dict())
            doc_data = [admin.name, admin.adminid, admin.contact, admin.artowned]
            data_set2.append(tuple(doc_data))
    if collection == u'artefatos':
        for doc in docs:
            artefato = Artefato.from_dict(doc.to_dict())
            doc_data = [artefato.artid, artefato.currentuser, artefato.lastuser,
                             artefato.lastregion, artefato.positions]
            data_set1.append(tuple(doc_data))
        for doc in docs2:
            artefato = Artefato.from_dict(doc.to_dict())
            doc_data = [artefato.artid, artefato.currentuser, artefato.lastuser,
                             artefato.lastregion, artefato.positions]
            data_set2.append(tuple(doc_data))
    if collection == u'regions':
        for doc in docs:
            region = Region.from_dict(doc.to_dict())
            doc_data = [region.name, region.regionid, region.week, region.month, region.population, region.rank]
            data_set1.append(tuple(doc_data))
        for doc in docs2:
            region = Region.from_dict(doc.to_dict())
            doc_data = [region.name, region.regionid, region.week, region.month, region.population, region.rank]
            data_set2.append(tuple(doc_data))
    if collection == u'sensores':
        for doc in docs:
            sensor = Sensor.from_dict(doc.to_dict())
            doc_data = [sensor.sensorid, sensor.regionid, sensor.position, sensor.avgattempt,
                           sensor.state, sensor.connections]
            data_set1.append(tuple(doc_data))
        for doc in docs2:
            sensor = Sensor.from_dict(doc.to_dict())
            doc_data = [sensor.sensorid, sensor.regionid, sensor.position, sensor.avgattempt,
                           sensor.state, sensor.connections]
            data_set2.append(tuple(doc_data))
    if collection == u'users':
        for doc in docs:
            user = User.from_dict(doc.to_dict())
            doc_data = [user.name, user.userid, user.condition, user.age, user.recent, user.highest]
            data_set1.append(tuple(doc_data))
        for doc in docs2:
            user = User.from_dict(doc.to_dict())
            doc_data = [user.name, user.userid, user.condition, user.age, user.recent, user.highest]
            data_set2.append(tuple(doc_data))
            print(docs2)
    intersection = list(set(data_set1).intersection(data_set2))
    print(intersection)
    #print(type(intersection))
    print(intersection[0][0])
    # [END .get collection WITH TWO CONDITIONALS] #

# [START .get collection WITH CONDITIONAL INTERVAL] #
def get_interval_query_collection_data(collection, data, comparative, value, data2, comp2, value2):
    doc_ref = db.collection(collection)
    docs = doc_ref.where(
        data,comparative,value).where(data2, comp2, value2).get()
    if collection == u'admins':
        for doc in docs:
            admin = Admin.from_dict(doc.to_dict())
            doc_data = [admin.name, admin.adminid, admin.contact, admin.artowned]
            print(u'{}'.format(doc_data))
    if collection == u'artefatos':
        for doc in docs:
            artefato = Artefato.from_dict(doc.to_dict())
            doc_data = [artefato.artid, artefato.currentuser, artefato.lastuser,
                             artefato.lastregion, artefato.positions]
            print(u'{}'.format(doc_data))
    if collection == u'regions':
        for doc in docs:
            region = Region.from_dict(doc.to_dict())
            doc_data = [region.name, region.regionid, region.week, region.month, region.population, region.rank]
            print(u'{}'.format(doc_data))
    if collection == u'sensores':
        for doc in docs:
            sensor = Sensor.from_dict(doc.to_dict())
            doc_data = [sensor.sensorid, sensor.regionid, sensor.position, sensor.avgattempt,
                           sensor.state, sensor.connections]
            print(u'{}'.format(doc_data))
    if collection == u'users':
        for doc in docs:
            user = User.from_dict(doc.to_dict())
            doc_data = [user.name, user.userid, user.condition, user.age, user.recent, user.highest]
            print(u'{}'.format(doc_data))
    # [END .get collection WITH CONDITIONAL INTERVAL] #

#1get_simple_query_collection_data(u'users', u'highest', u'>', 7)
get_compound_query_collection_data(u'users', u'age', u'>', 20, u'highest', u'>', 7)
#get_interval_query_collection_data(u'users', u'age', u'>', 20, u'age', u'<', 30)
#get_collection_data(u'users',u'name')
#update_data_transaction_result(u'users',u'500000111',u'highest')
#check_data_existance(u'users',u'500000111')