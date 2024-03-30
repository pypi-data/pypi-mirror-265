from setuptools import setup

setup(
    name='pythlete',
    version='0.1.7',
    description='Python package for instantaneous decision making in sports',
    url='https://github.com/AbdullahKhurram30/Pythlete',
    author='Muhammad Abdullah Khan',
    author_email='abdullah.khurram@uni.minerva.edu',
    packages=['pythlete'],
    install_requires=['fastf1', 'ipython', 'matplotlib',
                      'numpy', 'pandas', 'scipy',
                      'seaborn']
)