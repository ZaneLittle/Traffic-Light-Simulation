import random
from Environment import Environment

class Agent:
    def __init__(self):
        ''' 
        init as equiprobable
        the policy for each light is represented as an index of the policy array 
        '''
        self.policy = [0.5, 0.5, 0.5, 0.5]

    def updateLightDirections(self, env):
        for i in range(len(self.policy)):
            if(random.random() > self.policy[i]):
                env.lights[i].direction = False
            else:
                env.lights[i].direction = False

    def updatePolicy(self):
        pass #stub