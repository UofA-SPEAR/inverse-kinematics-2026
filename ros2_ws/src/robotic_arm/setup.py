from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'robotic_arm'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Install launch files
        (os.path.join('share', package_name, 'launch'), 
         glob(os.path.join('launch', '*'))),

        (os.path.join('share', package_name, 'urdf'), 
         glob(os.path.join('urdf', '*'))),

        (os.path.join('share', package_name, 'config'),
         glob(os.path.join('config', '*'))),

         (os.path.join('share', package_name, 'meshes'),
         glob(os.path.join('meshes', '*'))),

         (os.path.join('share', package_name, 'worlds'),
         glob(os.path.join('worlds', '*'))),
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='adamyin',
    maintainer_email='adamyin3837@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
