from setuptools import setup, find_packages

with open('LICENSE', 'rt', encoding='utf8') as lic, open('package_description.rst', 'rt', encoding='utf8') as readme, \
        open('requirements.txt', 'rt', encoding='utf8') as required_packages:
    setup(
        name='ball_game',
        maintainer='Sergey Yakimov',
        maintainer_email='sergwy@gmail.com',
        version='0.2.0',
        url='https://gitlab.com/sergwy/ball_game',
        description='Ball Game',
        long_description_content_type='text/x-rst',
        long_description=readme.read(),
        packages=find_packages(),
        license=lic.read(),
        install_requires=[req for req in required_packages],
        python_requires='>=3.8'
    )
