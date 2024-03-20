import time

def get_current_time(action):
    '''
    fix the timeshift of different time zone
    '''
    offset = 8*3600 if action else 0
    return time.strftime("%H:%M:%S", time.localtime(time.time() + offset))
