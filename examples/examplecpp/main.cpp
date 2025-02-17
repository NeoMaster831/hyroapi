#include <iostream>
#include <string>
#include <Windows.h>
#include <cassert>

#define A(x) if (x == 0) { std::cout << "Failed to get the function." << '\n'; return 1; }
int main()
{
	auto hDll = LoadLibrary(L"hyroapicpp.dll");
	if (hDll == NULL) {
		std::cout << "Failed to load the DLL." << '\n';
		return 1;
	}

	auto HyroApirTest = (BOOL(*)())GetProcAddress(hDll, "HyroApirTest");
	auto HyroApirGnrGetPhysAddr = (UINT64(*)(UINT64))GetProcAddress(hDll, "HyroApirGnrGetPhysAddr");
  auto HyroApirGnrAllocNonPagedBuffer = (PVOID(*)(UINT64))GetProcAddress(hDll, "HyroApirGnrAllocNonPagedBuffer");
  auto HyroApirGnrFreeNonPagedBuffer = (VOID(*)(PVOID))GetProcAddress(hDll, "HyroApirGnrFreeNonPagedBuffer");
  auto HyroApirGnrCopyNonPagedBuffer = (VOID(*)(PVOID, PVOID, SIZE_T))GetProcAddress(hDll, "HyroApirGnrCopyNonPagedBuffer");
  auto HyroApirGnrExecuteNonPagedBuffer = (UINT64(*)(PVOID, ULONG))GetProcAddress(hDll, "HyroApirGnrExecuteNonPagedBuffer");
  auto HyroApirGuestGnrCopyNonPagedBuffer = (VOID(*)(PVOID, PVOID, SIZE_T))GetProcAddress(hDll, "HyroApirGuestGnrCopyNonPagedBuffer");
  auto HyroApirGuestGnrExecuteNonPagedBuffer = (UINT64(*)(PVOID, ULONG))GetProcAddress(hDll, "HyroApirGuestGnrExecuteNonPagedBuffer");
	auto HyroApirEptHookAdd = (BOOL(*)(UINT64))GetProcAddress(hDll, "HyroApirEptHookAdd");
  auto HyroApirEptHookRemove = (VOID(*)(UINT64))GetProcAddress(hDll, "HyroApirEptHookRemove");
  auto HyroApirEptHookEnable = (BOOL(*)(UINT64))GetProcAddress(hDll, "HyroApirEptHookEnable");
  auto HyroApirEptHookDisable = (VOID(*)(UINT64))GetProcAddress(hDll, "HyroApirEptHookDisable");
  auto HyroApirEptHookModify = (BOOL(*)(UINT64, PVOID))GetProcAddress(hDll, "HyroApirEptHookModify");

  assert(HyroApirTest() == TRUE);

  auto kernelVar = HyroApirGnrAllocNonPagedBuffer(0x1000);
  std::cout << "Kernel buffer: " << std::hex << (UINT64)kernelVar << std::dec << '\n';

  // Let's test about getting the physical address of a virtual address.
  // You know we can't get the physical address of a virtual address in user mode.
  // But we can get the physical address of a virtual address in kernel mode.

  auto kernelPhysAddr = HyroApirGnrGetPhysAddr((UINT64)kernelVar);
  std::cout << "Kernel buffer physical address: " << std::hex << kernelPhysAddr << std::dec << '\n';

  // Let's test about copying a non-paged buffer.

  auto userArena1 = malloc(0x1000);
  RtlZeroMemory(userArena1, 0x1000);
  *(UINT64*)userArena1 = 0x4141414141414141; // Test..

  std::cout << "User buffer: " << std::hex << (UINT64)userArena1 << std::dec << '\n';
  std::cout << "User contents (UINT64): " << std::hex << *(UINT64*)userArena1 << std::dec << '\n';

  HyroApirGnrCopyNonPagedBuffer(kernelVar, userArena1, 0x1000);

  auto userArena2 = malloc(0x1000);
  RtlZeroMemory(userArena2, 0x1000);

  HyroApirGnrCopyNonPagedBuffer(userArena2, kernelVar, 0x2);

  std::cout << "User buffer 2: " << std::hex << (UINT64)userArena2 << std::dec << '\n';
  std::cout << "User contents 2 (UINT64): " << std::hex << *(UINT64*)userArena2 << std::dec << '\n';

  assert(*(UINT64*)userArena2 == 0x4141);

  free(userArena1);
  free(userArena2);

  UINT8 shellcode[] = {
    0x48, 0xC7, 0xC0, 0x45, 0x00, 0x00, 0x00, 
    0xC3
  }; // mov rax, 69; ret;

  // Now, let's test about executing a non-paged buffer.
  HyroApirGnrCopyNonPagedBuffer(kernelVar, (PVOID)shellcode, 0x8);

  auto result = HyroApirGnrExecuteNonPagedBuffer(kernelVar, 0x8);

  std::cout << "Result: " << result << '\n';

  assert(result == 69);

  // Testing EPT hooking.
  assert(HyroApirEptHookAdd(kernelPhysAddr));
  assert(HyroApirEptHookEnable(kernelPhysAddr));

  auto kernelVar2 = HyroApirGnrAllocNonPagedBuffer(0x1000);

  UINT8 shellcode2[] = { 
    0xB8, 0x4A, 0x00, 0x00, 0x00, 0xC3 
  }; // mov eax, 74; ret;

  HyroApirGnrCopyNonPagedBuffer(kernelVar2, (PVOID)shellcode2, 0x6);
  HyroApirEptHookModify(kernelPhysAddr, kernelVar2);

  // Now ept hook is enabled and modified.
  // Let's test about executing the kernelVar.

  result = HyroApirGuestGnrExecuteNonPagedBuffer(kernelVar, 0x8);
  // This should return 74.

  std::cout << "Result (EPT Hooked): " << result << '\n';

  assert(result == 74);
  UINT64 copied = 0;
  HyroApirGuestGnrCopyNonPagedBuffer(&copied, kernelVar, 0x8);

  std::cout << "But the code: " << std::hex << copied << std::dec << '\n';
  assert(copied == 0xc3'00'00'00'45'c0'c7'48);

  // Remove the hook and test once more.
  HyroApirEptHookDisable(kernelPhysAddr);
  HyroApirEptHookRemove(kernelPhysAddr);

  result = HyroApirGuestGnrExecuteNonPagedBuffer(kernelVar, 0x8);
  std::cout << "Result (EPT Unhooked): " << result << '\n';

  assert(result == 69);

  // Lastly free the buffer.
  HyroApirGnrFreeNonPagedBuffer(kernelVar2);
  HyroApirGnrFreeNonPagedBuffer(kernelVar);
  
  return 0;
}