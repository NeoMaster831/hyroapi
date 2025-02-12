#pragma once

#include "pch.h"

namespace GloVar {

	namespace Ioctl {

		// (..., ..., METHOD_BUFFERED, FILE_ANY_ACCESS)

		const DWORD IOCTL_HYROAPI_TEST = \
			CTL_CODE(FILE_DEVICE_UNKNOWN, 0x800, 0, 0);

		extern HANDLE hDevice;
	}

}