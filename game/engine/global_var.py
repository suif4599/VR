__glob = {'MAX_BRIGHTNESS_LEVEL': 7}

def set_var(key, value):
    __glob[key] = value

def get_var(key):
    return __glob[key]

def set_max_brightness_level(value: int):
    set_var('MAX_BRIGHTNESS_LEVEL', value)

def get_max_brightness_level() -> int:
    return get_var('MAX_BRIGHTNESS_LEVEL')