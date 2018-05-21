#EBTIDA = Earns Before Taxes, Interest, Depreciations, Amortizations#

# [START parceiro_DEF] #
class Parceiro(object):
    def __init__(self, parceiro_id, nome, contato, investiu_onde=[''], investiu_quanto=[0], retorno_ebtida=[0]):
        self.parceiro_id = parceiro_id
        self.nome = nome
        self.contato = contato
        self.investiu_onde = investiu_onde
        self.investiu_quanto = investiu_quanto #INSERIR QUANDO / TIMESTAMP
        self.retorno_ebtida = retorno_ebtida

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE] #
        parceiro = Parceiro(source['parceiro_id'], source['nome'], source['contato'])
        if 'investiu_onde' in source:
            parceiro.investiu_onde = source['investiu_onde']
        if 'investiu_quanto' in source:
            parceiro.investiu_quanto = source['investiu_quanto']
        if 'investiu_onde' in source:
            parceiro.retorno_ebtida = source['retorno_ebtida']
        return parceiro
    # [END_EXCLUDE] #

    def to_dict(self):
        # [START_EXCLUDE] #
        parceiro_dest = {
            'parceiro_id': self.parceiro_id,
            'nome': self.nome,
            'contato': self.contato
        }
        if self.investiu_onde:
            parceiro_dest['investiu_onde']
        if self.investiu_quanto:
            parceiro_dest['investiu_quanto']
        if self.retorno_ebtida:
            parceiro_dest['retorno_ebtida']
        return parceiro_dest
    # [END_EXCLUDE] #

    def __repr__(self):
        return 'Parceiro(nome={}, parceiro_id={}, contato={}, investiu_onde={}, investiu_quanto={}, retorno_ebtida={})'.format(
            self.nome, self.parceiro_id, self.contato, self.investiu_onde, self.investiu_quanto, self.retorno_ebtida)
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
    def __init__(self, usuario_id, idade=0, deficiencia=False, pulseira_id =['']):
        self.usuario_id = usuario_id
        self.idade = idade
        self.deficiencia = deficiencia
        self.pulseira_id = pulseira_id #Pulseira contem sensores, sensores contêm onde e quanto

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        usuario = Usuario(source['usuario_id'])
        if 'idade' in source:
            usuario.idade = source['idade']
        if 'deficiencia' in source:
            usuario.deficiencia = source['deficiencia']
        if 'pulseira_id' in source:
            usuario.pulseira_id = source['pulseira_id']
        return usuario
    # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        usuario_dest = {
            'usuario_id': self.usuario_id
        }
        if self.idade:
            usuario_dest['idade'] = self.idade
        if self.deficiencia:
            usuario_dest['deficiencia'] = self.deficiencia
        if self.pulseira_id:
            usuario_dest['pulseira_id'] = self.pulseira_id
        return usuario_dest
    # [END_EXCLUDE]

    def __repr__(self):
        return 'Usuario(usuario_id={}, deficiencia={}, idade={}, pulseira_id={})'.format(
            self.usuario_id, self.deficiencia, self.idade, self.pulseira_id)
    # [END Usuario_DEF] #