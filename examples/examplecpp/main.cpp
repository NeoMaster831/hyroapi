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

	auto HyroApiTest = (BOOL(*)())GetProcAddress(hDll, "HyroApiTest");

	if (HyroApiTest == NULL) {
		std::cout << "Failed to get the function." << std::endl;
		return 1;
	}

	std::cout << HyroApiTest() << std::endl;

}