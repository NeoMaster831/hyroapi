"""
general.py - General functions for Hyro API
"""

from hyroapipy.ioctlw import IOCTLSession
from hyroapipy.fixed import *
import logging
import ctypes
import enum

class KernelVarRequestType(enum.Enum):
    GUEST = 0
    HOST = 1

class KernelVar:
    """
    Class for managing kernel variables in non-paged pool memory
    """
    ioctl: IOCTLSession
    pool: int
    length: int

    def __init__(self, length: int = None, value: bytes = None, at: int = None, ioctl: IOCTLSession = None):
        """
        @brief Initialize a kernel variable (Non-Paged Pool)
        @param length Size of the kernel variable
        @param value The initial value of the kernel variable
        @param at Pointer to KernelVar Virtual Address
        @param ioctl The IOCTLSession object for driver communication
        """
        self.ioctl = IOCTLSession() if ioctl is None else ioctl

        if at is not None:
            assert(length is not None)
            self.pool = at
            self.length = length
            self._Sync()
            return

        if length is None:
            length = len(value)

        self.length = length
        length_bytes = length.to_bytes(8, "little")
        pool = self.ioctl.Request(IOCTL_HYROAPI_GENERAL_ALLOC_NONPAGED_BUFFER, length_bytes, 8)
        self.pool = int.from_bytes(pool, "little")

        if value is None:
            value = b"\x00" * length
        
        self.Set(value)

    def Virt(self) -> int:
        """
        @brief Get the virtual address of the kernel variable
        @return The virtual address of allocated memory
        """
        return self.pool

    def Phys(self) -> int:
        """
        @brief Get the physical address of the kernel variable
        @return The physical address of allocated memory
        """
        phys = self.ioctl.Request(
            IOCTL_HYROAPI_GENERAL_GET_PHYSICAL_ADDRESS, 
            self.pool.to_bytes(8, "little"), 
            8
        )
        return int.from_bytes(phys, "little")
    
    def Get(self, mode: KernelVarRequestType = KernelVarRequestType.GUEST) -> bytes:
        """
        @brief Get the current value of the kernel variable
        @param mode The mode of operation (GUEST or HOST)
        @return The value stored in kernel memory
        """

        """
        typedef struct _APIW_COPY_NONPAGED_BUFFER_REQUEST {
            PVOID dest;
            PVOID src;
            SIZE_T size;
        } APIW_COPY_NONPAGED_BUFFER_REQUEST, *PAPIW_COPY_NONPAGED_BUFFER_REQUEST;
        """

        value_length = self.length.to_bytes(8, "little")

        # Create destination buffer and get its address
        dest = (ctypes.c_uint8 * self.length)(*[0 for _ in range(self.length)] )
        dest_pointer = bytes(ctypes.cast(dest, ctypes.POINTER(ctypes.c_uint8)))

        # Prepare source address and size
        src = self.pool.to_bytes(8, "little")
        
        # Build request buffer: dest + src + size
        request = dest_pointer + src + value_length
        
        if mode == KernelVarRequestType.HOST:
            self.ioctl.Request(IOCTL_HYROAPI_GENERAL_COPY_NONPAGED_BUFFER, request, 0)
        else:
            self.ioctl.Request(IOCTL_HYROAPI_GUEST_GENERAL_COPY_NONPAGED_BUFFER, request, 0)
        
        return bytes(dest)

    def Set(self, value: bytes, mode: KernelVarRequestType = KernelVarRequestType.GUEST) -> None:
        """
        @brief Set a new value for the kernel variable
        @param value The new value to store in kernel memory
        @param mode The mode of operation (GUEST or HOST)
        """

        """
        typedef struct _APIW_COPY_NONPAGED_BUFFER_REQUEST {
            PVOID dest;
            PVOID src;
            SIZE_T size;
        } APIW_COPY_NONPAGED_BUFFER_REQUEST, *PAPIW_COPY_NONPAGED_BUFFER_REQUEST;
        """
        assert len(value) <= self.length

        if len(value) < self.length:
            value += b"\x00" * (self.length - len(value))

        value_length = len(value).to_bytes(8, "little")

        # Prepare destination address in kernel space
        dest = self.pool.to_bytes(8, "little")
        
        # Create source buffer and get its address
        src = (ctypes.c_uint8 * len(value))(*value)
        src_pointer = bytes(ctypes.cast(src, ctypes.POINTER(ctypes.c_uint8)))
        
        # Build request buffer: dest + src + size
        request = dest + src_pointer + value_length
        
        if mode == KernelVarRequestType.HOST:
            self.ioctl.Request(IOCTL_HYROAPI_GENERAL_COPY_NONPAGED_BUFFER, request, 0)
        else:
            self.ioctl.Request(IOCTL_HYROAPI_GUEST_GENERAL_COPY_NONPAGED_BUFFER, request, 0)

    def Execute(self, mode: KernelVarRequestType = KernelVarRequestType.GUEST) -> int:
        """
        @brief Execute the kernel variable as code
        @param mode The mode of execution (GUEST or HOST)
        @return Execution return value (-1 indicates potential failure)
        """

        """
        typedef struct _APIW_EXECUTE_NONPAGED_BUFFER_REQUEST {
            PVOID buffer;
            ULONG maxExecuteLength;
        } APIW_EXECUTE_NONPAGED_BUFFER_REQUEST, *PAPIW_EXECUTE_NONPAGED_BUFFER_REQUEST;
        """

        buffer = self.pool.to_bytes(8, "little")
        max_execute_length = self.length.to_bytes(4, "little")
        padding = b"\x00" * 4  # Align to 8 bytes

        if mode == KernelVarRequestType.HOST:
            return_value = self.ioctl.Request(
                IOCTL_HYROAPI_GENERAL_EXECUTE_NONPAGED_BUFFER, 
                buffer + max_execute_length + padding, 
                8
            )
        else:
            return_value = self.ioctl.Request(
                IOCTL_HYROAPI_GUEST_GENERAL_EXECUTE_NONPAGED_BUFFER, 
                buffer + max_execute_length + padding, 
                8
            )
        
        return_value = int.from_bytes(return_value, "little")
        
        if return_value == 0xFFFFFFFFFFFFFFFF:
            logging.warning("Execution failed maybe (return value is -1)")

        return return_value

    def __del__(self):
        """
        @brief Clean up kernel memory when object is destroyed
        """
        self.ioctl.Request(
            IOCTL_HYROAPI_GENERAL_FREE_NONPAGED_BUFFER, 
            self.pool.to_bytes(8, "little"), 
            0
        )

def NewKernelVar(value: bytes, ioctl: IOCTLSession = None):
    return KernelVar(value=value, ioctl=ioctl)

def AllocKernelVar(size: int, ioctl: IOCTLSession = None):
    return KernelVar(length=size, ioctl=ioctl)

def KernelVarAt(at: int, size: int, ioctl: IOCTLSession = None):
    return KernelVar(at=at, length=size, ioctl=ioctl)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    a = NewKernelVar(b"\x48\xC7\xC0\x45\x00\x00\x00\xC3")
    logging.info(a.Get())
    logging.info(a.Execute())

    b = KernelVarAt(a.Virt(), a.length)
    logging.info(b.Get())
    logging.info(b.Execute())