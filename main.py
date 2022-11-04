#PULSE SENSOR

from machine import ADC, Pin, Signal, Timer

adc = ADC(0)
# On my board on = off, need to reverse.
led = Signal(Pin(2, Pin.OUT), invert=True)

MAX_HISTORY = 250

# Maintain a log of previous values to
# determine min, max and threshold.
history = []
beat = False
beats = 0

def calculate_bpm(t):
    global beats
    print('BPM:', beats * 6)
    beats = 0

timer = Timer(1)
timer.init(period = 10000, mode = Timer.PERIODIC, callback = calculate_bpm)

j = 0
while (j<=10):
    for i in range(500):
        v = adc.read()   # range = 0 - 1023
        history.append(v)

    # Get the tail, up to MAX_HISTORY length
    history = history[-MAX_HISTORY:]
    
    minima, maxima = min(history), max(history)

    threshold_on = (minima + maxima * 3) // 4   # 3/4
    threshold_off = (minima + maxima) // 2      # 1/2

    if not beat and v > threshold_on:
        beat = True
        beats += 1
        led.on()

    if beat and v < threshold_off:
        beat = False
        led.off()
j += 1

# TEMPERATURE SENSOR CODE:

# from machine import ADC

# adc = ADC(0)

# for i in range(10):
#     def temp(value):
#         return value/10

#     def fahrenheit(celsius):
#         return (celsius * (9/5)) + 32

#     reading = adc.read()
#     celsius_temp = temp(reading)
#     fahrenheit_temp = fahrenheit(celsius_temp)

#     print("reading {}\nDegrees Celsius {}\nDegrees Faherenheit {}".format(reading, celsius_temp, fahrenheit_temp))