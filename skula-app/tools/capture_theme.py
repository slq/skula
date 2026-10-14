"""Capture the application's own demo window on Windows.

Run from skula-app: .venv/Scripts/python.exe tools/capture_theme.py
Only in-memory demo snapshots are used; no account storage, polling or network.
"""
import argparse
import ctypes
from ctypes import wintypes as w
from pathlib import Path
import struct
import sys
import time
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skula_app.core import Controller
from skula_app.ui import create_app


class DemoStorage:
    persistent = False
    def save(self, state): pass
    def load(self): raise AssertionError("Screenshot run must not restore account data")
    def clear(self): raise AssertionError("Screenshot run must not clear account data")


def capture_window(root, path):
    """Print only our Tk window into a memory DC; never capture the desktop."""
    user = ctypes.WinDLL("user32", use_last_error=True)
    gdi = ctypes.WinDLL("gdi32", use_last_error=True)
    user.GetParent.argtypes = [w.HWND]; user.GetParent.restype = w.HWND
    user.GetDC.argtypes = [w.HWND]; user.GetDC.restype = w.HDC
    user.ReleaseDC.argtypes = [w.HWND, w.HDC]
    user.PrintWindow.argtypes = [w.HWND, w.HDC, w.UINT]
    gdi.CreateCompatibleDC.argtypes = [w.HDC]; gdi.CreateCompatibleDC.restype = w.HDC
    gdi.CreateCompatibleBitmap.argtypes = [w.HDC, ctypes.c_int, ctypes.c_int]; gdi.CreateCompatibleBitmap.restype = w.HBITMAP
    gdi.SelectObject.argtypes = [w.HDC, w.HANDLE]; gdi.SelectObject.restype = w.HANDLE
    gdi.GetDIBits.argtypes = [w.HDC, w.HBITMAP, w.UINT, w.UINT, ctypes.c_void_p, ctypes.c_void_p, w.UINT]
    gdi.DeleteObject.argtypes = [w.HANDLE]; gdi.DeleteDC.argtypes = [w.HDC]
    hwnd = user.GetParent(root.winfo_id()) or root.winfo_id()
    width, height = root.winfo_width(), root.winfo_height()
    dc = user.GetDC(hwnd)
    memory = gdi.CreateCompatibleDC(dc)
    bitmap = gdi.CreateCompatibleBitmap(dc, width, height)
    old = gdi.SelectObject(memory, bitmap)
    try:
        if not user.PrintWindow(hwnd, memory, 3):
            raise ctypes.WinError(ctypes.get_last_error())
        gdi.SelectObject(memory, old)
        header = struct.pack("<IiiHHIIiiII", 40, width, -height, 1, 32, 0, width*height*4, 0, 0, 0, 0)
        info = ctypes.create_string_buffer(header + bytes(4))
        pixels = ctypes.create_string_buffer(width*height*4)
        if gdi.GetDIBits(memory, bitmap, 0, height, pixels, info, 0) != height:
            raise RuntimeError("Could not read the application's screenshot")
        raw = pixels.raw
        scanlines = bytearray()
        for y in range(height):
            scanlines.append(0)
            row = raw[y*width*4:(y+1)*width*4]
            for x in range(width):
                i=x*4
                scanlines.extend((row[i+2], row[i+1], row[i]))
        def chunk(kind, data):
            return struct.pack(">I",len(data))+kind+data+struct.pack(">I",zlib.crc32(kind+data)&0xffffffff)
        png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB",width,height,8,2,0,0,0))
        png += chunk(b"IDAT",zlib.compress(scanlines,6))+chunk(b"IEND",b"")
        path.write_bytes(png)
        print(path.name, f"{width}x{height}")
    finally:
        gdi.SelectObject(memory, old)
        gdi.DeleteObject(bitmap); gdi.DeleteDC(memory); user.ReleaseDC(hwnd, dc)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--size", default="1280x880")
    parser.add_argument("--output", default="docs/screenshots")
    args=parser.parse_args()
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    controller=Controller(storage=DemoStorage(), notifier=lambda *a:True, start_ticker=False)
    app=create_app(controller, restore=False)
    errors=[]
    app.root.report_callback_exception=lambda *error: errors.append(error)
    app.root.overrideredirect(True)
    app.root.geometry(args.size+"+30+30")
    controller.demo()
    if not controller.wait_idle():
        raise RuntimeError("Demo did not finish loading")
    app._render_state(controller._state())
    app.root.update()
    output=Path(args.output); output.mkdir(parents=True,exist_ok=True)
    try:
        for page in ("overview","messages","schedule","settings"):
            app.select_page(page)
            if page=="messages":
                view=app.views[page]
                row=view.tree.get_children()[0]
                view.tree.selection_set(row)
                view._select()
            app.root.update()
            time.sleep(0.15)
            app.root.update()
            capture_window(app.root,output/({"overview":"start","schedule":"calendar"}.get(page,page)+".png"))
        if errors:
            raise RuntimeError(errors)
    finally:
        app.close()


if __name__=="__main__":
    main()
