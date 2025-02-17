#pragma once

#include "pch.h"

/*
 * @brief Copy a non-paged buffer (as guest).
 */
extern "C" __declspec(dllexport) VOID HyroApirGuestGnrCopyNonPagedBuffer(PVOID dst, PVOID src, SIZE_T size);

/*
 * @brief Execute a non-paged buffer (as guest).
 */
extern "C" __declspec(dllexport) UINT64 HyroApirGuestGnrExecuteNonPagedBuffer(PVOID buffer, ULONG maxExecuteLength);