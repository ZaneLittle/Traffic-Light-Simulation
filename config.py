LIGHT_CONSTANTS = {
    "ACTION_DIR": {  # direction the car is facing in that queue
        "n": 0,
        "e": 1,
        "s": 2,
        "w": 3
    },
    "TIME_BINS": {
        "small_wait": 15,  # small waits are >0 and <= 15
        "medium_wait": 30  # medium waits are >15 and <= 30
    }
}

ENV_CONSTANTS = {
    "LIGHT_POSITIONS":{
        "NW": 0,
        "NE": 1,
        "SE": 2,
        "SW": 3
    },
    "QUEUE_DIR": LIGHT_CONSTANTS["ACTION_DIR"],
    "MAX_CARS": 100,
    "RUSH_HOUR_TIMES": [(5,10),(15,20)]
}

CAR_CONSTS = {
    "MAX_DELAY": 2
}
