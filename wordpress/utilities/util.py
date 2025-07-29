# utilities/util.py
import time
import traceback
import random, string
from utilities.custom_logger import customLogger

class Util:
    log = customLogger("util")

    def sleep(self, sec, info=""):
        if info:
            self.log.info("Wait %.2f s for %s", sec, info)
        try:
            time.sleep(sec)
        except InterruptedError:
            traceback.print_stack()

    def getAlphaNumeric(self, length, type='letters'):
        case = {
            'lower': string.ascii_lowercase,
            'upper': string.ascii_uppercase,
            'digits': string.digits,
            'mix': string.ascii_letters + string.digits,
            'letters': string.ascii_letters
        }.get(type, string.ascii_letters)
        return ''.join(random.choice(case) for _ in range(length))

    def getUniqueName(self, charCount=10):
        return self.getAlphaNumeric(charCount, 'lower')

    def verifyTextContains(self, actualText, expectedText):
        self.log.info("Actual → %s", actualText)
        self.log.info("Expect ⊂ %s", expectedText)
        return expectedText.lower() in (actualText or "").lower()

    def verifyTextMatch(self, actualText, expectedText):
        self.log.info("Actual → %s", actualText)
        self.log.info("Expect = %s", expectedText)
        return (actualText or "").strip().lower() == (expectedText or "").strip().lower()

    def verifyListMatch(self, expectedList, actualList):
        return set(expectedList) == set(actualList)

    def verifyListContains(self, expectedList, actualList):
        return all(item in actualList for item in expectedList)
