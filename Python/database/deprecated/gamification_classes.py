# [START: GAMIFICATION PROFILE -- RIGHT WRIST] #
class Gamification(object): #gamification_id = user_id + sensor_id // ex.: 60+28101001 or 1000+28101001, or 9999+28101001
    def __init__(self, title, experience=0, milestones=[''], achievements=[''], control_id=[0], **kwargs):
        self.title = title
        self.experience = experience
        self.milestones = milestones
        self.achievements = achievements
        self.control_id = control_id
        self.__dict__.update(kwargs)

    @staticmethod
    def from_dict(source):
        gamification = Gamification(source['title'])
        if 'experience' in source:
            gamification.experience = source['experience']
        if 'milestones' in source:
            gamification.milestones = source['milestones']
        if 'checkpoints' in source:
            gamification.achievements = source['achievements']
        if 'control_id' in source:
            gamification.control_id = source['control_id']
        return gamification

    def to_dict(self):
        gamification_dest = {
            'title': self.title
        }
        if self.experience:
            gamification_dest['experience'] = self.experience
        if self.milestones:
            gamification_dest['milestones'] = self.milestones
        if self.achievements:
            gamification_dest['achievements'] = self.achievements
        if self.control_id:
            gamification_dest['control_id'] = self.control_id
        return gamification_dest

    def __repr__(self):
        return 'Gamification(title={}, experience={}, milestones={}, achievements={}, control_id={})'.format(
            self.title, self.experience, self.milestones, self.achievements, self.control_id)
    # [END: GAMIFICATION PROFILE -- RIGHT WRIST] #
