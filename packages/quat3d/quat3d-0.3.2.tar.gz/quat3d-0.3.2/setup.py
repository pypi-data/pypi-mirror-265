from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    
setup(
    name='quat3d',
    version='0.3.2',
    description='This is an IMU quaternion data visualization tool for xkit.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='chanmin.park',
    author_email='devcamp@gmail.com',
    url='https://github.com/planxstudio/xkit',
    install_requires=['click', 'python-dotenv', 'pyside6', 'pyqtgraph', 'pyopengl', 'pyopengl_accelerate', 'numpy-stl', 'genlib'],
    packages=find_packages(exclude=[]),
    keywords=['xkit', 'genlib'],
    python_requires='>=3.11',
    package_data={},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'quat3d = quat3d.quat3d:main',            
        ],
    },
)
