from unittest import TestCase
from messageDecode import MessageDecode
import time
import unittest

__author__ = 'Ramki Subramanian'

inputstring = "Hi @Ramki how are you (smiles)http://www.cubrid.org/blog/dev-platform/understanding-jvm-internals/"
messageTime = time.ctime()

class TestMessageDecode(TestCase):

    def setUp(self):
        self.inputstring = inputstring
        self.messageTime = messageTime

    def test_removeduplicates(self):
        self.fail()

    def test_decode(self):

        retruned_json = MessageDecode()
        expected_json = {
                            "emoticons": [
                                "smiles"
                            ],
                            "links": [
                                {
                                    "id": 0,
                                    "title": "Understanding JVM Internals | CUBRID Blog",
                                    "url": "http://www.cubrid.org/blog/dev-platform/understanding-jvm-internals/"
                                }
                            ],
                            "mentions": [
                                "Ramki"
                            ],
                            "message_time": "Mon Mar 09 04:16:51 2015"
                        }

        self.assertEquals("Both expected and actual results are same",expected_json,retruned_json)

if __name__ == '__main__':
    unittest.main()