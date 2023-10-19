import unittest
import Wikipart1

class testWikipart1(unittest.TestCase):
    def setUp(self):
        self.response =Wikipart1.returnWikiAPI("https://en.wikipedia.org/w/api.php", "Canada")
        self.data = self.response.json()
        self.pages = self.data["query"]["pages"]
    
    
    def test_NoArticleExist(self):
        
        Wikipart1.checkExistanceWiki(self.pages)

    def test_NetworkError(self):
        Wikipart1.checkResponseStatus(200)

    def test_ValidEntry(self):
        Wikipart1.checkForValidEntry("Ball state")
    
    def test_redirectStatus(self):
        result = Wikipart1.checkRedirectStatus(self.data)
        self.assertEquals(1,result)
        
        
    
if __name__ == '__main__':
    unittest.main()