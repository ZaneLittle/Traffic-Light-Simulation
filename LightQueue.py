from Car import Car


class LightQueue:
    '''
    Represents the queue at each direction of a light
    '''

    def __init__(self, cars=[], time=0):
        self.cars = cars
        for i in range(len(self.cars)):
            self.cars[i].start_time = time
    

    def pushCar(self, car, time):
        ''' 
        Add a single car to the end of the queue and sets its start time
        '''
        car.start_time = time
        self.cars.append(car)

    def popCar(self):
        ''' 
        Pop a single car off the beginning of the queue and return it 
        '''
        return self.cars.pop(0)

    def getCost(self, time):
        return sum([time - car.start_time for car in self.cars])
