> Consultez d'abord le [read_me_demo](https://gitlab.univ-lille.fr/projet-sos/read_me_demo) si ce n'est pas déjà fait.

Clonez le projet
```sh
git clone git@gitlab-ssh.univ-lille.fr:projet-sos/demo_deux_robots/deux_robots_ws.git
# OU
git clone https://gitlab.univ-lille.fr/projet-sos/demo_deux_robots/deux_robots_ws.git
```

# Démonstration ROS 2 deux robots

Ce projet inclut un workspace ROS 2 qui contient trois démonstrations montrant de la communication entre deux robots :
- `mimic` : Le robot choisit un nombre n, il fait n aller-retour, puis il demande au second robot de faire le même nombre d'aller-retour.
- `qr_code` : Le premier robot est immobile et scanne des QR Code donnant des ordres (aller-retour, cercle, stop). Le deuxième robot exécute les ordres.
- `rendez_vous` : Le premier robot rejoint le deuxième robot en se basant sur sa position.

[Cette vidéo](https://nextcloud.univ-lille.fr/index.php/s/FDwxDeRFDH2BdtZ) illustre ces différents comportements.

# Lancer le projet sur les robots

Le dossier `ansible` contient tous les scripts qui permettent de transférer et exécuter le projet sur les robots. [Lire le README.md du dossier](./ansible/README.md).

# Simulation Gazebo

Pour ouvrir la simulation Gazebo:
```
cd deux_robots_ws
rosdep install --from-paths src -y --ignore-src
colcon build
source ./install/setup.bash
ros2 launch deux_tb3_sim empty_world.launch.py
```

Le programme fait apparaître une fenêtre gazebo avec deux robots `tb3_1` et `tb3_2`. Vous devrez avoir ces topics:
```
/tb3_1/cmd_vel
/tb3_1/imu
/tb3_1/joint_states
/tb3_1/odom
/tb3_1/robot_description
/tb3_1/scan
/tb3_1/tf
/tb3_1/tf_static

/tb3_2/cmd_vel
/tb3_2/imu
/tb3_2/joint_states
/tb3_2/odom
/tb3_2/robot_description
/tb3_2/scan
/tb3_2/tf
/tb3_2/tf_static
```

Dans un autre terminal, vous pouvez lancer le programme `mimic`:
```
source deux_robots_ws/install/setup.bash
ros2 launch mimic robots.launch.py
```