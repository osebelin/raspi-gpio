from time import sleep 
from gpiozero import LED, Button
from signal import pause
from thread import start_new_thread
import RPi.GPIO as GPIO

# start mit python /home/pi/blinkenlights/blinkenlights.py

led1 = LED(5)
led2 = LED(11)
led3 = LED(9)
led4 = LED(10)
led5 = LED(22)


button1 = Button(2)
button2 = Button(3)
button3 = Button(4)
button4 = Button(17)
button5 = Button(27)

leds = [led1, led2, led3, led4, led5]
leds_reverse = leds[::-1]
buttons = [button1, button2, button3, button4, button5]

actions = [None] * 33


button_state = 0

action = None
keep_running=True

def all_off():
        for led in leds:
            led.off()

def all_on():
        for led in leds:
            led.on()

def led1_on():
    leds[0].on()

def led4_on():
    leds[3].on()

def led5_on():
    leds[4].on()

def blink_all():
    for led in leds:
        led.on()
    sleep(0.2)
    for led in leds:
        led.off()
    sleep(0.2)


def blink_circle():
    for led in leds:
        led.on()
        sleep(0.2)
        led.off()
        sleep(0.2)

def blink_odd_even():
    leds[0].on()
    leds[2].on()
    leds[4].on()
    leds[1].off()
    leds[3].off()
    sleep(0.4)
    leds[0].off()
    leds[2].off()
    leds[4].off()
    leds[1].on()
    leds[3].on()
    sleep(0.4)


def inverted_blink_circle():
    for led in leds:
        led.on()
    for led in leds:
        led.off()
        sleep(0.1)
        led.on()
        sleep(0.1)

def caterpillar():
    for led in leds:
        led.on()
        sleep(0.1)
    for led in leds:
        led.off()
        sleep(0.1)

def reverse_caterpillar():
    for led in leds_reverse:
        led.on()
        sleep(0.1)
    for led in leds_reverse:
        led.off()
        sleep(0.1)

def equalizer():
    for led in leds:
        led.on()
        sleep(0.1)
    sleep(0.2)
    for led in leds_reverse:
        led.off()
        sleep(0.1)

def reverse_equalizer():
    for led in leds_reverse:
        led.on()
        sleep(0.1)
    sleep(0.2)
    for led in leds:
        led.off()
        sleep(0.1)

def outer_to_inner():
    leds[0].on()
    leds[4].on()
    sleep(0.1)
    leds[1].on()
    leds[3].on()
    sleep(0.1)
    leds[2].on()
    sleep(0.2)
    leds[0].off()
    leds[4].off()
    sleep(0.1)
    leds[1].off()
    leds[3].off()
    sleep(0.1)
    leds[2].off()
    sleep(0.1)

def inner_to_outer():
    leds[2].on()
    sleep(0.1)
    leds[1].on()
    leds[3].on()
    sleep(0.1)
    leds[0].on()
    leds[4].on()
    sleep(0.4)
    leds[0].off()
    leds[4].off()
    sleep(0.1)
    leds[1].off()
    leds[3].off()
    sleep(0.1)
    leds[2].off()
    sleep(0.1)


def watch_action():
    global keep_running;
    global action
    last_action=None
    while keep_running:
        eval_action()
        if action != None:
            if last_action != action:
                all_off()
            last_action = action
            try:
                action()
            except:
                all_off()
        else:
            all_off()
            sleep(0.05)


def eval_button_states():
    res = 0
    for num, button in enumerate(buttons, start=0):
        if button.is_pressed:
            res = res | 1 << num 
    return res


def eval_action():
    global button_state
    global action
    default_action=None
    new_button_state = eval_button_states()
    if button_state != new_button_state:
        button_state = new_button_state
        action = actions[button_state]
        if action == None:
            action=default_action
            print("Button state: {} => default_action".format(button_state))
        else:
            print("Button state: {}".format(button_state))


def on_button():
    eval_action()


actions[0]=all_off
actions[16]=leds[0].on
actions[8]=leds[1].on
actions[4]=leds[2].on
actions[2]=leds[3].on
actions[1]=leds[4].on
actions[24]=blink_all
actions[20]=blink_circle
actions[26]=inverted_blink_circle
actions[22]=caterpillar
actions[23]=reverse_caterpillar
actions[10]=blink_odd_even
actions[11]=equalizer
actions[7]=reverse_equalizer
actions[19]=all_on
actions[27]=outer_to_inner
actions[21]=inner_to_outer
actions[25]=inner_to_outer

#for button in buttons:
#    button.when_pressed = on_button
#    button.when_released = on_button

try:
    blink_all()
    start_new_thread(watch_action, ())
    pause()
finally:
    print("finally")
    keep_running = False
    sleep(0.2)

# finally:
#   GPIO.cleanup()

