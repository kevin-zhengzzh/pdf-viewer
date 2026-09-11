#!/usr/bin/env python3
"""
把本项目的静态文件（build/、web/）上传到阿里云 OSS，用于国内访问加速部署。

用法:
    export ALIYUN_ACCESS_KEY_ID=xxx
    export ALIYUN_ACCESS_KEY_SECRET=xxx
    python tools/deploy_oss.py --bucket my-bucket --endpoint oss-cn-hangzhou.aliyuncs.com

    # Windows PowerShell:
    $env:ALIYUN_ACCESS_KEY_ID="xxx"
    $env:ALIYUN_ACCESS_KEY_SECRET="xxx"
    python tools/deploy_oss.py --bucket my-bucket --endpoint oss-cn-hangzhou.aliyuncs.com

依赖:
    pip install oss2

AccessKey 不要写进代码或提交到仓库，从环境变量读取。

上传完成后，访问地址形如:
    https://<bucket>.<endpoint>/web/viewer.html?file=docs/1.pdf
"""

import argparse
import mimetypes
import os
import sys
from pathlib import Path

try:
    import oss2
except ImportError:
    sys.exit("缺少依赖 'oss2'。请先运行: pip install oss2")

REPO_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_DIRS = ["build", "web"]

# 一些系统的默认 MIME 库不认识这些后缀，手动指定，
# 否则浏览器可能拒绝执行 .mjs 模块脚本（表现为页面空白）。
EXTRA_CONTENT_TYPES = {
    ".mjs": "text/javascript",
    ".js": "text/javascript",
    ".wasm": "application/wasm",
    ".ftl": "text/plain; charset=utf-8",
    ".pdf": "application/pdf",
}


def guess_content_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in EXTRA_CONTENT_TYPES:
        return EXTRA_CONTENT_TYPES[ext]
    guessed, _ = mimetypes.guess_type(path.name)
    return guessed or "application/octet-stream"


def iter_files():
    for top in UPLOAD_DIRS:
        top_path = REPO_ROOT / top
        if not top_path.is_dir():
            continue
        for path in top_path.rglob("*"):
            if path.is_file():
                yield path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bucket", required=True, help="OSS Bucket 名称")
    parser.add_argument(
        "--endpoint",
        required=True,
        help="OSS Endpoint，例如 oss-cn-hangzhou.aliyuncs.com",
    )
    args = parser.parse_args()

    access_key_id = os.environ.get("ALIYUN_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIYUN_ACCESS_KEY_SECRET")
    if not access_key_id or not access_key_secret:
        sys.exit(
            "请先设置环境变量 ALIYUN_ACCESS_KEY_ID 和 ALIYUN_ACCESS_KEY_SECRET"
        )

    auth = oss2.Auth(access_key_id, access_key_secret)
    endpoint = args.endpoint
    if not endpoint.startswith("http"):
        endpoint = f"https://{endpoint}"
    bucket = oss2.Bucket(auth, endpoint, args.bucket)

    files = list(iter_files())
    if not files:
        sys.exit("没有找到要上传的文件，确认在项目根目录下运行本脚本。")

    print(f"准备上传 {len(files)} 个文件到 oss://{args.bucket} ...")
    for path in files:
        key = path.relative_to(REPO_ROOT).as_posix()
        content_type = guess_content_type(path)
        headers = {"Content-Type": content_type}
        bucket.put_object_from_file(key, str(path), headers=headers)
        print(f"  {key}  ({content_type})")

    host = args.endpoint.replace("https://", "").replace("http://", "")
    print("\n上传完成。访问地址示例:")
    print(f"  https://{args.bucket}.{host}/web/viewer.html?file=docs/1.pdf")


if __name__ == "__main__":
    main()
