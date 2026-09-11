# 无水印 PDF 网页展示

用 [pdf.js](https://github.com/mozilla/pdf.js) 官方发行版搭建的静态 PDF 阅读页，界面和 pdf.js 原生阅读器一致（侧栏、搜索、页码、缩放），统一深色配色，**没有任何第三方水印或标识**。纯静态网站，用 GitHub Pages 免费托管，扫码就能打开看 PDF。

**使用流程一共 4 步**：① 部署上线 → ② 放入你的 PDF → ③ 生成二维码 → ④（可选）自定义标题。下面按顺序讲。

## 免责声明

本项目是一个基于官方 pdf.js 的通用 PDF 展示模板，用途是让仓库所有者展示自己拥有合法权利的 PDF 文档。

- 使用者需自行对放入 `web/docs/` 的文件内容负责，确保拥有合法权利、内容不违反当地法律法规，不用于诈骗、侵权、传播违法信息等用途。
- 任何人 fork、克隆、部署本项目（包括修改后再分发）产生的后果，均由实际部署者和使用者自行承担，与本项目原作者无关。
- 本项目不提供任何身份鉴权或访问控制（见下文"关于访问控制的说明"），请勿用它托管需要保密或限制访问的内容。

---

## ① 部署上线（只需做一次）

> 已经部署过的可以跳过这一步。示例仓库：`kevin-zhengzzh/pdf-viewer`，把下面命令和链接里的用户名/仓库名换成你自己的即可。

**1. 推送到 GitHub**

在项目根目录执行：

```bash
git init
git add .
git commit -m "Add PDF viewer site"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

第一次 `push` 会弹出浏览器窗口要求登录 GitHub 账号，登录授权一下就行。

**2. 打开 Pages 功能**

打开仓库页面 → 顶部标签栏 **Settings**（不是右上角头像的账号设置）→ 左侧栏 **Pages**：
- Source 选 **Deploy from a branch**
- Branch 选 **main**，目录选 **/ (root)**
- 点 **Save**

等 1~2 分钟，页面会提示 "Your site is live at `https://<用户名>.github.io/<仓库名>/`"，部署就完成了。

> 直接打开这条链接会看到 404，这是正常的——首页不在根目录，而是在 `web/viewer.html`，见下一步。

## ② 放入你的 PDF

把 PDF 文件放进 `web/docs/` 目录，比如：

```
web/docs/report.pdf
```

访问链接是（`<file>` 换成你的文件名）：

```
https://<用户名>.github.io/<仓库名>/web/viewer.html?file=docs/<file>
```

举例，用户名 `kevin-zhengzzh`、仓库 `pdf-viewer`、文件 `1.pdf`：

```
https://kevin-zhengzzh.github.io/pdf-viewer/web/viewer.html?file=docs/1.pdf
```

- **想放多个 PDF**：都丢进 `web/docs/`，每个文件对应各自的链接（`?file=` 换成不同文件名），互不影响。
- **文件名**建议用英文/数字/下划线，避免中文或空格，链接会更短更干净。
- 改完文件要重新 `git add . && git commit -m "..." && git push`，GitHub Pages 会自动重新部署（等 1 分钟左右生效）。

## ③ 生成二维码

安装依赖（只需一次）：

```bash
pip install qrcode[pil]
```

生成二维码（把 URL 换成第 ② 步的最终链接）：

```bash
python tools/make_qr.py "https://kevin-zhengzzh.github.io/pdf-viewer/web/viewer.html?file=docs/1.pdf" -o qr.png
```

当前目录会生成 `qr.png`，纯黑白二维码，无 logo、无水印，扫码即可直接打开对应的 PDF。**每个 PDF 各自生成一张自己的二维码**（链接不同，图案自然也不同）。

## ④（可选）自定义标题

默认情况下，浏览器标签页 / 微信内打开时顶部显示的标题就是**文件名**（比如 `1.pdf`）。如果想显示一个跟文件名无关的自定义标题，在链接后面加 `&title=你的标题`：

```
https://kevin-zhengzzh.github.io/pdf-viewer/web/viewer.html?file=docs/1.pdf&title=我的自定义标题
```

打开后标题会精确显示成"我的自定义标题"，和 `1.pdf` 这个文件名完全没关系，支持中文。**生成二维码时把这条带 `title` 参数的完整链接交给 `make_qr.py` 就行**，用法跟第 ③ 步一样。

不加 `title` 参数就还是默认行为（显示文件名）。多个 PDF 可以各自设置不同标题，互不影响。

---

## 关于访问控制的说明

这是一个**纯静态站点**，没有后端、没有登录鉴权。只要知道链接，任何人都能访问到你放在 `web/docs/` 里的 PDF——仓库是 public 的话，PDF 文件本身也能被直接下载到（`.../web/docs/report.pdf`）。

如果需要真正的访问控制（比如限制特定人查看、链接失效、防止下载），纯静态托管做不到，需要换成带后端的方案。这里不提供假的"登录/权限"实现，以免造成"文件受保护"的错觉。

## 本地开发 / 测试（非必须，改代码时才需要）

想在自己电脑上先看效果、再决定要不要推送上线，可以起本地服务器：

```bash
python tools/serve.py
```

浏览器打开 `http://localhost:8000/web/viewer.html?file=docs/1.pdf`。

> **不要**用 `python -m http.server` 或双击打开 `viewer.html`——前者在部分系统上会把 `.mjs` 脚本识别成错误的类型导致页面空白，后者是 `file://` 协议会被浏览器拦截。`tools/serve.py` 已经处理好这些问题（线上 GitHub Pages 本身没有这个问题，只有本地起服务时才需要注意）。

**想用手机在同一 WiFi 下扫码测试**（上线前预览）：

```bash
python tools/serve.py 8000 --lan
```

终端会打印局域网地址（如 `http://192.168.x.x:8000/`），拼成完整链接后用 `make_qr.py` 生成二维码，手机连同一个 WiFi 扫码即可。首次运行可能弹出 Windows 防火墙提示，选"允许访问"（专用网络）。测试完 `Ctrl+C` 关掉，同一局域网的其他设备在服务器开着期间也能访问到 `web/docs/` 里的文件，别一直开着。

## 目录结构 & 技术细节

```
/
├── build/                  # pdf.js 官方核心文件（worker、渲染引擎），勿改
├── web/
│   ├── viewer.html         # pdf.js 官方阅读器页面（加了一行引用 title-override.js）
│   ├── title-override.js   # 自定义文件：支持 ?title= 参数自定义抬头，见"④ 自定义标题"
│   ├── viewer.mjs 等       # 官方发行版自带文件（有两处配置改动，见下表）
│   └── docs/
│       └── 1.pdf           # 放你自己的 PDF
├── tools/
│   ├── make_qr.py          # 生成访问二维码
│   └── serve.py            # 本地预览服务器
└── README.md
```

`build/` 和 `web/` 必须保持同级目录关系，因为 `web/viewer.mjs` 内部用相对路径 `../build/...` 引用 worker 文件——这是 pdf.js 官方发行版的固定结构，不要移动或改名这两个文件夹。

**对官方文件做的两处改动**（都在 `web/viewer.mjs`，只改配置项默认值，没有增删任何代码逻辑）：

| 配置项 | 原值 | 改成 | 作用 |
|---|---|---|---|
| `viewerCssTheme` | `0`（跟随系统深色/浅色模式） | `2`（强制深色） | 不管访问设备本身是浅色还是深色主题，阅读页都统一显示深色配色 |
| `annotationEditorMode` | `0`（显示批注编辑功能） | `-1`（禁用） | 工具栏隐藏画笔/文字/高亮/插图这几个批注编辑按钮，只保留纯展示所需的侧栏、搜索、页码、缩放 |

以后升级 pdf.js 版本、重新替换 `web/viewer.mjs` 时，记得在新文件里搜索这两个配置项名，把值改回上表"改成"那一列；同时把 `web/viewer.html` 里 `<script src="title-override.js">` 这一行加回去（新解压的官方文件不会包含它）。

## 常见问题

- **想用别的托管方式（Netlify、Vercel、自己的服务器）？** 完全可以，把 `build/`、`web/` 整个目录原样部署为静态资源即可，保持两者同级关系，访问路径同样是 `.../web/viewer.html?file=...`。
- **pdf.js 版本更新了怎么办？** 去 [pdf.js Releases](https://github.com/mozilla/pdf.js/releases) 下载最新的 `pdfjs-x.x.x-dist.zip`，解压后用其中的 `build/` 和 `web/`（除 `web/docs/`）整体替换本仓库对应目录，然后按上一节说明重新应用那两处配置改动和 `title-override.js` 的引用。
- **打开是 404？** 先确认访问的是 `.../web/viewer.html?file=...` 而不是网站根目录（根目录 404 是正常的，见"① 部署上线"）；再检查 Pages 是否已经提示 "Your site is live at ..."，刚部署完可能需要等 1~2 分钟。
