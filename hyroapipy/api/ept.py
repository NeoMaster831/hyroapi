"""
ept.py - EPT (Extended Page Table) functions for Hyro API
"""

from hyroapipy.fixed import *
from hyroapipy.api.general import AllocKernelVar, KernelVar
from hyroapipy.ioctlw import IOCTLSession
import logging

class EptHookSession:
    def __init__(self, ioctl: IOCTLSession = None):
        """
        @brief Initialize an EPT hook
        @param ioctl The IOCTLSession object
        """

        self.ioctl = IOCTLSession() if ioctl is None else ioctl
        self.hooks = {} # [physAddr] -> (hookCtx, enabled)

    def Add(self, physAddr: int):
        """
        @brief Add an EPT hook
        @param physAddr The physical address to hook
        """
        physAddr &= 0xFFFFFFFFFFFFF000 # Align to page boundary
        assert(physAddr not in self.hooks)

        physAddrBytes = physAddr.to_bytes(8, "little") # Convert to bytes
        returnValue = self.ioctl.Request(IOCTL_HYROAPI_EPT_ADD, physAddrBytes, SIZEOF_BOOL)
        returnValue = int.from_bytes(returnValue, "little")
        assert(returnValue != 0) # Check if the operation was successful

        self.hooks[physAddr] = [None, False]

        logging.debug(f"Hooked EPT at 0x{physAddr:016X}")
    
    def Remove(self, physAddr: int):
        """
        @brief Remove an EPT hook
        @param physAddr The physical address to unhook
        """
        physAddr &= 0xFFFFFFFFFFFFF000 # Align to page boundary
        assert(physAddr in self.hooks)

        physAddrBytes = physAddr.to_bytes(8, "little")
        self.ioctl.Request(IOCTL_HYROAPI_EPT_REMOVE, physAddrBytes, 0)
        self.hooks.pop(physAddr)

        logging.debug(f"Unhooked EPT at 0x{physAddr:016X}")

    def Enable(self, physAddr: int):
        """
        @brief Enable an EPT hook
        @param physAddr The physical address to enable
        """
        physAddr &= 0xFFFFFFFFFFFFF000 # Align to page boundary
        assert(physAddr in self.hooks and not self.hooks[physAddr][1])
        physAddrBytes = physAddr.to_bytes(8, "little")

        returnValue = self.ioctl.Request(IOCTL_HYROAPI_EPT_ENABLE, physAddrBytes, SIZEOF_BOOL)
        returnValue = int.from_bytes(returnValue, "little")
        assert(returnValue != 0)
        self.hooks[physAddr][1] = True

        logging.debug(f"Enabled EPT at 0x{physAddr:016X}")

    def Disable(self, physAddr: int):
        """
        @brief Disable an EPT hook
        @param physAddr The physical address to disable
        """
        physAddr &= 0xFFFFFFFFFFFFF000 # Align to page boundary
        assert(physAddr in self.hooks and self.hooks[physAddr][1])

        physAddrBytes = physAddr.to_bytes(8, "little")
        self.ioctl.Request(IOCTL_HYROAPI_EPT_DISABLE, physAddrBytes, 0)
        self.hooks[physAddr][1] = False

        logging.debug(f"Disabled EPT at 0x{physAddr:016X}")
    
    def Modify(self, physAddr: int, hookCtx: KernelVar):
        """
        @brief Modify an EPT hook
        @param physAddr The physical address to modify
        @param hookCtx The new hook context
        """

        physAddr &= 0xFFFFFFFFFFFFF000 # Align to page boundary
        assert(physAddr in self.hooks)
        assert(hookCtx.length == 0x1000) # PAGE_SIZE

        """
        typedef struct _APIW_EPT_MODIFY_REQUEST {
            UINT64 physicalAddr;
            PVOID hookCtx;
        } APIW_EPT_MODIFY_REQUEST, * PAPIW_EPT_MODIFY_REQUEST;
        """
        physAddrBytes = physAddr.to_bytes(8, "little")
        hookCtxBytes = hookCtx.pool.to_bytes(8, "little")
        request = physAddrBytes + hookCtxBytes

        returnVal = self.ioctl.Request(IOCTL_HYROAPI_EPT_MODIFY, request, SIZEOF_BOOL)
        returnVal = int.from_bytes(returnVal, "little")
        assert(returnVal != 0)

        self.hooks[physAddr][0] = hookCtx.Get()

        logging.debug(f"Modified EPT at 0x{physAddr:016X}")

    def Get(self, physAddr: int) -> tuple[bytes, bool]:
        """
        @brief Get the EPT hook context
        @param physAddr The physical address of the hook
        @return The hook context and the enabled status
        """
        physAddr &= 0xFFFFFFFFFFFFF000

        assert(physAddr in self.hooks)
        hookCtx = self.hooks[physAddr][0]
        enabled = self.hooks[physAddr][1]
        return hookCtx, enabled

    def __del__(self):
        physAddrList = list(self.hooks.keys())
        for physAddr in physAddrList:
            self.Remove(physAddr)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ept_hook = EptHookSession()

    v1 = AllocKernelVar(0x1000)
    v1.Set(b"\x48\xC7\xC0\x45\x00\x00\x00\xC3")
    logging.info(f"v1 Executed: {v1.Execute()}")
    v2 = AllocKernelVar(0x1000)
    v2.Set(b"\xB8\x4a\x00\x00\x00\xc3")
    logging.info(f"v2 Executed: {v2.Execute()}")

    ept_hook.Add(v1.Phys())
    ept_hook.Enable(v1.Phys())

    ept_hook.Modify(v1.Phys(), v2)
    hookCtx, enabled = ept_hook.Get(v1.Phys())
    logging.info(f"Hook context: {hookCtx[:16]}...")
    logging.info(f"Enabled: {enabled}")
    
    logging.info(f"v1 Executed: {v1.Execute()}")
    logging.info(f"v1 Get: {v1.Get()[:16]}...")
    ept_hook.Disable(v1.Phys())
    logging.info(f"v1 Executed: {v1.Execute()}")
    logging.info(f"v1 Get: {v1.Get()[:16]}...")
    ept_hook.Remove(v1.Phys())