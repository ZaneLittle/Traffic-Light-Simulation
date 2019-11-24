LIGHT_CONSTANTS = {
    "ACTION_DIR": {  # direction the car is facing in that queue
        "n": 0,
        "e": 1,
        "s": 2,
        "w": 3
    },
    "TIME_BINS": {
        "small_upper": 2,    # 0 < small wait <= 2
        "med_upper": 5       # 2 < medium wait <= 5                       
    }                        # large wait > 5
}

EPISODE_LEN = 50000
NUM_INTERVALS = 5

boundaryOne     = EPISODE_LEN//NUM_INTERVALS
boundaryTwo     = (EPISODE_LEN//NUM_INTERVALS)*2
boundaryThree   = (EPISODE_LEN//NUM_INTERVALS)*3
boundaryFour    = (EPISODE_LEN//NUM_INTERVALS)*4

ENV_CONSTANTS = {
    "EPISODE_LENGTH": EPISODE_LEN,
    "NUM_INTERVALS": NUM_INTERVALS,
    "LIGHT_POSITIONS":{
        "NW": 0,
        "NE": 1,
        "SE": 2,
        "SW": 3
    },
    "QUEUE_DIR": LIGHT_CONSTANTS["ACTION_DIR"],
    "MAX_CARS": 500,
    "RUSH_HOUR_TIMES":  [(boundaryOne,boundaryTwo-1),(boundaryThree,boundaryFour-1)],
    "TIME_INTERVALS": [(0,boundaryOne-1),(boundaryOne,boundaryTwo-1),(boundaryTwo,boundaryThree-1),(boundaryThree,boundaryFour-1),(boundaryFour,EPISODE_LEN-1)]
    
}

CAR_CONSTS = {
    "MAX_DELAY": 2
}


# Used to determine the size of the state by considering each variable that makes up the state
# Parameterize construction of dictionaries 
def stateEntity(quantity, numStates):
    return {"quantity": quantity, "numStates": numStates}

STATE_COSTANTS = {
    "LIGHTS": stateEntity(4,2),
    "QUEUES": stateEntity(8,1+len(LIGHT_CONSTANTS["TIME_BINS"])),   # Add one to the length here because the length is the number of boundaries, which is one more than the number of bins
    "TIME_OF_DAY": stateEntity(1,NUM_INTERVALS)
}

