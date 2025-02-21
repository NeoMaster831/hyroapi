from hyroapipy.all import *

logging.basicConfig(level=logging.INFO)

ioctlSession = IOCTLSession()

# Test the IOCTL session
test = TestSession(ioctlSession)
test.Test()
del test

kernelVar1 = AllocKernelVar(0x1000, ioctlSession)

logging.info(f"Kernel buffer: {hex(kernelVar1.Virt())}")
logging.info(f"Kernel buffer phys: {hex(kernelVar1.Phys())}")

kernelVar1.Set(b"\x48\xC7\xC0\x45\x00\x00\x00\xC3")
result = kernelVar1.Execute()
logging.info(f"Result: {result}")

assert(result == 69)

eptHook = EptHookSession(ioctlSession)
eptHook.Add(kernelVar1.Phys())
eptHook.Enable(kernelVar1.Phys())

kernelVar2 = AllocKernelVar(0x1000, ioctlSession)
kernelVar2.Set(b"\xB8\x4a\x00\x00\x00\xc3")

eptHook.Modify(kernelVar1.Phys(), kernelVar2)
result = kernelVar1.Execute()
logging.info(f"Result (EPT Hooked): {result}")

assert(result == 74)

logging.info(f"But the code: {kernelVar1.Get()[:16]}...")

result = kernelVar1.Execute(mode=KernelVarRequestType.HOST)
logging.info(f"Result (HOST): {result}")

assert(result == 69)

eptHook.Disable(kernelVar1.Phys())
result = kernelVar1.Execute()
logging.info(f"Result (EPT Disabled): {result}")

assert(result == 69)

eptHook.Remove(kernelVar1.Phys())

del kernelVar1
del kernelVar2
del eptHook

logging.info("Session closed all successfully")

del ioctlSession