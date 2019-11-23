from Environment import Environment
# from Agent import Agent

environment = Environment(0)
# agent = Agent(environment)

# Create all possible routes
routes = environment.generateRoutes()

# Rush hour from traffic Lights 
routesFromTop = []  # Routes starting from light 0 or light 1
routesFromBottom = []  # Routes starting from light 2 or light 3
for route in routes:
    if route[0][0] in [0, 1]:
        routesFromTop.append(route)
    else:
        routesFromBottom.append(route)

state_tracker = []

for time in range(20):
    # state = {
    #     "lights": [light.directionIsNorthSouth
    # for light in environment.lights]
    # }
    print("Time step: {}".format(time))
    lightDirections = [
        "north/south" if light.directionIsNorthSouth
        else "east/west"
        for light in environment.lights
    ]
    print("Directions for traffic lights: {}".format(lightDirections))
    environment.update(time,routes)
    print(str(environment))
    print("state: {}, cost: {}".format(environment.mapEnvironmentToState(time),environment.getCost(time)))

