#include "pch.h"

BOOL HyroApirTest() {
	BOOL returnValue = FALSE;

	if (!Ioctl::Request(
		GloVar::Ioctl::IOCTL_HYROAPI_TEST,
		NULL,
		0,
		&returnValue,
		sizeof(BOOL)
	)) {
		return FALSE;
	}

	return returnValue;
}