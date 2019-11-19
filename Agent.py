import random


class Agent:

    def __init__(self, environment):
        ''' 
        init as equiprobable
        the policy for each light is represented as an index of the policy array
        p[a|s]
        '''
        self.environment = environment
        self.policy = [0.5, 0.5, 0.5, 0.5]
        # Parameter used to alter how long the naive lights stay on for before switching direction
        self.phase_time_bound = 1
        # Time elapses since lights have last changed direction
        self.current_phase_time = 0

    def update(self, time):
        self.current_phase_time = self.current_phase_time + 1
        # For now, test with a naive, constant policy of light changing
        self.constantPolicy(time)

    def constantPolicy(self, time):
        # If enough time has elapsed, change light direction
        if self.current_phase_time >= self.phase_time_bound:
            self.current_phase_time = 0
            for light in self.environment.lights:
                # Toggle light direction
                light.changeLight(time)

    def learningPolicy(self, env):
        for i in range(len(self.policy)):
            if(random.random() > self.policy[i]):
                env.lights[i].direction = False
            else:
                env.lights[i].direction = False

    def updatePolicy(self):
        pass  # stub
