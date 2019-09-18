from time import sleep 
from gpiozero import LED, Button
from signal import pause
from thread import start_new_thread

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
buttons = [button1, button2, button3, button4, button5]

button_state = 0

def all_off():
        for led in leds:
            led.off()

def blink_all():
    start_state=button_state
    while start_state == button_state:
        for led in leds:
            led.on()
        sleep(0.2)
        for led in leds:
            led.off()
        sleep(0.2)


def blink_circle():
    start_state=button_state
    while start_state == button_state:
        for led in leds:
            led.on()
            sleep(0.2)
            led.off()
            sleep(0.2)

def inverted_blink_circle():
    start_state=button_state
    while start_state == button_state:
        for led in leds:
            led.on()
        for led in leds:
            led.off()
            sleep(0.1)
            led.on()
            sleep(0.1)


def eval_button_states():
    res = 0
    for num, button in enumerate(buttons, start=0):
        if button.is_pressed:
            res = res | 1 << num 
    return res

def on_button():
    global button_state
    new_button_state = eval_button_states()
    if button_state != new_button_state:
        button_state = new_button_state
        print("New button state: {}".format(button_state))
        if button_state == 1:
            start_new_thread(blink_all, ())
        elif button_state == 2:
            start_new_thread(blink_circle, ())
        elif button_state == 3:
            start_new_thread(inverted_blink_circle, ())
        elif button_state == 0:
            all_off()
for button in buttons:
    button.when_pressed = on_button
    button.when_released = on_button

pause()

# finally:
#   GPIO.cleanup()

