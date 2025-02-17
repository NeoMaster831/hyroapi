#include "pch.h"

UINT64 HyroApirGnrGetPhysAddr(UINT64 virtualAddr, UINT64 cr3) {

  APIW_GET_PHYS_ADDR_REQUEST inputBuffer = { .virtualAddress = virtualAddr, .cr3 = cr3 };
  UINT64 outputBuffer = 0;
  if (!Ioctl::Request(
    GloVar::Ioctl::IOCTL_HYROAPI_GENERAL_GET_PHYSICAL_ADDRESS,
    &inputBuffer,
    sizeof(APIW_GET_PHYS_ADDR_REQUEST),
    &outputBuffer,
    sizeof(UINT64)
  )) {
    return 0;
  }

  return outputBuffer;
}

PVOID HyroApirGnrAllocNonPagedBuffer(UINT64 size) {
  PVOID outputBuffer = NULL;
  if (!Ioctl::Request(
    GloVar::Ioctl::IOCTL_HYROAPI_GENERAL_ALLOC_NONPAGED_BUFFER,
    &size,
    sizeof(UINT64),
    &outputBuffer,
    sizeof(PVOID)
  )) {
    return NULL;
  }
  return outputBuffer;
}

VOID HyroApirGnrFreeNonPagedBuffer(PVOID buffer) {
  Ioctl::Request(
    GloVar::Ioctl::IOCTL_HYROAPI_GENERAL_FREE_NONPAGED_BUFFER,
    &buffer,
    sizeof(PVOID),
    NULL,
    0
  );
}

VOID HyroApirGnrCopyNonPagedBuffer(PVOID dst, PVOID src, SIZE_T size) {
  APIW_COPY_NONPAGED_BUFFER_REQUEST request = { dst, src, size };
  Ioctl::Request(
    GloVar::Ioctl::IOCTL_HYROAPI_GENERAL_COPY_NONPAGED_BUFFER,
    &request,
    sizeof(APIW_COPY_NONPAGED_BUFFER_REQUEST),
    NULL,
    0
  );
}

UINT64 HyroApirGnrExecuteNonPagedBuffer(PVOID buffer, ULONG maxExecuteLength) {
  APIW_EXECUTE_NONPAGED_BUFFER_REQUEST request = { buffer, maxExecuteLength };
  UINT64 result = 0xFFFF'FFFF'FFFF'FFFF;

  Ioctl::Request(
    GloVar::Ioctl::IOCTL_HYROAPI_GENERAL_EXECUTE_NONPAGED_BUFFER,
    &request,
    sizeof(APIW_EXECUTE_NONPAGED_BUFFER_REQUEST),
    &result,
    sizeof(UINT64)
  );

  return result;
}