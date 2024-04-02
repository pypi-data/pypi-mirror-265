from setuptools import setup, find_packages

setup(
    name='radosdb',
    version='0.1.2',
    packages=find_packages(),
    url='https://gitlab.techfin.ai/yangzhanwen/ceph_mod/-/tree/main/radosdb',
    license='MIT',
    author='yangzhanwen',
    author_email='1163630331@qq.com',
    install_requires=['numpy', 'pandas', 'pymongo', 'pytz'],
    entry_points={
        'console_scripts': [
            '__init__ = radosdb.transfer_dpmt:main',
        ]
    }
)