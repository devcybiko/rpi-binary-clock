rtc = machine.RTC()
import time

def to_tuple(now):
    return (now["year"], now["month"], now["day"], now["weekday"], now["hours"], now["mins"], now["secs"], now["subsecs"])

def get_datetime():
    now=rtc.datetime()
    print(now)
    dict = {
        "year": now[0],
        "month": now[1],
        "day": now[2],
        "weekday": now[3],
        "hours": now[4],
        "mins": now[5],
        "secs": now[6],
        "subsecs": now[7],
    }
    return dict;

def next_datetime(now):
    now["secs"]=(now["secs"]+1)%60
    if now["secs"]==0:
        now["mins"]=(now["mins"]+1)%60
        if now["mins"]==0:
            now["hours"]=(now["hours"]+1)%24
    return now;

def split_int(n, d):
    a = int(n/d)
    b = n % d
    return [a,b]

def main():
    rtc = machine.RTC()
    rtc.datetime((2020, 1, 1, 0, 11, 59, 0, 0))
    print(rtc.datetime())
    print("starting...")

    while True:
        # print(hours,mins,secs,":",hours_12,mins_10s,mins_01s,secs_10s,secs_01s)
        time.sleep_ms(1000)
        now = get_datetime()
        #now = next_datetime(now);
        #newtime=to_tuple(now);
        hours = now["hours"] % 12
        mins = now["mins"]
        secs = now["secs"]
        if hours == 0: hours = 12
        [mins_hi, mins_lo] = split_int(mins, 10)
        [secs_hi, secs_lo] = split_int(secs, 10)
        #print(hours, mins_hi, mins_lo, secs_hi, secs_lo)
        print(to_binary(hours))
        print(to_binary(mins_hi))
        print(to_binary(mins_lo))
        print(to_binary(secs_hi))
        print(to_binary(secs_lo))
        print("...")
        #rtc.datetime(newtime)
        #print("?",now)

def to_binary(n):
    a = n % 2
    n = n >> 1
    b = n % 2
    n = n >> 1
    c = n % 2
    n = n >> 1
    d = n % 2
    return [d, c, b, a]
    
main()