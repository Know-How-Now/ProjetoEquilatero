# [START: USER PROFILE -- LEFT WRIST] # 
class Profile(object): #profile_id = 5 + deficiência {range(0,6)} + sensor_id // ex.: 50+28101001 or 5628101001
    def __init__(self, sex, birthdate=0, group_size=0, control_id=0, **kwargs):
        self.sex = sex
        self.birthdate = birthdate
        self.group_size = group_size
        self.control_id = control_id
        self.__dict__.update(kwargs)

    @staticmethod
    def from_dict(source):
        profile = Profile(source['sex'], source['birthdate'], source['group_size'], source['control_id'])
        return profile

    def to_dict(self):
        profile_dest = {
            'sex': self.sex,
            'birthdate': self.birthdate,
            'group_size': self.group_size,
            'control_id': self.control_id
        }
        return profile_dest

    def __repr__(self):
        return 'Profile(sex={}, birthdate={}, group_size={}, control_id={})'.format(
            self.sex, self.birthdate, self.group_size, self.control_id)
    # [END: USER PROFILE -- LEFT WRIST] #
