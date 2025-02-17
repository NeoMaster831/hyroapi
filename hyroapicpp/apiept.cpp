#include "pch.h"

BOOL HyroApirEptHookAdd(UINT64 physAddr) {
  UINT64 inputBuffer = physAddr;
	BOOL returnValue = FALSE;

	if (!Ioctl::Request(
		GloVar::Ioctl::IOCTL_HYROAPI_EPT_ADD,
		&inputBuffer,
		sizeof(UINT64),
		&returnValue,
		sizeof(BOOL)
	)) {
		return FALSE;
	}

	return returnValue;
}

VOID HyroApirEptHookRemove(UINT64 physAddr) {
  UINT64 inputBuffer = physAddr;
  if (!Ioctl::Request(
    GloVar::Ioctl::IOCTL_HYROAPI_EPT_REMOVE,
    &inputBuffer,
    sizeof(UINT64),
    NULL,
    0
  )) {
    return;
  }
}

BOOL HyroApirEptHookEnable(UINT64 physAddr) {
  UINT64 inputBuffer = physAddr;
  BOOL returnValue = FALSE;
  if (!Ioctl::Request(
    GloVar::Ioctl::IOCTL_HYROAPI_EPT_ENABLE,
    &inputBuffer,
    sizeof(UINT64),
    &returnValue,
    sizeof(BOOL)
  )) {
    return FALSE;
  }
  return returnValue;
}

VOID HyroApirEptHookDisable(UINT64 physAddr) {
  UINT64 inputBuffer = physAddr;
  if (!Ioctl::Request(
    GloVar::Ioctl::IOCTL_HYROAPI_EPT_DISABLE,
    &inputBuffer,
    sizeof(UINT64),
    NULL,
    0
  )) {
    return;
  }
}

BOOL HyroApirEptHookModify(UINT64 physAddr, PVOID hookCtx) {
  APIW_EPT_MODIFY_REQUEST inputBuffer = { physAddr, hookCtx };
  BOOL returnValue = FALSE;
  if (!Ioctl::Request(
    GloVar::Ioctl::IOCTL_HYROAPI_EPT_MODIFY,
    &inputBuffer,
    sizeof(APIW_EPT_MODIFY_REQUEST),
    &returnValue,
    sizeof(BOOL)
  )) {
    return FALSE;
  }
  return returnValue;
}