import unittest
import numpy as np
import types

def kwarg_gen(arg, arg_val, testname):
    def test_fun(self):
        element = getattr(self, testname)
        element_arg_val = getattr(element, arg)
        self.assertEqual(element_arg_val, arg_val)

    return test_fun


def basic_setup(self, testname='element', **kwargs):
    for arg in kwargs:
        arg_val = kwargs[arg]
        setattr(self, '_{}'.format(arg), arg_val)
        # test_fun = kwarg_gen(arg, arg_val)
        test_name = '{}_test'.format(arg)
        test = kwarg_gen(arg, arg_val, testname=testname)
        setattr(self, test_name, test)
        setattr(getattr(self, test_name), '__name__', test_name)

def array_tol(meas, ref, tol):
    return np.all(meas - ref < tol)


def change_E(self, old_gamma, new_gamma):
    self.element.change_E(old_gamma, new_gamma)
    return self
