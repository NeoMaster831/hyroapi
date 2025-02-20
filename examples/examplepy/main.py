from hyroapipy.ioctlw import *

session = IOCTLSession()
response = session.Request(IOCTL_HYROAPI_TEST, NULL, 4)

print(response)