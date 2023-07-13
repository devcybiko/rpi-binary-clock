rtc = machine.RTC()
import time
from machine import Pin 
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
from machine import Pin 

# Create a Pin object for the onboard LED, configure it as an output
led = Pin("LED", Pin.OUT)

# Initialize the LED state to 0 (off)
led_state = 0

HOLD = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
SLOW = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_UP)
FAST = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)

gnow=0
delay = 100
DEBUG = False
NOON = {
        "year": 2023,
        "month": 1,
        "day": 1,
        "weekday": 1,
        "hours": 12,
        "mins": 0,
        "secs": 0,
        "subsecs": 0,
    }
def init_ble():
    ble = bluetooth.BLE()
    sp = BLESimplePeripheral(ble)
    return [ble, sp]

def init_gpio(pins):
    arr = []
    for i in range(0,len(pins)):
        arr.append(Pin(pins[i], Pin.OUT))
    return arr

# Define a callback function to handle received data
def on_rx(data):
    global gnow
    global delay
    global DEBUG
    
    try:
        print("Data received: ", data)  # Print the received data
        words = data.decode('ascii').strip().split(" ", 1)
        print(words)
        if words[0] == "time":
            new_time = words[1].strip()
            gnow = dup_datetime(NOON)
            gnow["hours"] = int(new_time[0:2])
            gnow["mins"] = int(new_time[2:4])
            gnow["secs"] = int(new_time[4:6])
            print("new time", gnow)
            set_datetime(gnow)
            gnow = get_datetime()
        if words[0] == "delay":
            delay = int(words[1].strip())
        if words[0] == "debug":
            DEBUG = words[1] == "on"
    except:
        print("ERROR... resetting clock")
        set_datetime(NOON)

def dup_datetime(now):
    return dict(now)
    
def set_datetime(now):
    prev_now = prev_datetime(now)  ### fixes a quirk in RTC
    tup = to_tuple(prev_now)
    rtc.datetime(tup)

def to_tuple(now):
    return (now["year"], now["month"], now["day"], now["weekday"], now["hours"], now["mins"], now["secs"], now["subsecs"])

def get_datetime():
    now=rtc.datetime()
    #print(now)
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

def next_datetime(_now, dh=0, dm=0, ds=1):
    now = dup_datetime(_now)
    now["secs"] += ds
    now["mins"] += dm
    now["hours"] += dh
    
    if now["secs"] > 59:
        now["mins"] += now["secs"] // 60
        now["secs"] = now["secs"] % 60
    if now["mins"] > 59:
        now["hours"] += now["mins"] // 60
        now["mins"] = now["mins"] % 60
    if now["hours"] > 23:
        now["hours"] = now["hours"] % 24
    return now;

def prev_datetime(_now):
    now = dup_datetime(_now)
    now["secs"] -= 1
    if now["secs"] < 0:
        now["secs"] = 59
        now["mins"] -= 1
        if now["mins"] < 0:
            now["mins"] = 59
            now["hours"] -= 1
            if now["hours"] < 0:
                now["hours"] = 23
    return now;

def split_int(n, d):
    a = int(n/d)
    b = n % d
    return [a,b]

def set_leds(bits, leds):
    for i in range(0, len(leds)):
        leds[i].value(bits[i])

def main():
    global gnow
    global delay
    global DEBUG
    global led_state
        
    [ble, sp] = init_ble();
    set_datetime(NOON)
    print(rtc.datetime())
    print("starting...")
    secs_lo_leds = init_gpio([0,1,2,3])
    secs_hi_leds = init_gpio([4,5,6])
    mins_lo_leds = init_gpio([7,8,9,10])
    mins_hi_leds = init_gpio([11,12,13])
    hours_leds = init_gpio([14,15,16,17])
    
    gnow = get_datetime()
    DEFAULT_DELAY = 100
    delay = DEFAULT_DELAY
    reset_secs = False
    
    while True:
        if sp.is_connected():  # Check if a BLE connection is established
            sp.on_write(on_rx)  # Set the callback function for data reception

        gnow = get_datetime()
        
        if not DEBUG:
            delay = DEFAULT_DELAY
        else:
            gnow = next_datetime(gnow);

        if HOLD.value():
            hold_time = get_datetime()
            set_datetime(hold_time)
        
        if FAST.value() == 0:
            print(gnow)
            gnow = next_datetime(gnow, 0, 0, 59)
            set_datetime(gnow)
            delay = 20
            reset_secs = "fast"
        elif reset_secs == "fast":
#            gnow["secs"] = 0
#            gnow["mins"] = 0
            set_datetime(gnow)
            print(reset_secs, gnow)
            reset_secs = False

        if SLOW.value() == 0:
            gnow = next_datetime(gnow, 0, 0, 1)
            set_datetime(gnow)
            delay = 1
            reset_secs = "slow"
        elif reset_secs == "slow":
#           gnow["secs"] = 0
            set_datetime(gnow)
            print(reset_secs, gnow)
            reset_secs = False
              
        if delay: time.sleep_ms(delay)
        hours = gnow["hours"] % 12
        mins = gnow["mins"]
        secs = gnow["secs"]
        if hours == 0: hours = 12
        
        [mins_hi, mins_lo] = split_int(mins, 10)
        [secs_hi, secs_lo] = split_int(secs, 10)
                
        bin_hours = to_binary(hours)
        bin_mins_hi = to_binary(mins_hi)
        bin_mins_lo = to_binary(mins_lo)
        bin_secs_hi = to_binary(secs_hi)
        bin_secs_lo = to_binary(secs_lo)
        
        #print(bin_hours)
        
        set_leds(bin_hours, hours_leds)
        set_leds(bin_mins_hi, mins_hi_leds)
        set_leds(bin_mins_lo, mins_lo_leds)
        set_leds(bin_secs_hi, secs_hi_leds)
        set_leds(bin_secs_lo, secs_lo_leds)
        
        led_state = not led_state
        led.value(led_state)
        #print("...")
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
    arr = [d, c, b, a]
    arr.reverse()
    return arr
    
main()