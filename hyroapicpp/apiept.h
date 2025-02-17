#pragma once

#include "pch.h"

/*
 * @brief Add an Ept Hook.
 * @param physAddr The physical address to hook.
 * @return BOOL - TRUE if the Ept Hook was added successfully.
 */
extern "C" __declspec(dllexport) BOOL HyroApirEptHookAdd(UINT64 physAddr);

/*
 * @brief Remove an Ept Hook.
 * @param physAddr The physical address to unhook.
 */
extern "C" __declspec(dllexport) VOID HyroApirEptHookRemove(UINT64 physAddr);

/*
 * @brief Enable an Ept Hook.
 * @param physAddr The physical address to enable.
 * @return BOOL - TRUE if the Ept Hook was enabled successfully.
 */
extern "C" __declspec(dllexport) BOOL HyroApirEptHookEnable(UINT64 physAddr);

/*
 * @brief Disable an Ept Hook.
 * @param physAddr The physical address to disable.
 */
extern "C" __declspec(dllexport) VOID HyroApirEptHookDisable(UINT64 physAddr);

typedef struct _APIW_EPT_MODIFY_REQUEST {
  UINT64 physicalAddr;
  PVOID hookCtx;
} APIW_EPT_MODIFY_REQUEST, * PAPIW_EPT_MODIFY_REQUEST;

/*
 * @brief Modify an Ept Hook.
 * @param physAddr The physical address to modify.
 * @param hookCtx Context of the hook (virtual address)
 * @return BOOL - TRUE if the Ept Hook was modified successfully.
 */
extern "C" __declspec(dllexport) BOOL HyroApirEptHookModify(UINT64 physAddr, PVOID hookCtx);