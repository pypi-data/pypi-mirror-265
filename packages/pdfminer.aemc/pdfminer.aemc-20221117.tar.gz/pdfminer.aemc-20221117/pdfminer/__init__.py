import sys
import warnings


__version__ = '20221117'

if sys.version_info < (3, 8):
    warnings.warn('Please upgrade to Python 3.8 or newer.')

if __name__ == '__main__':
    print(__version__)
