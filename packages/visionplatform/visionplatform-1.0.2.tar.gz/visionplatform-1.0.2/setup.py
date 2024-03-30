from setuptools import setup

setup(
    name='visionplatform',
    version='1.0.2',
    packages=['visionplatform'],
    entry_points={
        'console_scripts': [
            'visionplatform=visionplatform.install_visionplatform:install',
        ],
    },
)
