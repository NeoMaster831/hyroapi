#include <iostream>
#include <string>
#include <Windows.h>

int main()
{
	auto hDll = LoadLibrary(L"hyroapicpp.dll");
	if (hDll == NULL) {
		std::cout << "Failed to load the DLL." << std::endl;
		return 1;
	}

	auto HyroApirTest = (BOOL(*)())GetProcAddress(hDll, "HyroApirTest");

	if (HyroApirTest == NULL) {
		std::cout << "Failed to get the function." << std::endl;
		return 1;
	}

	std::cout << HyroApirTest() << std::endl;

}