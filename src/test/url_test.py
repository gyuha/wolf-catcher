# 참고 : https://wikidocs.net/16107
import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from util.Config import Config

def custom_function(file_name):
    with open(file_name, 'rt') as f:
        return sum(1 for _ in f)

class ConfigTest(unittest.TestCase): 
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_config(self):
        config = Config()
        self.assertEqual(config.data["site"][0]["name"], "wfwf")


# unittest를 실행
if __name__ == '__main__':  
    unittest.main()