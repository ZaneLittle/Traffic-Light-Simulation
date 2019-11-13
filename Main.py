from Environment import Environment

environment = Environment(0)

# Testing route generation
routes = environment.generateRoutes()
# print(routes)

for time in range(100):
    print("Env num cars: sum({}) = {}"
          .format([light.getNumCars() for light in environment.lights],
                  environment.getNumCars()))

    environment.update(time)
    print(environment.mapEnvironmentToState(time))
    print("Total wait time: {}".format(environment.getWaitTime(time)))
