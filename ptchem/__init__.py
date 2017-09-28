'''
The internal code for Computational Chemistry
 - originally written by: Thien-Phuc Tu-Nguyen
 - current version: 0.2
 - last update: September 2017
 - by: Thien-Phuc Tu-Nguyen
 - tested on: Anaconda3 4.4
All right reserved
'''
from .gaussian import Gaussian09
from .mopac import Mopac2016
from .raspa import Raspa2
from .collector import Collector

__version__ = '0.2'
