from setuptools import setup, find_packages

setup(
    name='my_library_hospital_management',
    version='0.1',
    packages=find_packages(),
    description='Hospital Management',
    install_requires=['asgiref','Django','parse','Pillow','sqlparse','tzdata'],  # Add dependencies if any
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)

