from setuptools import setup, find_packages

setup(
    name='massivetools',
    version='0.0.2',
    description='Useful packages to perform computer vision tasks',
    author='pythonzz0622',
    author_email='pythonzz0622@gmail.com',
    url='https://github.com/pythonzz0622',
    install_requires=['pytz', 'numpy', 'opencv-python', 'pymysql' ,'tqdm','pandas', 'pycocotools'],
    packages=find_packages(exclude=[]),
    keywords=['preprocessing', 'db', 'timer', 'logger', 'pypi'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
