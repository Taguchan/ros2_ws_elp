from setuptools import find_packages, setup

package_name = 'emotion_recognition'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='karin-22',
    maintainer_email='taguchan.karin@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [

            'camera_preview = emotion_recognition.camera_preview:main',
            'fer_preview = emotion_recognition.fer_preview:main',
    
        ],
    },
)
