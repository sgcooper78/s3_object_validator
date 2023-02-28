import unittest
import src.cli.s3_object_validator_cli

class TestDivideByThree(unittest.TestCase):

	def test_divide_by_three(self):
		self.assertEqual(divide_by_three(12), 4)

unittest.main()