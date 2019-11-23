LIGHT_CONSTANTS = {
    "ACTION_DIR": {  # direction the car is facing in that queue
        "n": 0,
        "e": 1,
        "s": 2,
        "w": 3
    },
    "TIME_BINS": {
        "small_wait": 15,   # 0 < small wait <= 15
        "medium_wait": 30   # 15 < medium wait <= 30
                            # large wait > 30
    }
}

EPISODE_LEN = 25

boundaryOne     = EPISODE_LEN//5
boundaryTwo     = (EPISODE_LEN//5)*2
boundaryThree   = (EPISODE_LEN//5)*3
boundaryFour    = (EPISODE_LEN//5)*4

ENV_CONSTANTS = {
    "EPISODE_LENGTH": EPISODE_LEN,
    "LIGHT_POSITIONS":{
        "NW": 0,
        "NE": 1,
        "SE": 2,
        "SW": 3
    },
    "QUEUE_DIR": LIGHT_CONSTANTS["ACTION_DIR"],
    "MAX_CARS": 100,
    "RUSH_HOUR_TIMES":  [(boundaryOne,boundaryTwo-1),(boundaryThree,boundaryFour-1)],
    "TIME_INTERVALS": [(0,boundaryOne-1),(boundaryOne,boundaryTwo-1),(boundaryTwo,boundaryThree-1),(boundaryThree,boundaryFour-1),(boundaryFour,EPISODE_LEN-1)]
    
}

CAR_CONSTS = {
    "MAX_DELAY": 2
}
