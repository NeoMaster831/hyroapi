#include "pch.h"

VOID HyroApirGuestGnrCopyNonPagedBuffer(PVOID dst, PVOID src, SIZE_T size) {
  APIW_COPY_NONPAGED_BUFFER_REQUEST request = { dst, src, size };
  Ioctl::Request(
    GloVar::Ioctl::IOCTL_HYROAPI_GUEST_GENERAL_COPY_NONPAGED_BUFFER,
    &request,
    sizeof(APIW_COPY_NONPAGED_BUFFER_REQUEST),
    NULL,
    0
  );
}

UINT64 HyroApirGuestGnrExecuteNonPagedBuffer(PVOID buffer, ULONG maxExecuteLength) {
  APIW_EXECUTE_NONPAGED_BUFFER_REQUEST request = { buffer, maxExecuteLength };
  UINT64 result = 0xFFFF'FFFF'FFFF'FFFF;

  Ioctl::Request(
    GloVar::Ioctl::IOCTL_HYROAPI_GUEST_GENERAL_EXECUTE_NONPAGED_BUFFER,
    &request,
    sizeof(APIW_EXECUTE_NONPAGED_BUFFER_REQUEST),
    &result,
    sizeof(UINT64)
  );

  return result;
}