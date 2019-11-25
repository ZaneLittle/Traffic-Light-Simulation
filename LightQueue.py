from Car import Car


class LightQueue:
    '''
    Represents the queue at each direction of a light
    '''

    def __init__(self, id, cars=[], time=0):
        self.id = id
        self.cars = cars[:]
        for car in self.cars:
            car.startTime = time

    def __str__(self):
        return "< Light Queue {}> ".format(self.id)

    def pushCar(self, car, time):
        ''' 
        Add a single car to the end of the queue and sets its start time
        '''
        initLength = len(self.cars)
        car.startTime = time
        self.cars.append(car)
        assert(len(self.cars) - initLength == 1)

    def peakCar(self):
        return self.cars[0]

    def popCar(self):
        ''' 
        Pop a single car off the beginning of the queue and return it 
        '''
        initNumCars = len(self.cars)
        car = self.cars.pop(0)
        assert(initNumCars - len(self.cars) == 1)
        return car

    def getNumCars(self):
        return len(self.cars)

    def getNumCarsDriving(self):
        return len([car for car in self.cars if car.delay])

    def carsWaiting(self):
        return [car for car in self.cars if not car.delay]

    def getNumCarsWaiting(self):
        return len(self.carsWaiting())

    def getWaitTimes(self, time):
        # The delay attribute in the car class represents how far away it is from 
        # starting it's "wait" in the queue. This is like saying the car isn't
        # stationary if it's delay is >0 and we don't count it towards the agent's
        # cost.
        return sum([time - car.startTime for car in self.cars if car.delay == 0])

