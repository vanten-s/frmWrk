import datetime

enable_logging = True
log_file = "log.txt"

def log(func):
    def wrapper(*args, **kwargs):
        if not enable_logging: return func(*args, **kwargs)
        returnVal = func(*args, **kwargs)
        with open(log_file, "a") as f:
            try:
                if len(returnVal) < 100:
                    f.write(f"{func.__name__} was called at {datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} and returned {returnVal}\n")
                else:
                    f.write(f"{func.__name__} was called at {datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}\n")
            except TypeError as e:
                f.write(f"{func.__name__} was called at {datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}\n")    

        return returnVal
    
    return wrapper


def log_string(string):
    if not enable_logging: return string
    with open(log_file, "a") as f:
        f.write(f"{string}\n")
    return string




