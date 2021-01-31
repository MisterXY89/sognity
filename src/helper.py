
import datetime

def ms_to_mins(ms):
    return ":".join(str(datetime.timedelta(milliseconds=ms)).split(":")[1:]).split(".")[0]    
