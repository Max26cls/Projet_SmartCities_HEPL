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
