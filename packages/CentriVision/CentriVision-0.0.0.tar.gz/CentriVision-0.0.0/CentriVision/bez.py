# -*- encoding: utf-8 -*-
'''
@File        :bez.py
@Time        :2021/09/28 11:26:28
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :None
'''

import configparser
import os
import re
import math
from math import *
import numpy as np
import pandas as pd
import CentriVision
from Bio import Seq, SeqIO, SeqRecord
import codecs
from tqdm import trange
import gc
import matplotlib.pyplot as plt
from matplotlib.patches import *
from matplotlib.patches import Circle, Ellipse
from pylab import *
from collections import Counter

def config():
    conf = configparser.ConfigParser()
    conf.read(os.path.join(CentriVision.__path__[0], 'conf.ini'))
    return conf.items('ini')

def load_conf(file, section):
    conf = configparser.ConfigParser()
    conf.read(file)
    return conf.items(section)



