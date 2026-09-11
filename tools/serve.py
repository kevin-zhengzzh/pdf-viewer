#!/usr/bin/env python3
"""
本地静态服务器,修正部分系统上 .mjs 文件被判定为 text/plain 的问题
(会导致浏览器以"strict MIME type checking"拒绝加载 pdf.js 的 ES 模块脚本,
表现为页面空白、页码显示 0/0)。

用法(在仓库根目录执行):
    python tools/serve.py                # 默认端口 8000,仅本机可访问(127.0.0.1)
    python tools/serve.py 8080           # 指定端口
    python tools/serve.py 8000 --lan     # 监听局域网,同一 WiFi 下手机可访问(用于扫码测试)

然后浏览器打开:
    http://localhost:8000/web/viewer.html?file=docs/1.pdf

注意: --lan 模式会让同一局域网内的其他设备也能访问到这台电脑上 web/docs/ 里的
所有 PDF,仅在你信任当前网络环境(如自己家里 WiFi)时使用,测试完建议 Ctrl+C 关闭。
"""

import functools
import http.server
import socket
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".mjs": "text/javascript",
        ".js": "text/javascript",
    }

    def end_headers(self):
        # 调试阶段禁用缓存,避免手机/浏览器缓存旧版 viewer.mjs 导致改动看起来没生效
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def main() -> None:
    args = sys.argv[1:]
    use_lan = "--lan" in args
    args = [a for a in args if a != "--lan"]
    port = int(args[0]) if args else 8000
    bind_host = "0.0.0.0" if use_lan else "127.0.0.1"
    display_host = lan_ip() if use_lan else "127.0.0.1"

    handler = functools.partial(Handler, directory=str(REPO_ROOT))
    with http.server.ThreadingHTTPServer((bind_host, port), handler) as httpd:
        if use_lan:
            print(f"局域网模式: 同一 WiFi 下的设备可通过 http://{display_host}:{port}/ 访问")
        print(f"Serving {REPO_ROOT} at http://{display_host}:{port}/")
        print(f"打开: http://{display_host}:{port}/web/viewer.html?file=docs/1.pdf")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
