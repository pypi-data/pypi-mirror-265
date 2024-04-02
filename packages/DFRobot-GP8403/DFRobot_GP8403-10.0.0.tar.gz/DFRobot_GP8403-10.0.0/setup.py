import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DFRobot_GP8403",
    keywords = 'Raspberry Pi, Raspi, Python, GPIO, GP8403, DAC',
    version="10.0.0",
    author="Joel Klein",
    description="DFRobot_GP8403 is now GP8XXX_IIC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joe2824/DFRobot_GP8403",
    classifiers=["Development Status :: 7 - Inactive"],
    packages=['DFRobot'],
    python_requires=">=3",
    install_requires=[
          'smbus2'
      ]
)
