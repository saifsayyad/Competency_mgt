"""
Competancy_mgt
==============
"""
from setuptools import setup, find_packages
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('competancy_mgt/version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='competancy_mgt',
    version=version,
    url='http://competancy_mgt.readthedocs.org',
    license='MIT license',
    author='Saifali Saiyyad',
    author_email='saifalis@kpit.com',
    description="A web based application for managing competancy of each infividual.",
    long_description=__doc__,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    platforms='any',
    setup_requires=[],
    tests_require=[],
    install_requires=['groundwork', 'flask'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': ["competancy_mgt = "
                            "competancy_mgt.applications.competancy_mgt_app:start_app"],
        'groundwork.plugin': ["CompetancyMgtWebPlugin = "
                              "competancy_mgt.plugins.competancy_mgt_web_plugin.competancy_mgt_web_plugin:"
                              "CompetencyMgtWebPlugin"],
    }
)
