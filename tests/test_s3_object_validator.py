import unittest
import s3_object_validator as validator

class TestDivideByThree(unittest.TestCase):

	def test_s3_object_validator(self):
		self.assertEqual(validator.sanitizeStructure('Probablynotapath'), )

unittest.main()