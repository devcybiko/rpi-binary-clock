rtc = machine.RTC()
import time
from machine import Pin 
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

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
    try:
        print("Data received: ", data)  # Print the received data
        new_time = data.strip()
        hours = int(data[0:2])
        mins = int(data[2:4])
        secs = int(data[4:6])
        print("new time", hours,mins,secs)
        set_time(hours,mins,secs)
    except:
        set_time(12,0,0)

def set_time(hours,mins,secs):
    rtc.datetime((2023,1,1,0,hours,mins,secs,0))

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
    return dict

def next_datetime(now):
    now["secs"]=(now["secs"]+1)%60
    if now["secs"]==0:
        now["mins"]=(now["mins"]+1)%60
        if now["mins"]==0:
            now["hours"]=(now["hours"]+1)%24
    return now

def split_int(n, d):
    a = int(n/d)
    b = n % d
    return [a,b]

def set_leds(bits, leds):
    for i in range(0, len(leds)):
        leds[i].value(bits[i])

def to_binary(n, bits):
    arr = []
    for _ in range(bits):
        bit = n % 2
        arr.append(bit)
        n = n >> 1
    return arr

def main():
    [ble, sp] = init_ble()
    set_time(12,0,0)
    print(rtc.datetime())
    print("starting...")
    secs_lo_leds = init_gpio([0,1,2,3])
    secs_hi_leds = init_gpio([4,5,6])
    mins_lo_leds = init_gpio([7,8,9,10])
    mins_hi_leds = init_gpio([11,12,13])
    hours_leds = init_gpio([14,15,16,17])
    
    now = get_datetime()

    while True:
        if sp.is_connected():  # Check if a BLE connection is established
            sp.on_write(on_rx)  # Set the callback function for data reception
        time.sleep_ms(500)
        now = get_datetime()
        #now = next_datetime(now)
        #newtime=to_tuple(now)
        hours = now["hours"] % 12
        mins = now["mins"]
        secs = now["secs"]
        if hours == 0: hours = 12
        
        [mins_hi, mins_lo] = split_int(mins, 10)
        [secs_hi, secs_lo] = split_int(secs, 10)
        
        print(hours, mins_hi, mins_lo, secs_hi, secs_lo)
        
        bin_hours = to_binary(hours)
        bin_mins_hi = to_binary(mins_hi)
        bin_mins_lo = to_binary(mins_lo)
        bin_secs_hi = to_binary(secs_hi)
        bin_secs_lo = to_binary(secs_lo)
        
        print(bin_hours)
        
        set_leds(bin_hours, hours_leds)
        set_leds(bin_mins_hi, mins_hi_leds)
        set_leds(bin_mins_lo, mins_lo_leds)
        set_leds(bin_secs_hi, secs_hi_leds)
        set_leds(bin_secs_lo, secs_lo_leds)
        
        print("...")
        #rtc.datetime(newtime)
        #print("?",now)
    
main()