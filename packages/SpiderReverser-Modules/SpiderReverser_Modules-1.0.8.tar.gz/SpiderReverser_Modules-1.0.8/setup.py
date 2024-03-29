from setuptools import setup, find_packages

# install_requires rely on requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

requirements = list(map(lambda x: x.split("==")[0], requirements))

print(requirements)

setup(
    name='SpiderReverser_Modules',
    version='1.0.8',
    packages=find_packages(),
    install_requires=requirements,
    author="SpiderReverser",
    author_email="spiderreverser@foxmail.com",
    description="SpiderReverser person modules",
    url="https://github.com/SpiderReverser/SpiderReverser_Modules",
)
