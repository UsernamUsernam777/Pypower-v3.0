
def time_apart(time1, time2):
    a = reverse_many_hms(time1)
    b = reverse_many_hms(time2)
    return abs(a - b)
def how_many_hms_in_s(sec):
    """how many hours, minutes and seconds in seconds"""
    hours = int(sec // 3600)
    minutes = int((sec % 3600) // 60)
    seconds = int((sec % 3600) % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"
def reverse_many_hms(time_str):
    result = tuple(map(int, time_str.split(':')))
    if len(result) == 2:
        s = 0
    else:
        s = result[2]
    return (result[0]*3600) + (result[1]*60) + s
