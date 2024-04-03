from setuptools import setup, find_packages

pkj_name = 'likes'

with open('requirements.txt') as f:
    requires = f.read().splitlines()


setup(
    name='django-ok-likes-latest',
    version='0.8.0',
    description='Django likes app latest',
    long_description='file: README.rst',
    author='Abhishek Khanduri',
    author_email='khanduriabhishek012@gmail.com',
    url='https://github.com/ColoredCow/ok-likes',
    packages=[pkj_name] + [pkj_name + '.' + x for x in find_packages(pkj_name)],
    include_package_data=True,
    license='MIT',
    install_requires=requires,
    classifiers=[
        'Environment :: Web Environment',
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django :: 5.0",
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3.10",
    ]

)
