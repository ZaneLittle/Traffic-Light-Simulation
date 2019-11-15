from Environment import Environment

environment = Environment(0)

# Testing route generation
routes = environment.generateRoutes()
# print(routes)

for time in range(10):
    print("Time step: {}".format(time))
    # print("Env num cars: sum({}) = {}"
    #       .format([light.getNumCars() for light in environment.lights],
    #               environment.getNumCars()))
    i = 0
    for light in environment.lights:
        print("{} traffic light, queue sizes: {}".format(["NW","NE","SE","SW"][i], list(zip([['n','e','s','w'][j] for j in range(4)],[queue.getNumCars() for queue in light.queues]))))
        i = i + 1
    # print(environment.mapEnvironmentToState(time))
    # print("Total wait time: {}".format(environment.getWaitTime(time)))

    environment.update(time)
