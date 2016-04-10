import numpy as np
import pickle as pc

__doc__ = '''
Contains the Room() class as well as definitions for helping create rooms.
'''

class Room(object):
    '''
    The Room() class contains all the information about a room, and when called
    will randomly generate a room (no inputs required).
    '''
    def __init__(self, size = 'random', metric = 'imperial', shape = 'random',
                 bounds = ((5,50),(5,50),(5,50)), walls = 'random',
                 seed = None):
        '''
        Initializes the Room() class.

        Inputs:
            - size: 3-tuple such that it is (width1, width2, height), or a sting
                containing the word "random" (default). (3-tuple, string)
            - metric: the system of measurements to be used
                (options: 'imperial','metric'). Default imperial system.
                (string)
            - shape: the shape of the room, current options: 'random',
                'rectangle', 'ellipse'. (string) For a non-rectangular/polygonal
                room, the size tuple takes the form (semimajor, semiminor,
                height) (semimajor/semiminor axes)
            - bounds: the bounds for the dimensionality of the room. This is a
                3-tuple of two-tuples, one tuple for each value in the "size"
                parameter. For example, if I wanted my room to not exceed 100
                feet in width or height, and not be smaller than 20 feet in
                width or height, I would assigne the tuple:
                    bounds = ((20,100),(20,100),(20,100))
                The default is ((5,50),(5,50),(5,50)).
            - walls: the type of wall material. 'random' will pick from the
                following list:
                - 'good quality stone'
                - 'poor quality stone'
                - 'good quality wood'
                - 'poor quality wood'
                - 'dirt, compacted'
                - 'dirt, loose'
                Default is 'random'. Can change possible options and their
                weights in the file 'room.in'
            - seed: used to recreate a particular room (int)
        '''
        # Predefined attributes
        self.allowed_size = ['random', type((0,))]
        self.allowed_metric = ['imperial','metric']
        ## Random must be first.
        self.allowed_shape = ['random','rectangle','ellipse']
        self.allowed_bounds = [type((0,))]
        self.seedi = 0

        # User-input attributes
        self.size = size
        self.metric = metric.lower()
        self.shape = shape.lower()
        self.bounds = bounds

        # Checking inputs for problems
        self.checks()

        # Checking for random inputs to generate
        if self.size == 'random' or self.shape == 'random':
            if seed == None:
                # This generates a see and the randomization attribute
                # self.rand, which contains all the functions contained in
                # the numpy.random module.
                self.generate_seed()
            else:
                self.seed = seed
                self.rand = np.rand.RandomState(seed)
        if self.size == 'random':
            self.random_size()
        if self.shape == 'random':
            self.random_shape()

        # Generating the room
        self.create_room()

    def generate_seed(self):
        '''
        Generates a seed for the room's random generations and generates a
        numpy.random generator seeded with our seed.
        '''
        seed = np.random.randint(1, 4294967000)
        self.rand = np.random.RandomState(seed)
        self.seed = seed

    def reset_seed(self):
        '''
        Resets the seed after a seed shift.
        '''
        self.rand = np.random.RandomState(seed)
        self.seedi = 0

    def seed_increment(self):
        '''
        Increments the self.rand seed. This allows for functions to
        generate multiple random results with the same "seed", which is
        saved in self.seed.
        '''
        self.seedi += 1
        self.rand = np.random.RandomState(self.seed+self.seedi)

    def random_size(self):
        '''
        Generate a random room size given a seed.
        '''
        w1 = self.rand.randint(self.bounds[0][0], self.bounds[0][1])
        self.seed_increment()
        w2 = self.rand.randint(self.bounds[1][0], self.bounds[1][1])
        self.seed_increment()
        w3 = self.rand.randint(self.bounds[2][0], self.bounds[2][1])
        self.size = (
            w1,
            w2,
            w3
        )

    def random_shape(self):
        guess = self.rand.randint(1,len(self.allowed_shape))
        self.shape = self.allowed_shape[guess]

    def checks(self):
        '''
        Checks to make sure all inputs are valid ones.
        '''
        allowed_size = ['random', type((0,))]
        allowed_metric = ['imperial','metric']
        allowed_shape = ['random','rectangle','ellipse']
        allowed_bounds = [type((0,))]

        if (self.size not in allowed_size and
            type(self.size) not in allowed_size):
            raise ValueError('The "size" input is not assigned an allowed input.')
        elif self.metric not in allowed_metric:
            raise Valueerror('The "metric" input is not assigned an allowed input.')
        elif self.shape not in allowed_shape:
            raise ValueError('The "shape" input is not assigned an allowed input.')
        elif (self.bounds not in allowed_bounds and
              type(self.bounds) not in allowed_bounds and
              len(self.bounds) != 3):
            raise ValueError('The "bounds" input is not assigned an allowed input.')

    def create_room(self):
        '''
        Generates the room.
        '''
        # Creating a cubical map on which to place the room's features.
        self.bgmap = np.zeros(self.size)

        # Generating the walls & ceiling.
        self.walls = self.bgmap
        if self.shape == 'rectangle':
            self.walls[0,:,:] = 1
            self.walls[:,0,:] = 1
            self.walls[:,:,0] = 1
            self.walls[self.size[0]-1,:,:] = 1
            self.walls[:,self.size[1]-1,:] = 1
            self.walls[:,:,self.size[2]-1] = 1

        elif self.shape == 'ellipse':
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    ellipes_eq = np.rint(((i+5)/self.size[0])**2 + ((j+5)/self.size[1])**2)
                    if ellipes_eq >= 1:
                        self.walls[i,j,:] = 1
                    else:
                        self.walls[i,j,:] = 0

    def roomString(self,level = 1):
        '''
        Generates a string that represents the room at a given height
        level.
        Inputs:
            - level: the level to be displayed/printed
        Outputs:
            - roomstr: a string that when printed represented the room and
                its contents.
        '''
        # Importing character settings, see character.draw
        chars = {}
        with open('character.draw','r') as infile:
            for line in infile:
                if line[0] == '*':
                    # Comment character for input files
                    # Since hashtags are used too often in chars
                    # At least, I predict they might be.
                    pass

                else:
                    # Split into list ["key","char"]
                    splitz = line.split(':')
                    chars[splitz[0]] = splitz[1][:-1]

        # Generating the string
        roomstr = ""

        # Barebones gen (floor + walls + ceiling)
        # Chopping desired level
        current_level = self.walls[:,:,level]
        for i in range(current_level.shape[0]):
            for j in range(current_level.shape[1]):
                if current_level[i,j] == 1:
                    # Wall
                    roomstr += chars['wall']
                elif current_level[i,j] == 0:
                    # Floor
                    roomstr += chars['floor']
                else:
                    # Idk yet
                    roomstr += ' '
            # Enter
            roomstr += '\n'

        #Eventually add more things here (features, etc.)

        return roomstr

# END
