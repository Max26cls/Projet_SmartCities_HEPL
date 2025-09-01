Voici un projet réalisé dans le cadre d'un projet scolaire.

Ce projet a pour objectif de créer un nicoir connecté à l'aide d'un raspberry et d'un esp32-cam et de rendre celui-ci autonome.
Voici donc les différents codes réaliser et mis en place pour le bon fonctionnement du projet.

Le code "envoi_image.py" est le code devant se trouver en main() sur l'esp32-cam.

Les codes "reception_image.py" et "index.html" doivent sur trouver dans le même dossier sur le raspberry.
Un mqtt doit évidemment être lancé sur le raspberry et les lignes de code concernant ce mqtt doivent être modifié en fonction du mqtt créé (Topic, user, ip,...)


Voici les différentes choses à améliorer dans ce projet : 

- Partie de la simulation de la batterie, à modifier lorsque j'aurais la batterie pour récupérer la valeur de celle-ci

- Faire en sorte de vérifier le bonne connexion au mqtt de l'esp32-cam.
  
    -> Envoyer un message sur un topic lorsqu'il se connecte afin que le raspberry puisse voir qu'il est connecté.
  
    -> Durant l'envoie de l'image, faire en sorte que le raspberry envoi un callback par mqtt quand il reçoit l'image pour que l'esp32-cam sache qu'elle est bien arrivée (lecture de l'esp32-cam sur le mqtt aussi)
  
    -> Si pas reçu de callback au bout de x temps, renvoyer etc
  
- Modifier la partie du HTML car mal placé

----------------------------------------------English Version--------------------------------------------------------

This is a project carried out as part of a school project.

The aim of this project is to create a connected nicoir using a Raspberry Pi and an ESP32-Cam and to make it autonomous.
Here are the different codes created and implemented to ensure the project works properly.

The code ‘envoi_image.py’ is the code that must be located in main() on the ESP32-Cam.

The codes ‘reception_image.py’ and ‘index.html’ must be located in the same folder on the Raspberry Pi.
An MQTT must obviously be launched on the Raspberry Pi and the lines of code concerning this MQTT must be modified according to the MQTT created (Topic, user, IP, etc.).


Here are the various things to improve in this project: 

- Part of the battery simulation, to be modified when I have the battery to retrieve its value.

- Ensure that the esp32-cam is properly connected to the MQTT.
  
    -> Send a message on a topic when it connects so that the Raspberry Pi can see that it is connected.
  
    -> While sending the image, ensure that the Raspberry Pi sends a callback via MQTT when it receives the image so that the ESP32-Cam knows that it has arrived (read the ESP32-Cam on the MQTT as well).
  
    -> If no callback is received after x amount of time, resend, etc.
  
- Modify the HTML section as it is incorrectly placed.
