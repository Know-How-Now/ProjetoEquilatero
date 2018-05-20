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
cred = credentials.Certificate('/Users/cbmelo/Documents/Projects/CESAR/Primerio_Periodo/Equilatero/Alpha/Database/Raw Database/Equilatero_Raw_Database_serviceAccount.json')  #('/Usuarios/lucianomelo/Desktop/equilatero-parceirosk.json')   #('/home/cbmelo/Downloads/equilateroparceiroBeta.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
transaction = db.transaction()
batch = db.batch()
# [END GLBOAL DEF] #

# [START parceiro_DEF] #
class Parceiro(object):
    def __init__(self, nome, parceiro_id, contato, trilhas_adotadas=[''], pulseiras_adotadas=[''], sensores_adotados=['']):
        self.nome = nome
        self.parceiro_id = parceiro_id
        self.contato = contato
        self.trilhas_adotadas = trilhas_adotadas
        self.pulseiras_adotadas = pulseiras_adotadas
        self.sensores_adotados = sensores_adotados

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE] #
        parceiro = Parceiro(source['nome'], source['parceiro_id'], source['contato'])
        if 'trilhas_adotadas' in source:
            parceiro.trilhas_adotadas = source['trilhas_adotadas']
        if 'pulseiras_adotadas' in source:
            parceiro.pulseiras_adotadas = source['pulseiras_adotadas']
        if 'sensores_adotados' in source:
            parceiro.sensores_adotados = source['sensores_adotados']
        return parceiro
    # [END_EXCLUDE] #

    def to_dict(self):
        # [START_EXCLUDE] #
        parceiro_dest = {
            'nome': self.nome,
            'parceiro_id': self.parceiro_id,
            'contato': self.contato
        }
        if self.trilhas_adotadas:
            parceiro_dest['trilhas_adotadas']
        if self.pulseiras_adotadas:
            parceiro_dest['pulseiras_adotadas']
        if self.sensores_adotados:
            parceiro_dest['sensores_adotados']
        return parceiro_dest
    # [END_EXCLUDE] #

    def __repr__(self):
        return 'Parceiro(nome={}, parceiro_id={}, contato={}, trilhas_adotadas={}, pulseiras_adotadas={}, sensores_adotados={})'.format(
            self.nome, self.parceiro_id, self.contato, self.trilhas_adotadas, self.pulseiras_adotadas, self.sensores_adotados)
    # [END Region_DEF] #

# [START pulseira_DEF] #
class Pulseira(object):
    def __init__(self, pulseira_id, usuario_id_atual='', usuario_id_passado='', checkpoints=[0]):
        self.pulseira_id = pulseira_id
        self.usuario_id_atual = usuario_id_atual
        self.usuario_id_passado = usuario_id_passado
        self.checkpoints = checkpoints

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE] #
        pulseira = Pulseira(source['pulseira_id'])
        if 'usuario_id_atual' in source:
            pulseira.usuario_id_atual = source['usuario_id_atual']
        if 'usuario_id_passado' in source:
            pulseira.usuario_id_passado = source['usuario_id_passado']
        if 'checkpoints' in source:
            pulseira.checkpoints = source['checkpoints']
        return pulseira
    # [END_EXCLUDE] #

    def to_dict(self):
        # [START_EXCLUDE] #
        pulseira_dest = {
            'pulseira_id': self.pulseira_id
        }
        if self.usuario_id_atual:
            pulseira_dest['usuario_id_atual'] = self.usuario_id_atual
        if self.usuario_id_passado:
            pulseira_dest['usuario_id_passado'] = self.usuario_id_passado
        if self.checkpoints:
            pulseira_dest['checkpoints'] = self.checkpoints
        return pulseira_dest
    # [END_EXCLUDE] #

    def __repr__(self):
        return 'Pulseira(pulseira_id={}, usuario_id_atual={} usuario_id_passado={}, checkpoints={})'.format(
            self.pulseira_id, self.usuario_id_atual, self.usuario_id_passado, self.checkpoints)
    # [END pulseira_DEF] #

# [START Region_DEF] #
class Trilha(object):
    def __init__(self, nome, trilha_id, visitas=['']):
        self.nome = nome
        self.trilha_id = trilha_id
        self.visitas = visitas

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE] #
        trilha = Trilha(source['nome'], source['trilha_id'])
        if 'visitas' in source:
            trilha.visitas = source['visitas']
        return trilha
    # [END_EXCLUDE] #

    def to_dict(self):
        # [START_EXCLUDE] #
        trilha_dest = {
            'nome': self.nome,
            'trilha_id': self.trilha_id
        }
        if self.visitas:
            trilha_dest['visitas'] = self.visitas
        return trilha_dest
    # [END_EXCLUDE] #

    def __repr__ (self):
        return 'Trilha(nome={}, trilha_id={}, visitas={})'.format(
            self.nome, self.trilha_id, self.visitas)
    # [END Region_DEF] #

# [START Sensor_DEF] #
class Sensor(object):
    def __init__(self, sensor_id, trilha_id, posicao=0, pareamentos=0):
        self.sensor_id = sensor_id
        self.trilha_id = trilha_id
        self.posicao = posicao
        self.pareamentos = pareamentos

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE] #
        sensor = Sensor(source['sensor_id'], source['trilha_id'])
        if 'posicao' in source:
            sensor.posicao = source['posicao']
        if 'pareamentos' in source:
            sensor.pareamentos= source['pareamentos']
        return sensor
    # [END_EXCLUDE] #

    def to_dict(self):
        # [START_EXCLUDE] #
        sensor_dest = {
            'sensor_id': self.sensor_id,
            'trilha_id': self.trilha_id
        }
        if self.posicao:
            sensor_dest['posicao'] = self.posicao
        if self.pareamentos:
            sensor_dest['pareamentos'] = self.pareamentos
        return sensor_dest
    # [END_EXCLUDE] #

    def __repr__(self):
        return 'Sensor(sensor_id={}, trilha_id={}, posicao={}, pareamentos={})'.format(
            self.sensor_id, self.trilha_id, self.posicao, self.pareamentos)
    # [END Sensor_DEF] #

# [START Usuario_DEF] #
class Usuario(object):
    def __init__(self, nome, usuario_id, deficiencia=False, idade=0, checkpoints=[0]):
        self.nome = nome
        self.usuario_id = usuario_id
        self.deficiencia = deficiencia
        self.idade = idade
        self.checkpoints = checkpoints

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        usuario = Usuario(source['nome'], source['usuario_id'], source['deficiencia'])
        if 'idade' in source:
            usuario.idade = source['idade']
        if 'checkpoints' in source:
            usuario.checkpoints = source['checkpoints']
        return usuario
    # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        usuario_dest = {
            'nome': self.nome,
            'usuario_id': self.usuario_id,
            'deficiencia': self.deficiencia
        }
        if self.idade:
            usuario_dest['idade'] = self.idade
        if self.checkpoints:
            usuario_dest['checkpoints'] = self.checkpoints
        return usuario_dest
    # [END_EXCLUDE]

    def __repr__(self):
        return 'Usuario(nome={}, usuario_id={}, deficiencia={}, idade={}, checkpoints={})'.format(
            self.nome, self.usuario_id, self.deficiencia, self.idade, self.checkpoints)
    # [END Usuario_DEF] #

# [START GENERATE UNIQUE ID FOR id_type] #
def generate_unique_id(id_type):
    unique_id = id_type +''.join(random.choice(string.digits) for _ in range(5))
    print(unique_id)
    # ADICIONAR CHECKidadeM DE ID UNICO #
    # [END GENERATE UNIQUE ID FOR id_type] #

# [START ADD SAMPLE parceiro DATA] #
def add_sample_parceiro_data():
    # [REFERENCE collection (AND/OR document)]
    parceiro_ref = db.collection('parceiros')
    # [ADD MULTIPLE EXAMPLES FOR parceiro]
    parceiro_ref.document('100000001').set(
        Parceiro('Cliente', '100000001', 'cliente@clientemail.com', ['400000001', '400000002']).to_dict())
    parceiro_ref.document('100000002').set(
        Parceiro('Guia', '100000002', 'guia@guiamail.com', ['400000003', '400000004']).to_dict())
    parceiro_ref.document('100000003').set(
        Parceiro('CESAR', '100000003', 'cesar@is.cool', ['400000005']).to_dict())
    parceiro_ref.document('100000004').set(
        Parceiro('KHOW', '100000004', 'khow@is.cooler', ['400000006']).to_dict())
    # [END OF parceiro DATA SAMPLE]

# [START ADD SAMPLE Pulseira DATA] #
def add_sample_pulseira_data(): #pulseira_id, usuario_id_atual, usuario_id_passado, checkpoints=[0.0]):
    # [REFERENCE collection (AND/OR document)]
    pulseira_ref = db.collection('pulseiras')
    # [ADD MULTIPLE EXAMPLES FOR Pulseira]
    pulseira_ref.document('200000006').set(
        Pulseira('200000006', '500000001' '500000006', [100, 200, 400]).to_dict())
    pulseira_ref.document('200000005').set(
        Pulseira('200000005', '500000002', '500000005', [90, 150, 300]).to_dict())
    pulseira_ref.document('200000004').set(
        Pulseira('200000004', '500000003', '500000004', [4090]).to_dict())
    pulseira_ref.document('200000003').set(
        Pulseira('200000003', '500000004', '500000003', [100, 200, 400]).to_dict())
    pulseira_ref.document('200000002').set(
        Pulseira('200000002', '500000005', '500000002', [1900, 7610]).to_dict())
    pulseira_ref.document('200000001').set(
        Pulseira('200000001', '500000006', '500000003', [100]).to_dict())
    # [END OF Pulseira DATA SAMPLE]

# [START ADD SAMPLE trilha DATA] #
def add_sample_trilha_data():
    # [REFERENCE collection (AND/OR document)]
    trilhas_ref = db.collection('trilhas')
    # [ADD MULTIPLE EXAMPLES FOR trilha]
    trilhas_ref.document('300000001').set(
        Trilha('Cha_de_Cruz', '300000001', ['userlalala, userlololo']).to_dict())
    trilhas_ref.document('300000003').set(
        Trilha('Jardim_Botanico', '300000003', ['userlalala, userlololo']).to_dict())
    trilhas_ref.document('300000002').set(
        Trilha('Horto', '300000002', ['userlalala, userlololo']).to_dict())
    # [END OF trilha DATA SAMPLE]

# [START ADD SAMPLE Sensor DATA] #
def add_sample_sensor_data():
    # [REFERENCE collection (AND/OR document)]
    sensor_ref = db.collection('sensores')
    # [ADD MULTIPLE EXAMPLES FOR Pulseira]
    sensor_ref.document('400000001').set(
        Sensor('400000001', '300000001', 1000, 6).to_dict())
    sensor_ref.document('400000002').set(
        Sensor('400000002', '300000001', 2000, 100).to_dict())
    sensor_ref.document('400000003').set(
        Sensor('400000003', '300000001', 3000, 5).to_dict())
    sensor_ref.document('400000004').set(
        Sensor('400000004', '300000002', 1000, 12).to_dict())
    sensor_ref.document('400000005').set(
        Sensor('400000005', '300000002', 2000, 72).to_dict())
    sensor_ref.document('400000006').set(
        Sensor('400000006', '300000002', 3000, 12).to_dict())
    sensor_ref.document('400000007').set(
        Sensor('400000007', '300000003', 1000, 5).to_dict())
    sensor_ref.document('400000008').set(
        Sensor('400000008', '300000003', 2000, 45).to_dict())
    sensor_ref.document('400000009').set(
        Sensor('400000009', '300000003', 3000, 22).to_dict())
    sensor_ref.document('400000010').set(
        Sensor('400000010', '300000003', 4000, 36).to_dict())
    # [END OF Usuario Sensor SAMPLE]

# [START ADD SAMPLE Usuario DATA] #
def add_sample_usuario_data():
    # [REFERENCE collection (AND/OR document)]
    usuarios_ref = db.collection('usuarios')
    # [ADD MULTIPLE EXAMPLES FOR Usuario]
    usuarios_ref.document('500000001').set(
        Usuario('Leonardo', '500000001', True, 21, [100, 200, 400]).to_dict())
    usuarios_ref.document('500000002').set(
        Usuario('Matheus', '500000002', False, 18, [1100, 2200, 9100]).to_dict())
    usuarios_ref.document('500000003').set(
        Usuario('Bernardo', '500000003', False, 28, [5100, 1200, 3400]).to_dict())
    usuarios_ref.document('500000004').set(
        Usuario('Arthur', '500000004', False, 18, [7500, 2320, 4021]).to_dict())
    usuarios_ref.document('500000005').set(
        Usuario('Beatriz', '500000005', True, 19, [8310, 9091, 4242]).to_dict())
    usuarios_ref.document('500000006').set(
        Usuario('Jacqueline', '500000006', False, 18, [1231, 9732, 4310]).to_dict())
    # [END OF Usuario DATA SAMPLE]

# [START SPLITTING INCOMING DATA] #
def split_incoming_data(source, size):
    return [source[i:i + size] for i in range(0, len(source), size)]
    # [END OF SPLITTING INCOMING DATA] #

# [START UPDATE SINGLE ITEM IN SAMPLE Sensor DATA] #
def update_single_sensor():
    # [REFERENCE collection (AND/OR document)]
    sensor_ref = db.collection('sensors').document('400000010')
    # [UPDATE SINGLE ITEM]
    sensor_ref.update({'state': False})
    # [END OF ITEM UPDATE IN Sensor SAMPLE] #

# [START UPDATE MULTIPLE ITEMS IN SAMPLE Usuario PULSEIRA DATA] #
def update_sensores(collection,document, item1, item2, data1, data2):
    # [REFERENCE collection (AND/OR document)]
    doc_ref = db.collection(collection).document(document)
    # [UPDATE MULTIPLE ITEMS]
    doc_ref.update({
        item1 : data1,
        item2 : data2
    }, cloudfirestore.CreateIfMissingOption(True))
    # [END OF ITEMS UPDATE IN Usuario SAMPLE] #

# [START update_nested] #
def update_nested_create_if_missing(collection, document):
    # [REFERENCE collection (AND/OR document)]
    parceiros_ref = db.collection(collection).document(document)
    parceiros_ref.set({
        'nome': 'Cliente',
        'pulseiras_adotadas': {
            '200000001',
            '200000002'
        },
        'contato': 'cliente@clientemail.com'
    })
    parceiros_ref.update({
        'idade': 'T-Access',
        'pulseiras_adotadas.200000002': '200000022'
    }, cloudfirestore.CreateIfMissingOption(True))
    # [END update_nested] #

# [START check IF Usuario EXISTS] #
def check_data_existance(collection, document):
    # [REFERENCE collection (AND/OR document)]
    doc_ref = db.collection(collection).document(document)
    # [CHECK IF REFERENCE EXISTS]
    try:
        doc = doc_ref.get()
        print('Document exits: {}'.format(doc.to_dict()))
        return doc.to_dict()
    except exception.NotFound:
        #print('No such document!')
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
        print('Data updated.')
        return True
    else:
        print('Data could not be updated.')
        return False
    # [END UPDATE DATA TRANSACTION] #

# [START ADD BATCH DATA IN MULTIPLE collection (AND/OR document)] #
def add_batch_sample():
    # [REFERENCE collection (AND/OR document)]
    # [SET NEW checkpoints DATA FOR usuarios (collection) > Ux00001 (document)]
    usuarios_ref = db.collection('usuarios').document('500000001')
    batch.set(usuarios_ref, {'checkpoints': 1.8})
    # [REFERENCE collection (OR document)]
    # [UPDATE Sensor document]
    sensor_ref = db.collection('sensors').document('400000009')
    batch.update(sensor_ref, {'state': False})
    # [REFERENCE collection (OR document)]
    # [DELETE Sensor document]
    sensor_ref = db.collection('sensors').document('400000011')
    batch.delete(sensor_ref)
    # [COMMIT BATCH OF CHANGES]
    batch.commit()
    # [END OF BATCH COMMIT DATA IN MULTIPLE collection (or document)] #

# [START .get SAMPLE QUERY WITH .where FILTER]
def get_deficientes_usuarios():
    # [REFERENCE collection (AND/OR document)]
    docs = db.collection('usuarios').where('deficiencia', '==', True).get()
    for doc in docs:
        usuario = Usuario.from_dict(doc.to_dict())
        doc_data = [usuario.nome, usuario.usuario_id, usuario.deficiencia, usuario.idade, usuario.checkpoints]
        print('{}'.format(doc_data))
        print('{}, {}'.format(usuario.nome, usuario.checkpoints))
    # [END OF .get SIMPLE QUERY WITH FILTER]

# [START .get ALL DATA IN colletion] #
def get_deficiente_data(collection,order_by):
    # [REFERENCE collection (AND/OR document)]
    doc_ref = db.collection(collection)
    docs = doc_ref.order_by(
        order_by, direction=cloudfirestore.Query.DESCENDING).get()
    # [SEARCH FOR ALL DATA IN collection & Order_by... ]\
    if collection == 'pulseiras':
        for doc in docs:
            pulseira = Pulseira.from_dict(doc.to_dict())
            doc_data = [pulseira.pulseira_id, pulseira.usuario_id_atual, pulseira.usuario_id_passado, pulseira.checkpoints]
            print('{}'.format(doc_data))
    if collection == 'trilhas':
        for doc in docs:
            trilha = Trilha.from_dict(doc.to_dict())
            doc_data = [trilha.nome, trilha.trilha_id, trilha.visitas]
            print('{}'.format(doc_data))
    if collection == 'usuarios':
        for doc in docs:
            usuario = Usuario.from_dict(doc.to_dict())
            doc_data = [usuario.nome, usuario.usuario_id, usuario.deficiencia, usuario.idade, usuario.checkpoints]
            print('{}'.format(doc_data))
    # data_source = doc.to_dict()
    # print('Data source: {}\nSensor ID: {}'.format(data_source, sensor.sensor_id))
    #[END GET ALL DATA IN collection & Order_by...]

# [START .get ALL DATA IN document] #
def get_document_data(collection,document):
    # [REFERENCE collection (AND/OR document)]
    doc_ref = db.collection(collection).document(document)
    doc = doc_ref.get()
    if collection == 'parceiros':
        parceiro = Parceiro.from_dict(doc.to_dict())
        doc_data = [parceiro.nome, parceiro.parceiro_id, parceiro.contato, parceiro.pulseiras_adotadas]
        print('{}'.format(doc_data))
    if collection == 'pulseiras':
        pulseira = Pulseira.from_dict(doc.to_dict())
        doc_data = [pulseira.pulseira_id, pulseira.usuario_id_atual, pulseira.usuario_id_passado, pulseira.checkpoints]
        print('{}'.format(doc_data))
    if collection == 'trilhas':
        trilha = Trilha.from_dict(doc.to_dict())
        doc_data = [trilha.nome, trilha.trilha_id, trilha.visitas]
        print('{}'.format(doc_data))
    if collection == 'sensores':
        sensor = Sensor.from_dict(doc.to_dict())
        doc_data = [sensor.sensor_id, sensor.trilha_id, sensor.posicao, sensor.pareamentos]
        print('{}'.format(doc_data))
    if collection == 'usuarios':
        usuario = Usuario.from_dict(doc.to_dict())
        doc_data = [usuario.nome, usuario.usuario_id, usuario.deficiencia, usuario.idade, usuario.checkpoints]
        print('{}'.format(doc_data))
    # data_source = doc.to_dict()
    # print('Data source: {}\nSensor ID: {}'.format(data_source, sensor.sensor_id))
    # [END .get ALL DATA IN document] #

# [START .get ALL DATA IN colletion] #
def get_collection_data(collection,order_by):
    # [REFERENCE collection (AND/OR document)]
    doc_ref = db.collection(collection)
    docs = doc_ref.order_by(
        order_by, direction=cloudfirestore.Query.DESCENDING).get()
    # [SEARCH FOR ALL DATA IN collection & Order_by... ]
    if collection == 'parceiros':
        for doc in docs:
            parceiro = Parceiro.from_dict(doc.to_dict())
            doc_data = [parceiro.nome, parceiro.parceiro_id, parceiro.contato, parceiro.pulseiras_adotadas]
            print('{}'.format(doc_data))
    if collection == 'pulseiras':
        for doc in docs:
            pulseira = Pulseira.from_dict(doc.to_dict())
            doc_data = [pulseira.pulseira_id, pulseira.usuario_id_atual, pulseira.usuario_id_passado, pulseira.checkpoints]
            print('{}'.format(doc_data))
    if collection == 'trilhas':
        for doc in docs:
            trilha = Trilha.from_dict(doc.to_dict())
            doc_data = [trilha.nome, trilha.trilha_id, trilha.visitas]
            print('{}'.format(doc_data))
    if collection == 'sensores':
        for doc in docs:
            sensor = Sensor.from_dict(doc.to_dict())
            doc_data = [sensor.sensor_id, sensor.trilha_id, sensor.posicao, sensor.pareamentos]
            print('{}'.format(doc_data))
    if collection == 'usuarios':
        for doc in docs:
            usuario = Usuario.from_dict(doc.to_dict())
            doc_data = [usuario.nome, usuario.usuario_id, usuario.deficiencia, usuario.idade, usuario.checkpoints]
            print('{}'.format(doc_data))
            print([doc_data[0],doc_data[-1]])
            #return nome_metro
    # data_source = doc.to_dict()
    # print('Data source: {}\nSensor ID: {}'.format(data_source, sensor.sensor_id))
    #[END GET ALL DATA IN collection & Order_by...]

# [START .get collection WITH deficienciaAL] #
def get_simple_query_collection_data(collection, data, comparative, value):
    doc_ref = db.collection(collection)
    docs = doc_ref.where(data,comparative,value).get()
    if collection == 'parceiros':
        for doc in docs:
            parceiro = Parceiro.from_dict(doc.to_dict())
            doc_data = [parceiro.nome, parceiro.parceiro_id, parceiro.contato, parceiro.pulseiras_adotadas]
            print('{}'.format(doc_data))
    if collection == 'pulseiras':
        for doc in docs:
            pulseira = Pulseira.from_dict(doc.to_dict())
            doc_data = [pulseira.pulseira_id, pulseira.usuario_id_atual, pulseira.usuario_id_passado, pulseira.checkpoints]
            print('{}'.format(doc_data))
    if collection == 'trilhas':
        for doc in docs:
            trilha = Trilha.from_dict(doc.to_dict())
            doc_data = [trilha.nome, trilha.trilha_id, trilha.visitas]
            print('{}'.format(doc_data))
    if collection == 'sensores':
        for doc in docs:
            sensor = Sensor.from_dict(doc.to_dict())
            doc_data = [sensor.sensor_id, sensor.trilha_id, sensor.posicao, sensor.pareamentos]
            print('{}'.format(doc_data))
    if collection == 'usuarios':
        for doc in docs:
            usuario = Usuario.from_dict(doc.to_dict())
            doc_data = [usuario.nome, usuario.usuario_id, usuario.deficiencia, usuario.idade, usuario.checkpoints]
            print('{}'.format(doc_data))
    # [END .get collection WITH deficienciaAL] #

# [START .get collection WITH TWO deficienciaALS] #
def get_compound_query_collection_data(collection, data, comparative, value, data2, comp2, value2):
    doc_ref = db.collection(collection)
    docs = doc_ref.where(data, comparative, value).get()
    docs2 = doc_ref.where(data2, comp2, value2).get()
    data_set1 = []
    data_set2 = []
    if collection == 'parceiros':
        for doc in docs:
            parceiro = Parceiro.from_dict(doc.to_dict())
            doc_data = [parceiro.nome, parceiro.parceiro_id, parceiro.contato, parceiro.pulseiras_adotadas]
            data_set1.append(tuple(doc_data))
        for doc in docs2:
            parceiro = Parceiro.from_dict(doc.to_dict())
            doc_data = [parceiro.nome, parceiro.parceiro_id, parceiro.contato, parceiro.pulseiras_adotadas]
            data_set2.append(tuple(doc_data))
    if collection == 'pulseiras':
        for doc in docs:
            pulseira = Pulseira.from_dict(doc.to_dict())
            doc_data = [pulseira.pulseira_id, pulseira.usuario_id_atual, pulseira.usuario_id_passado, pulseira.checkpoints]
            data_set1.append(tuple(doc_data))
        for doc in docs2:
            pulseira = Pulseira.from_dict(doc.to_dict())
            doc_data = [pulseira.pulseira_id, pulseira.usuario_id_atual, pulseira.usuario_id_passado, pulseira.checkpoints]
            data_set2.append(tuple(doc_data))
    if collection == 'trilhas':
        for doc in docs:
            trilha = Trilha.from_dict(doc.to_dict())
            doc_data = [trilha.nome, trilha.trilha_id, trilha.visitas]
            data_set1.append(tuple(doc_data))
        for doc in docs2:
            trilha = trilha.from_dict(doc.to_dict())
            doc_data = [trilha.nome, trilha.trilha_id, trilha.visitas]
            data_set2.append(tuple(doc_data))
    if collection == 'sensores':
        for doc in docs:
            sensor = Sensor.from_dict(doc.to_dict())
            doc_data = [sensor.sensor_id, sensor.trilha_id, sensor.posicao, sensor.pareamentos]
            data_set1.append(tuple(doc_data))
        for doc in docs2:
            sensor = Sensor.from_dict(doc.to_dict())
            doc_data = [sensor.sensor_id, sensor.trilha_id, sensor.posicao, sensor.pareamentos]
            data_set2.append(tuple(doc_data))
    if collection == 'usuarios':
        for doc in docs:
            usuario = Usuario.from_dict(doc.to_dict())
            doc_data = [usuario.nome, usuario.usuario_id, usuario.deficiencia, usuario.idade, usuario.checkpoints]
            data_set1.append(tuple(doc_data))
        for doc in docs2:
            usuario = Usuario.from_dict(doc.to_dict())
            doc_data = [usuario.nome, usuario.usuario_id, usuario.deficiencia, usuario.idade, usuario.checkpoints]
            data_set2.append(tuple(doc_data))
    intersection = list(set(data_set1).intersection(data_set2))
    print(intersection)
    #print(type(intersection))
    print(intersection[0][0])
    # [END .get collection WITH TWO deficienciaALS] #

# [START .get collection WITH deficienciaAL INTERVAL] #
def get_interval_query_collection_data(collection, data, comparative, value, data2, comp2, value2):
    doc_ref = db.collection(collection)
    docs = doc_ref.where(
        data,comparative,value).where(data2, comp2, value2).get()
    if collection == 'parceiros':
        for doc in docs:
            parceiro = Parceiro.from_dict(doc.to_dict())
            doc_data = [parceiro.nome, parceiro.parceiro_id, parceiro.contato, parceiro.pulseiras_adotadas]
            print('{}'.format(doc_data))
    if collection == 'pulseiras':
        for doc in docs:
            pulseira = Pulseira.from_dict(doc.to_dict())
            doc_data = [pulseira.pulseira_id, pulseira.usuario_id_atual, pulseira.usuario_id_passado, pulseira.checkpoints]
            print('{}'.format(doc_data))
    if collection == 'trilhas':
        for doc in docs:
            trilha = Trilha.from_dict(doc.to_dict())
            doc_data = [trilha.nome, trilha.trilha_id, trilha.visitas]
            print('{}'.format(doc_data))
    if collection == 'sensores':
        for doc in docs:
            sensor = Sensor.from_dict(doc.to_dict())
            doc_data = [sensor.sensor_id, sensor.trilha_id, sensor.posicao, sensor.pareamentos]
            print('{}'.format(doc_data))
    if collection == 'usuarios':
        for doc in docs:
            usuario = Usuario.from_dict(doc.to_dict())
            doc_data = [usuario.nome, usuario.usuario_id, usuario.deficiencia, usuario.idade, usuario.checkpoints]
            print('{}'.format(doc_data))
    # [END .get collection WITH deficienciaAL INTERVAL] #

def get_teste(primary_collection, primary_document, secondary_collection, secondary_document):
    primary_col_ref = db.collection(primary_collection)
    primary_doc_ref = primary_col_ref.document(primary_document)
    secondary_col_ref = primary_doc_ref.collection(secondary_collection)
    secondary_doc_ref = secondary_col_ref.document(secondary_document)
    if primary_collection == 'pulseira':
        primary_col_ref.document('200000006').set(
            Pulseira('200000006', '500000001' '500000006', [100, 200, 400]).to_dict())

def add_timestamp():
    # [REFERENCE collection (AND/OR document)]
    parceiro_ref = db.collection('parceiros')
    # [ADD MULTIPLE EXAMPLES FOR parceiro]
    parceiro_ref.document('100000001').set(
        Parceiro('Cliente', '100000001', 'cliente@clientemail.com', ['400000001', '400000002'], ['01']).to_dict())
    parceiro_ref.document('100000001').add(
        {'created': db.FieldValue.serverTimestamp()})
    # [END OF parceiro DATA SAMPLE]

add_timestamp()
#1get_simple_query_collection_data('usuarios', 'highest', '>', 7)
#get_interval_query_collection_data('usuarios', 'idade', '>', 20, 'idade', '<', 30)
#get_collection_data('usuarios','nome')
#update_data_transaction_result('usuarios','500000111','highest')
#check_data_existance('usuarios','500000111')