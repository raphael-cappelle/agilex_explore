Ce projet Ansible permet de copier et lancer un projet ROS 2 pour trois scénarios impliquant deux robots. Si vous avez des problèmes lors du lancement d'une démonstration, consultez le fichier [ansible.md](https://gitlab.univ-lille.fr/projet-sos/read_me_demo/-/blob/master/ansible.md) du `read_me_demo`.

Avant de commencer, assurez-vous d'être dans le dossier `ansible` du projet. Toutes les commandes doivent être exécutées dans ce répertoire de votre ordinateur. Aucune commande n'est à exécuter sur les robots (c'est l'avantage d'Ansible).

# Lister les robots utilisés

Modifiez le fichier `hosts` pour inclure la liste des robots. Spécifiez également la commande pour lancer le driver ROS des robots et indiquez dans quel workspace se trouve ce driver. Pour ce projet, les robots sont nommés `tb3_1` et `tb3_2`; ne changez pas ces noms.

# Vérifier que les robots sont connectés

Utilisez le script Python `check_connection` pour vérifier si tous les robots sont connectés au réseau :

```sh
python3 check_connection.py
```

Ce script est particulièrement utile lorsque vous avez une flotte de robots et que vous devez attendre qu'ils soient tous allumés.

# Téléverser le workspace ROS 2

Avant de copier le workspace, synchronisez l'horloge des robots. Vous pouvez le faire en configurant un serveur NTP sur votre machine ou en exécutant la commande ci-dessous (à faire à chaque démarrage des robots). **Si la commande ne fonctionne pas sur un robot, connectez-vous sur ce robot en SSH pour confirmer l'empreinte de clé publique du robot.**
```sh
ansible-playbook sync_date.yaml
```

Pour copier et compiler le workspace sur les robots, utilisez :
```sh
ansible-playbook copy_ws.yaml
```

Si les robots doivent installer des dépendances, assurez-vous qu'ils aient accès à internet. Si vous avez créé un point d'accès sur votre machine, utilisez `sudo ufw disable` pour désactiver le pare-feu.

Par défaut, la commande copie le dossier `~/deux_robots_ws` vers `~/deux_robots_ws`. Vous pouvez modifier cela avec les paramètres `ws_src` et `ws_dst` :
```sh
ansible-playbook copy_ws.yaml -e "ws_src=~/nathan_ws" -e "ws_dst=~/nathan_ws"
```

Pour éviter de tout recompiler à chaque téléversement, les dossiers `install`, `build` et `log` sont conservés. Si vous rencontrez des problèmes lors de la compilation, ajoutez l'argument `clean_install` pour supprimer ces dossiers avant de compiler (ce sera plus long) :
```sh
ansible-playbook copy_ws.yaml -e "clean_install=true"
``` 

# Démarrer un programme ROS 2

Une fois le workspace copié et compilé, lancez le programme sur les robots.

## Programme "mimic"

Le robot `tb3_1` choisit un nombre n et effectue n allers-retours. Une fois terminé, `tb3_2` effectue le même nombre d'allers-retours.

Placez les deux robots au sol, orientés vers la même direction en vous assurant qu'il n'y a pas d'obstacle devant eux. Pour lancer le programme, faites cette commande :
```sh
ansible-playbook start.yaml -e "app=mimic"
```

## Programme "qr_code"

`tb3_1` scanne des QR codes donnant des ordres, que `tb3_2` exécute. Les différents QR codes se trouvent dans le dossier `qr_codes` du workspace.

Placez les deux robots au sol, `tb3_1` restera immobile. Assurez-vous que `tb3_2` ait l'espace suffisant pour pouvoir faire des aller-retour et faire un cercle. Ensuite, exécutez cette commande :
```sh
ansible-playbook start.yaml -e "app=qr_code"
```

## Programme "rendez_vous"

Nous allons utiliser le système de caméra OptiTrack pour récupérer la position des robots. Regardez le fichier [optitrack.md](https://gitlab.univ-lille.fr/projet-sos/read_me_demo/-/blob/master/optitrack.md) pour ajouter les deux robots et créer le topic pour récupérer leur position. Assurez-vous bien que les robots sont orientés vers les grandes fenêtres extérieures quand vous créez les rigid bodies. Chaque nom de rigid body doit correspondre à `tb3_1` et `tb3_2`.

Un robot rejoint l'autre grâce à la position fournie par les caméras OptiTrack.
```sh
ansible-playbook start.yaml -e "app=rendez_vous"
```
Pour ce programme, envoyez une action ROS 2 pour qu'un robot rejoigne l'autre :
```sh
cd ~/deux_robots_ws
rosdep install --from-paths src -y --ignore-src
colcon build
source ./install/setup.bash
# `tb3_1` rejoint `tb3_2`
ros2 action send_goal /tb3_1/go_to_point rendez_vous_interfaces/action/GoToPoint "distance_tolerance: 0.4"
# `tb3_2` rejoint `tb3_1`
ros2 action send_goal /tb3_2/go_to_point rendez_vous_interfaces/action/GoToPoint "distance_tolerance: 0.4"
```

# Arrêter un programme

La commande suivante va arrêter le programme sur tous les robots. Le lidar devrait arrêter de tourner.
```sh
ansible-playbook stop.yaml
```