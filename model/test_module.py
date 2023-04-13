
import unittest
from train_evaluate import train_model

class TestModule(unittest.TestCase):

    def test_Module(self):
        
        # Act
        results = train_model()

        # Assert
        self.assertGreaterEqual(80, results["r2"])
        self.assertLessEqual(results["mape"], 30)
