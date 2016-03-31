import numpy as np

__doc__ = '''
Contains the Room() class as well as definitions for helping create rooms.
'''

class Room(object):
    '''
    The Room() class contains all the information about a room, and when called
    will randomly generate a room (no inputs required).
    '''
    def __init__(self, size = 'random', metric = 'imperial', shape = 'random',
                 bounds = ((5,50),(5,50),(5,50)), seed = None):
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
                room, the size tuple takes the form (radius, eccentricity,
                height)
            - bounds: the bounds for the dimensionality of the room. This is a
                3-tuple of two-tuples, one tuple for each value in the "size"
                parameter. For example, if I wanted my room to not exceed 100
                feet in width or height, and not be smaller than 20 feet in
                width or height, I would assigne the tuple:
                    bounds = ((20,100),(20,100),(20,100))
                The default is ((5,50),(5,50),(5,50)).
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
        self.metric = metric
        self.shape = shape
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
            self.random_size()

    def generate_seed(self):
        '''
        Generates a seed for the room's random generations and generates a
        numpy.random generator seeded with our seed.
        '''
        seed = np.random.randint(1, 1e10)
        self.rand = np.random.RandomState(seed)
        self.seed = seed

    def reset_seed(self):
        '''
        Resets the seed after a seed shift.
        '''
        self.rand = np.random.Randomstate(seed)
        self.seedi = 0

    def seed_increment(self):
        '''
        Increments the self.rand seed. This allows for functions to
        generate multiple random results with the same "seed", which is
        saved in self.seed.
        '''
        self.seedi += 1
        self.rand = np.random.Randomstate(seed+self.seedi)

    def random_size(self):
        '''
        Generate a random room size given a seed.
        '''
        w1 = self.rand.randint(self.bounds[0][0], self.bounds[0][1],2)
        self.seed_increment()
        w2 = self.rand.randint(self.bounds[1][0], self.bounds[1][1],2)
        self.seed_increment()
        w3 = self.rand.randint(self.bounds[2][0], self.bounds[2][1],2)
        self.size = (
            (w1[0],w1[1]),
            (w2[0],w2[1]),
            (w3[0],w3[1])
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
