import numpy as np

class Feature(object):
    '''
    The Feature() class contains anything which might be a feature in a room;
    that is, if it would appear in or alter the room, it would be here.
    '''
    def __init__(self, name = 'Feature', description = None, HP = 1,
                 modify = False, icon = '?'):
        '''
        Initializes the Feature() class.
        Inputs:
            - name: the name of the feature (default 'Feature'). (any type)
            - description: a description of the feature (default None). (str
                or None)
            - HP: the Hit Points of the feature (default 1). (int)
            - modify: if True, will be able to modify the chape of the Room()
                it is in (for example, an indentation would change the room
                shape slightly). Default False. (boolean)
            -

        '''
        self.name = name
        self.description = description
        self.HP = HP
        self.modify = modify
        self.exists = True
        self.icon = icon
        if len(icon) > 1:
            raise ValueError("icon must be a str of length 1")

    def delete_feature(self):
