import machine
import neopixel
import time
import random


# GPIO Pin Configuration
NUM_LEDS = 16
NEOPIXEL_GPIO_PIN = 19
AMBER_FLAME_BTN_GPIO_PIN = 4
GREEN_FLAME_BTN_GPIO_PIN = 2
CONSTANT_AMBER_FLAME_BTN_GPIO_PIN = 1
BLUE_FLAME_BTN_GPIO_PIN = 3
ONBOARD_LED_GPIO_PIN = 25

# Hardware Setup
neoPixel = neopixel.NeoPixel(machine.Pin(NEOPIXEL_GPIO_PIN), NUM_LEDS)
led = machine.Pin(ONBOARD_LED_GPIO_PIN, machine.Pin.OUT)
amberFlameButton = machine.Pin(AMBER_FLAME_BTN_GPIO_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
greenFlameButton = machine.Pin(GREEN_FLAME_BTN_GPIO_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
toggleFlameButton = machine.Pin(CONSTANT_AMBER_FLAME_BTN_GPIO_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
blueFlameButton = machine.Pin(BLUE_FLAME_BTN_GPIO_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# Utility Functions
def Clear():
    neoPixel.fill((0, 0, 0))
    neoPixel.write()

def FlashOnboardLed(duration_ms=100):
    led.value(1)
    time.sleep_ms(duration_ms)
    led.value(0)

def StartRgbChase():
    for color in [(255, 0, 0), (0, 0, 255), (0, 255, 0)]:
        for i in range(NUM_LEDS):
            neoPixel.fill((0, 0, 0))
            neoPixel[i] = color
            neoPixel.write()
            time.sleep(0.05)
    Clear()

def GetFlameColorForMode(mode):
    if mode == 1:  # Amber
        return [random.randint(220, 255), random.randint(60, 100), 0]
    if mode == 2:  # Green
        return [random.randint(10, 40), random.randint(180, 255), random.randint(0, 30)]
    if mode == 8:  # Blue
        return [random.randint(0, 40), random.randint(80, 120), random.randint(200, 255)]
    return [255, 80, 0]

def AddColorVariance(baseColor): #Simulates Flame Flicker
    return [
        min(255, max(0, baseColor[0] + random.randint(-10, 10))),
        min(255, max(0, baseColor[1] + random.randint(-10, 10))),
        min(255, max(0, baseColor[2] + random.randint(-10, 10)))
    ]

def GetTransitionFlickerColor(c1, c2, t):
    return [int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)]

def GetElapsedTime(start, duration):
    return time.ticks_diff(time.ticks_ms(), start) / duration

def GetRandomFlameDuration():
    return time.ticks_add(time.ticks_ms(), random.randint(55 * 60 * 1000, 65 * 60 * 1000))

def IsFlameDurationExpired(endTime):
    return time.ticks_diff(endTime, time.ticks_ms()) < 0

def GetPressedFlameButton(lastState, lastTime, debounceDelay):
    currentTime = time.ticks_ms()
    state = (
        (amberFlameButton.value() == 0) << 0 |
        (greenFlameButton.value() == 0) << 1 |
        (toggleFlameButton.value() == 0) << 2 |
        (blueFlameButton.value() == 0) << 3
    )
    if state != 0 and lastState == 0:
        if time.ticks_diff(currentTime, lastTime) > debounceDelay:
            return state, currentTime
    return 0, lastTime

# Main Execution
def Init():
    FlashOnboardLed(500)
    StartRgbChase()

def Main():
    isFlameActive = False
    isFlameToggled = False
    activeFlameMode = 0
    flameEnd = 0
    baseColor = [255, 80, 0]
    currentColor = baseColor
    nextColor = baseColor
    transitionStart = time.ticks_ms()
    flickerSpeed = random.randint(100, 400)

    lastButtonState = 0
    lastButtonTime = 0
    debounceDelay = 200
    while True:
        pressedButton, lastButtonTime = GetPressedFlameButton(lastButtonState, lastButtonTime, debounceDelay)
        lastButtonState = pressedButton

        if pressedButton:
            FlashOnboardLed()
            if pressedButton in (1, 2, 8):
                if isFlameActive and activeFlameMode == pressedButton:
                    isFlameActive = False
                    isFlameToggled = False
                    activeFlameMode = 0
                    Clear()
                else:
                    isFlameActive = True
                    isFlameToggled = False
                    activeFlameMode = pressedButton
                    flameEnd = GetRandomFlameDuration()
                    baseColor = GetFlameColorForMode(pressedButton)
                    currentColor = AddColorVariance(baseColor)
                    nextColor = AddColorVariance(baseColor)
                    transitionStart = time.ticks_ms()
                    flickerSpeed = random.randint(100, 400)
            elif pressedButton == 4:
                isFlameToggled = not isFlameToggled
                isFlameActive = isFlameToggled
                activeFlameMode = 0
                if isFlameToggled:
                    baseColor = GetFlameColorForMode(1)
                    currentColor = AddColorVariance(baseColor)
                    nextColor = AddColorVariance(baseColor)
                    transitionStart = time.ticks_ms()
                    flickerSpeed = random.randint(100, 400)
                else:
                    Clear()

        if isFlameActive:
            if not isFlameToggled and IsFlameDurationExpired(flameEnd):
                isFlameActive = False
                activeFlameMode = 0
                Clear()
            else:
                elapsed = GetElapsedTime(transitionStart, flickerSpeed)
                if elapsed >= 1:
                    currentColor = nextColor
                    nextColor = AddColorVariance(baseColor)
                    transitionStart = time.ticks_ms()
                    flickerSpeed = random.randint(100, 400)
                    elapsed = 0
                interpolated = GetTransitionFlickerColor(currentColor, nextColor, elapsed)
                for i in range(NUM_LEDS):
                    neoPixel[i] = tuple(interpolated)
                neoPixel.write()
                time.sleep_ms(20)
        else:
            time.sleep_ms(50)

Init()
Main()
                                                                                                                                