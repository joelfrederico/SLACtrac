import unittest


class slactrac_element_base(object):
    def name_test(self):
        self.assertEqual(self.element.name, self._name)

    def order_test(self):
        self.assertEqual(self.element.order, self._order)
