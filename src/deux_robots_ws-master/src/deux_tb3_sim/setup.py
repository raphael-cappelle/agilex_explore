from itertools import chain
import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'deux_tb3_sim'

data_files = [
    (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
]

def generate_data_files(data_files):
    data_dirs = ('urdf', 'worlds', 'models')
    for path, _, files in chain.from_iterable(os.walk(data_dir) for data_dir in data_dirs):
        install_dir = os.path.join('share', package_name, path)    
        list_entry = (install_dir, [os.path.join(path, f) for f in files if not f.startswith('.')])
        data_files.append(list_entry)
    return data_files

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=generate_data_files(data_files),
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hallez',
    maintainer_email='nathan.hallez.etu@univ-lille.fr',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'spawn_robots = deux_tb3_sim.spawn_robots:main',
        ],
    },
)
