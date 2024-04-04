import unittest

from utils import (AI, TTS, WWW, Console, Git, Image, LatLng, Translator,
                   Tweet, _, Log, Hash, Parallel, XMLElement)


class TestCase(unittest.TestCase):
    def test_init(self):
        for x in [
            AI, TTS, WWW, Console, Git, Image, LatLng, Translator,
                   Tweet, _, Log, Hash, Parallel, XMLElement
        ]:
            self.assertIsNotNone(x)
