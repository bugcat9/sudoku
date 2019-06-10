'''
Created on 2019年5月6日

@author: zhouning
'''
from distutils.core import setup
import py2exe
import sys

py2exe_options = {
    "includes": ["sip"],
    "dll_excludes": ["MSVCP90.dll",],
    "compressed": 1,
    "optimize": 2,
    "ascii": 0,
    "bundle_files": 1,
    }

setup(
  name = '第一个PyQt5程序',
  version = '1.0',
  windows = ['DLXWindow.py'],
  zipfile = None,
  options = {'py2exe': py2exe_options}
  )