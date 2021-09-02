from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content if 'git+' not in x]

setup(
    name='photosorganisation',
    version="1.0.3.0",
    description=(
                "This python Package helps you sort and organize photos."
                "Duplicates,Memes,Screenshots and Blurry Photos are identifed."
                "Photos are tagged and classified for Geo-Location, Selfies,Animals etc."
    ),
    packages=find_packages(),
    install_requires=requirements,
    test_suite='tests',
    #include_package_data: to install data from MANIFEST.in
    include_package_data=True,
    scripts=[
        'scripts/photosorganisation-run'
    ],
    zip_safe=False)
