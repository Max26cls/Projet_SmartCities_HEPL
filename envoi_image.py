import camera
import network
from umqtt.simple import MQTTClient
import time
import machine
import esp32
import random
import ubinascii
import ujson
from machine import wake_reason, TIMER_WAKE

LED = machine.Pin(4, machine.Pin.OUT)
PIR = machine.Pin(2, machine.Pin.IN)

SSID = 'iPhone de Max'
PASSWORD = 'YLCJAHRK'

MQTT_BROKER = "172.20.10.3"
MQTT_PORT = 1883
TOPIC = "ProjetNichoir"

WAKE_INTERVAL_MS = 30000      #24 * 60 * 60 * 1000 pour 24h

def get_battery_level():
    return random.randint(1, 100)       
def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to WiFi...")
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            time.sleep(0.1)
    print("WiFi connected:", sta_if.ifconfig())
    return sta_if

def disconnect_wifi(sta_if):
    if sta_if.isconnected():
        sta_if.disconnect()
        sta_if.active(False)
        print("WiFi disconnected")

def publish_message(image_data, battery_level):
    if image_data:
        b64_image = ubinascii.b2a_base64(image_data).decode().replace("\n", "")
    else:
        b64_image = None

    payload = ujson.dumps({
        "battery": battery_level,
        "image": b64_image
    })
    client = MQTTClient("esp32_client", MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    client.publish(TOPIC, payload)
    print(f"Message publié : Batterie {battery_level}% {'+ image' if b64_image else '(sans image)'}")
    client.disconnect()

def initialize_camera():
    try:
        camera.init()
        camera.quality(10)
        return True
    except Exception as e:
        print("Camera init error:", e)
        return False

def capture_photo():
    if initialize_camera():
        try:
            LED.value(1)
            time.sleep(0.5)
            img = camera.capture()
            LED.value(0)
            return bytearray(img)
        finally:
            camera.deinit()
    return None

def go_to_sleep():
    print("Going to deep sleep...")
    esp32.wake_on_ext0(pin=PIR, level=esp32.WAKEUP_ANY_HIGH)
    machine.deepsleep(WAKE_INTERVAL_MS)

def main():
    print("Reset cause:", wake_reason())
    sta_if = connect_to_wifi()

    if wake_reason() == TIMER_WAKE:
        if not PIR.value():
            print("Réveil périodique (24h / attente) → capture photo + batterie")
            img = capture_photo()
            if img:
                battery_level = get_battery_level()
                publish_message(img, battery_level)
            else:
                print("Capture échouée")
            
            time.sleep(1)
            disconnect_wifi(sta_if)
            go_to_sleep()

    last_motion_time = time.time()

    while True:
        if PIR.value() == 1:
            print("Mouvement détecté !")
            last_motion_time = time.time()
            img = capture_photo()
            if img:
                battery_level = get_battery_level()
                publish_message(img, battery_level)
            else:
                print("Capture échouée")
            time.sleep(10)
        else:
            if time.time() - last_motion_time > 15:      #60:   pour 1minute pour projet final
                disconnect_wifi(sta_if)
                go_to_sleep()
        time.sleep(0.5)

main()



