  class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
      self.cases = ('string', 1.5)
      for case in self.cases:
        with self.subTest(x=case):
          self.assertRaises(TypeError, factorize, case)
    
    def test_negative(self):
      self.cases = (-1, -10, -100)
      for case in self.cases:
        with self.subTest(x=case):
          self.assertRaises(ValueError, factorize, case)
    
    def test_zero_and_one_cases(self):
      self.cases = (0, 1)
      for case in self.cases:
        with self.subTest(x=case):
          self.assertTupleEqual(factorize(case), (case,))
    
    def test_simple_numbers(self):
      self.cases = (3, 13, 29)
      for case in self.cases:
        with self.subTest(x=case):
          self.assertTupleEqual(factorize(case), (case,))
          
    def test_two_simple_multipliers(self):
      self.cases = (6, 26, 121)
      expected = ((2, 3), (2, 13), (11, 11))
      for i, case in enumerate(self.cases):
        with self.subTest(x=case):
          self.assertTupleEqual(factorize(case), expected[i])
    
    def test_many_multipliers(self):
      self.cases = (1001, 9699690)
      expected = ((7, 11, 13), (2, 3, 5, 7, 11, 13, 17, 19))
      for i, case in enumerate(self.cases):
        with self.subTest(x=case):
          self.assertTupleEqual(factorize(case), expected[i])
