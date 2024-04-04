# distutils: language=c++
import numpy as np
cimport numpy as np
from libcpp cimport bool
import sys

cimport init_wrapper

assert sizeof(int) == sizeof(np.int32_t)