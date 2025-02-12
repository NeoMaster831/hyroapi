#pragma once

#ifdef _DEBUG

#define LogConsole(Format, ...) fprintf(stdout, Format, __VA_ARGS__)

#else

#define LogConsole(Format, ...)

#endif