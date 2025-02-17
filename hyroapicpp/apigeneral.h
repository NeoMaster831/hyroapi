#pragma once

#include "pch.h"

/*
 * @brief Get the physical address of a virtual address.
 * @param virtualAddress The virtual address to get the physical address of.
 * @return UINT64 - The physical address of the virtual address.
 */
extern "C" __declspec(dllexport) UINT64 HyroApirGnrGetPhysAddr(UINT64 virtualAddress);

/*
 * @brief Allocate a non-paged buffer.
 * @param size The size of the buffer to allocate.
 * @return PVOID - The allocated buffer.
 */
extern "C" __declspec(dllexport) PVOID HyroApirGnrAllocNonPagedBuffer(UINT64 size);

/*
 * @brief Free a non-paged buffer.
 * @param buffer The buffer to free.
 */
extern "C" __declspec(dllexport) VOID HyroApirGnrFreeNonPagedBuffer(PVOID buffer);

typedef struct _APIW_COPY_NONPAGED_BUFFER_REQUEST {
  PVOID dest;
  PVOID src;
  SIZE_T size;
} APIW_COPY_NONPAGED_BUFFER_REQUEST, * PAPIW_COPY_NONPAGED_BUFFER_REQUEST;

/*
 * @brief Copy a non-paged buffer.
 * @param dst The destination buffer.
 * @param src The source buffer.
 * @param size The size of the buffer to copy.
 */
extern "C" __declspec(dllexport) VOID HyroApirGnrCopyNonPagedBuffer(PVOID dst, PVOID src, SIZE_T size);

typedef struct _APIW_EXECUTE_NONPAGED_BUFFER_REQUEST {
  PVOID buffer;
  ULONG maxExecuteLength;
} APIW_EXECUTE_NONPAGED_BUFFER_REQUEST, * PAPIW_EXECUTE_NONPAGED_BUFFER_REQUEST;

/*
 * @brief Execute a non-paged buffer.
 * @param buffer The buffer to execute.
 */
extern "C" __declspec(dllexport) UINT64 HyroApirGnrExecuteNonPagedBuffer(PVOID buffer, ULONG maxExecuteLength);