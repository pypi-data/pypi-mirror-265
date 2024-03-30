from setuptools import setup, find_packages

setup(
    name='cpphospitalmanagementproject',
    version='0.0.2',
    packages=find_packages(),
    description='Hospital Management',
    install_requires=['asgiref','Django','parse','Pillow','sqlparse','tzdata'],  # Add dependencies if any
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)

