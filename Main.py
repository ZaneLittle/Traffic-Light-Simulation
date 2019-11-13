from Environment import Environment

environment = Environment(0)

# Testing route generation
routes = environment.generateRoutes()
# print(routes)

for time in range(10):
    print("Env num cars: {}".format(environment.getNumCars()))

    environment.update(time)
    # print(environment.getCost(time))
