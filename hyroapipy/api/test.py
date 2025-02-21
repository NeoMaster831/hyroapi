"""
test.py - Test the IOCTL session
"""

from hyroapipy.fixed import *
from hyroapipy.ioctlw import IOCTLSession
import logging

class TestSession:
    def __init__(self, ioctl: IOCTLSession = None):
        """
        @brief Initialize a test session
        @param ioctl The IOCTLSession object
        """
        self.ioctl = IOCTLSession() if ioctl is None else ioctl

    def Test(self):
        """
        @brief Test the IOCTL session
        """
        returnValue = self.ioctl.Request(IOCTL_HYROAPI_TEST, NULL, 4)
        returnValue = int.from_bytes(returnValue, "little")
        
        assert(returnValue == 0x1)

        logging.info("Test successful")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    session = TestSession()
    session.Test()
    print("Session opened successfully")