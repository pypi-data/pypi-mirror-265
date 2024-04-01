# -*- encoding: utf-8 -*-
'''
@File        :run.py
@Time        :2021/09/28 09:04:51
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :主程序
'''


import argparse
import os
import sys
import configparser
import pandas as pd
import CentriVision
import CentriVision.bez as bez


from CentriVision.getPASA import getPASA
from CentriVision.getNCBI import getNCBI



parser = argparse.ArgumentParser(
    prog = 'CentriVision', usage = '%(prog)s [options]', epilog = "", formatter_class = argparse.RawDescriptionHelpFormatter,)
parser.description = '''\
runing CentriVision
    -------------------------------------- '''
parser.add_argument("-v", "--version", action = 'version', version='0.0.0')



parser.add_argument("-getpasa", dest = "getPASA",
                    help = "get_PASA")
parser.add_argument("-getncbi", dest = "getNCBI",
                    help = "get_NCBI")

args = parser.parse_args()



def run_getPASA():
    options = bez.load_conf(args.getPASA, 'getPASA')
    getPASA1 = getPASA(options)
    getPASA1.run()

def run_getNCBI():
    options = bez.load_conf(args.getNCBI, 'getNCBI')
    getNCBI1 = getNCBI(options)
    getNCBI1.run()


def module_to_run(argument):
    switcher = {


        'getPASA': run_getPASA,
        'getNCBI': run_getNCBI,


    }
    return switcher.get(argument)()

def main():
    path = CentriVision.__path__[0]
    options = {

               'getPASA': 'getPASA.conf',
               'getNCBI': 'getNCBI.conf',

               }
    for arg in vars(args):
        value = getattr(args, arg)
        # print(value)
        if value is not None:
            if value in ['?', 'help', 'example']:
                f = open(os.path.join(path, 'example', options[arg]))
                print(f.read())
            elif value == 'e':
                out = '''\
        File example
        [fpchrolen]
        chromosomes number_of_bases
        *   *
        *   *
        *   *
        [fpgff]
        chromosomes gene    start   end
        *   *   *   *
        *   *   *   *
        *   *   *   *
        [fpgenefamilyinf]
        gene1   gene2   Ka  Ks
        *   *   *   *
        *   *   *   *
        *   *   *   *
        [alphagenepairs]
        gene1   gene2
        *   *   *
        *   *   *
        *   *   *

        The file columns are separated by Tab
        -----------------------------------------------------------    '''
                print(out)
            elif not os.path.exists(value):
                print(value+' not exits')
                sys.exit(0)
            else:
                module_to_run(arg)

