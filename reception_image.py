import os
import paho.mqtt.client as mqtt
from PIL import Image
import io, time, base64, json
from flask import Flask, render_template, send_from_directory

# --- ParamÃ¨tres MQTT ---
mqtt_broker = "172.20.10.3"
mqtt_port = 1883
mqtt_topic = "ProjetNichoir"

# --- Dossier pour sauvegarder les images ---
image_folder = "/home/Max/Documents/Photos"
os.makedirs(image_folder, exist_ok=True)

# --- Flask app ---
app = Flask(__name__)

# --- Variables ---
connected_once = False


def on_message(client, userdata, msg):
    print(f"Message reÃ§u sur {msg.topic}, taille : {len(msg.payload)}")

    try:
        data = json.loads(msg.payload.decode("utf-8"))
        battery_level = data.get("battery", "Inconnu")
        b64_image = data.get("image")

        if not b64_image:
            print("Pas d'image dans le message !")
            return

        image_bytes = base64.b64decode(b64_image)
        image_stream = io.BytesIO(image_bytes)
        image = Image.open(image_stream)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        image_filename = f"image_{timestamp}.jpg"
        image_path = os.path.join(image_folder, image_filename)


        image.save(image_path)
        print(f"Image sauvegardÃ©e : {image_path}")


        battery_file = os.path.join(image_folder, f"{image_filename}.txt")
        with open(battery_file, "w") as bf:
            bf.write(str(battery_level))

        print(f"Niveau de batterie associÃ© : {battery_level}%")

    except Exception as e:
        print(f"Erreur traitement message : {e}")


def on_connect(client, userdata, flags, rc):
    global connected_once
    
    if rc == 0:
        if not connected_once:
            print("ConnectÃ© au broker MQTT")
            connected_once = True
        client.subscribe(mqtt_topic)

    else:
        print("Erreur connexion MQTT:", rc)


client = mqtt.Client("image_receiver")
client.on_connect = on_connect
client.on_message = on_message


print("Connexion MQTT...")
client.connect(mqtt_broker, mqtt_port)
client.loop_start()


@app.route("/")

def index():

    images = sorted([img for img in os.listdir(image_folder) if img.endswith(".jpg")], reverse=True)
    image_battery_info = []
    
    for image in images:
        battery_file = os.path.join(image_folder, f"{image}.txt")
        battery_level = "Inconnu"

        if os.path.exists(battery_file):
            with open(battery_file, "r") as bf:
                battery_level = bf.read().strip()
                
        image_battery_info.append((image, battery_level))

    return render_template("index.html", image_battery_info=image_battery_info)


@app.route("/images/<filename>")

def get_image(filename):
    return send_from_directory(image_folder, filename)


if __name__ == "__main__":
    
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)

    except KeyboardInterrupt:
        print("DÃ©connexion MQTT")
        
        client.loop_stop()
        client.disconnect()


