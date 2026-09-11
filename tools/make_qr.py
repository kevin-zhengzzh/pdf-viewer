#!/usr/bin/env python3
"""
根据一条 URL 生成二维码 PNG（纯黑白，无 logo、无水印）。

用法:
    python tools/make_qr.py "https://<user>.github.io/<repo>/web/viewer.html?file=docs/mydoc.pdf"
    python tools/make_qr.py "https://..." -o qr.png

依赖:
    pip install qrcode[pil]
"""

import argparse
import sys

try:
    import qrcode
except ImportError:
    sys.exit(
        "缺少依赖 'qrcode'。请先运行: pip install qrcode[pil]"
    )


def make_qr(url: str, output: str) -> None:
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output)
    print(f"已生成二维码: {output}")
    print(f"编码内容: {url}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="要编码进二维码的链接")
    parser.add_argument(
        "-o", "--output", default="qr.png", help="输出文件路径（默认 qr.png）"
    )
    args = parser.parse_args()
    make_qr(args.url, args.output)


if __name__ == "__main__":
    main()
