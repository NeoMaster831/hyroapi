"""
ioctlw.py - IOCTL wrapper for Hyro APi
"""

import ctypes
from ctypes import wintypes
import logging

kernel32 = ctypes.WinDLL("kernel32.dll")

def IoctlCtlCode(DeviceType, Function, Method, Access):
    return (DeviceType << 16) | (Access << 14) | (Function << 2) | Method

from hyroapipy.fixed import *

class IOCTLSession:
    def __init__(self) -> None:
        self.device = kernel32.CreateFileW(
            "\\\\.\\HyroAPIW",
            0xC0000000,  # GENERIC_READ | GENERIC_WRITE
            0,
            None,  # NULL -> None
            3,  # OPEN_EXISTING
            0x80,  # FILE_ATTRIBUTE_NORMAL
            None  # NULL -> None
        )
        if self.device == -1:
            error_code = kernel32.GetLastError()
            raise Exception(f"Failed to open device, error code: {error_code}")
        logging.debug(f"Device opened successfully, handle: {self.device}")
    
    def Request(self, ioctl_code, input_buffer: bytes, output_buffer_size: int) -> bytes:
        """
        @brief Request an IOCTL operation
        @param ioctl_code The IOCTL code
        @param input_buffer The input buffer. if there's no input buffer, pass `NULL`.
        @param output_buffer_size The size of the output buffer. if there's no output buffer, pass 0.
        @return A tuple of (success, response)
        """    
        if output_buffer_size == 0:
            output_buffer = 0
        else:
            output_buffer = (ctypes.c_uint8 * output_buffer_size)()
        
        bytes_returned = wintypes.DWORD(0)

        input_buffer_size = len(input_buffer)
        if len(input_buffer) == 0: # Maybe NULL in fixed.py
            input_buffer = 0 # NULL
            input_buffer_size = 0

        success = kernel32.DeviceIoControl(
            self.device,
            ioctl_code,
            input_buffer,
            input_buffer_size,
            output_buffer,
            output_buffer_size,
            ctypes.byref(bytes_returned),
            None  # lpOverlapped -> None
        )

        if not success:
            error_code = kernel32.GetLastError()
            raise Exception(f"Request failed, error code: {error_code}")
        
        if bytes_returned.value == 0:
            logging.debug("Request successful, but no data returned")
            return None
        else:
            return bytes(output_buffer[:bytes_returned.value])

    def __del__(self) -> None:
        if hasattr(self, 'device') and self.device != -1:
            kernel32.CloseHandle(self.device)
            logging.debug("Device closed")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    session = IOCTLSession()
    k = session.Request(IOCTL_HYROAPI_TEST, NULL, 0x4)
    print(k)
    print("Session opened successfully")