from copy import deepcopy
from datetime import datetime
import json
import os
import sys
import numpy as np
import pandas as pd

from ddt import ddt, data, unpack
from unittest import TestCase, mock, skip


# store example data for unit and local testing
DIR_TESTS = os.path.dirname(__file__)
DIR_DATA = os.path.join(DIR_TESTS, 'data')
DIR_RESULTS = os.path.join(DIR_TESTS, 'results')