import preprocessing as prep
import unittest

class TestPreprocessing(unittest.TestCase):

    def test_cleanPunctuation(self):
        self.assertEqual(prep.cleanPunctuation("Hi!@#$%:^Hi"),"HiHi")

    def test_stemming(self):
        self.assertEqual(prep.stemming("playing running sleeping"),"play run sleep")

    def test_Lemma(self):
        self.assertEqual(prep.Lemmatization("The children are playing"),"The child are playing")

    def test_cleanSW(self):
        self.assertEqual(prep.cleanSW("This is an apple"),['This','apple'])

    def test_correctSpelling(self):
        self.assertEqual(prep.correctSpelling(['applle']),"apple")

    def test_cleanPunctuationAndLower(self):
        self.assertEqual(prep.cleanPunctuationAndLower("HI!@##@$#%?HI"),"hihi")

    def test_stemmingAndLemma(self):
        self.assertEqual(prep.StemmingAndLemmatization("the children are playing"),"the child are play")

    def test_cleanSWANDSpelling(self):
        self.assertEqual(prep.cleanStopWordsAndSpelling("i am a studet"),"student")


if __name__=='__main__':
    unittest.main()