from Car import Car


class LightQueue:
    '''
    Represents the queue at each direction of a light
    '''

    def __init__(self, cars=[], time=0):
        self.cars = cars
        for i in range(len(self.cars)):
            self.cars[i].start_time = time

    def push(self, car, time):
        ''' 
        Add a single car to the end of the queue and sets its start time
        '''
        car.start_time = time
        self.cars.append(car)

    def pop(self):
        ''' 
        Pop a single car off the beginning of the queue and return it 
        '''
        return self.cars.pop(0)

    def cost(self, time):
        total_cost = 0
        for car in self.cars:
            total_cost += time - car.start_time

        return total_cost
