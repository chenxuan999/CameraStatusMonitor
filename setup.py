from setuptools import setup, find_packages

setup(
    name='camera-status-monitor',
    version='0.1.0',
    description='A simple tool to monitor camera status',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/camera-status-monitor',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pillow',
        'pyinstaller',
        'tk',
        'pygetwindow',
        'pywinctl'
    ],
    entry_points={
        'console_scripts': [
            'camera-monitor=camera_monitor:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
