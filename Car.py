class Car:
    '''
    Defines each car in the environment
    :start_time: (int) the time the car got to a light, None if not at a light
    :route: a list of directions representing the route the car will take through the environment 
        route is represented as follows: ['n', 's', 'e', 'w']
    '''

    def __init__(self, route, start_time=None):
        #self.startLocation = route.pop(0)
        self.MAX_DELAY = 2
        self.route = route
        self.start_time = start_time
        self.delay = 0
