# 无水印 PDF 网页展示

用 [pdf.js](https://github.com/mozilla/pdf.js) 官方发行版搭建的静态 PDF 阅读页，界面基于 pdf.js 原生阅读器（目录、搜索、页码、缩放、更多菜单），统一深色配色、隐藏了批注编辑按钮，只保留纯展示所需的功能，**没有任何第三方水印或标识**。纯静态站点，用 GitHub Pages 免费托管。

## 目录结构

```
/
├── build/              # pdf.js 官方核心文件（worker、渲染引擎），勿改
├── web/
│   ├── viewer.html         # pdf.js 官方阅读器页面（加了一行引用下面这个文件，见下）
│   ├── title-override.js   # 自定义文件：支持用 ?title= 参数自定义抬头，与文件名无关
│   ├── viewer.mjs 等       # 官方发行版自带文件（有两处配置改动，见下）
│   └── docs/
│       └── 1.pdf           # 放你自己的 PDF
├── tools/
│   ├── make_qr.py      # 生成访问二维码
│   └── serve.py        # 本地预览服务器（修正 .mjs MIME 类型，支持局域网访问）
└── README.md
```

`build/` 和 `web/` 必须保持同级目录关系，因为 `web/viewer.mjs` 内部用相对路径 `../build/...` 引用 worker 文件——这是 pdf.js 官方发行版的固定结构，不要移动或改名这两个文件夹。

**对官方文件做的两处改动**（都在 `web/viewer.mjs`，都是改配置项的默认值，没有增删任何代码逻辑）：

| 配置项 | 原值 | 改成 | 作用 |
|---|---|---|---|
| `viewerCssTheme` | `0`（跟随系统深色/浅色模式） | `2`（强制深色） | 不管扫码设备本身是浅色还是深色主题，阅读页都统一显示深色配色 |
| `annotationEditorMode` | `0`（显示批注编辑功能） | `-1`（禁用） | 工具栏隐藏画笔/文字/高亮/插图这几个批注编辑按钮，只保留纯展示所需的侧栏、搜索、页码、缩放，风格更接近参考模板；这也符合"纯展示、不需要让人在你的 PDF 上画图"的场景 |

以后升级 pdf.js 版本、重新替换 `web/viewer.mjs` 时，记得在新文件里搜索这两个配置项名，把值改回上表中"改成"那一列。

**另外新增了一个文件**：`web/title-override.js`，配合 `web/viewer.html` 里多加的一行 `<script src="title-override.js">`，用来支持自定义抬头（见下面"想改抬头"一节）。升级 pdf.js 时这两个文件/改动不会被覆盖，正常保留即可；如果重新解压官方 zip 覆盖了 `viewer.html`，记得把这一行 `<script>` 标签重新加回去。

## 1. 替换成你自己的 PDF

把你的 PDF 文件放进 `web/docs/` 目录，例如：

```
web/docs/report.pdf
```

然后访问时用 `?file=` 参数指向它（相对 `viewer.html` 所在目录的路径）：

```
web/viewer.html?file=docs/report.pdf
```

- 想同时放多个 PDF：把它们都放进 `web/docs/`，用不同的 `?file=` 值区分即可，例如：
  - `viewer.html?file=docs/report.pdf`
  - `viewer.html?file=docs/handbook.pdf`
- 文件名建议用英文/数字/下划线，避免中文或空格在 URL 里需要转义导致链接变长。

### 想改抬头/标题怎么办

浏览器标签页标题、以及微信内置浏览器打开时顶部那栏大标题，pdf.js 默认显示的是**文件名本身**。如果想要一个跟文件名完全无关的自定义抬头，在链接后面加一个 `title` 参数即可：

```
viewer.html?file=docs/1.pdf&title=我的自定义标题
```

抬头会精确显示成"我的自定义标题"，跟 `1.pdf` 这个文件名没有任何关系（`title` 参数支持中文，正常 URL 编码/交给二维码工具处理即可，浏览器地址栏会自动帮你编码）。这是靠新增的 [web/title-override.js](web/title-override.js) 实现的：page 加载后如果检测到 `title` 参数，就把它锁定为 `document.title`，不管 pdf.js 自己怎么根据文件名/元数据重新设置标题，都会被这个自定义值覆盖。

如果不加 `title` 参数，就还是 pdf.js 默认行为——显示文件名（含 `.pdf` 后缀）。多个 PDF 的话，每个链接各自带上想要的 `title` 就行，互不影响。

## 2. 本地预览

在仓库根目录起本地服务器：

```bash
python tools/serve.py
```

浏览器打开：

```
http://localhost:8000/web/viewer.html?file=docs/1.pdf
```

确认：能正常翻页、缩放、搜索、查看目录，且页面上没有任何水印或第三方标识。

> **不要**直接用 `python -m http.server` 或双击打开 `viewer.html`。
> - 双击打开是 `file://` 协议，浏览器会拦截 pdf.js 加载同目录 PDF 的请求，表现为页面空白、页码显示 `0 / 0`。
> - 部分系统上 `python -m http.server` 会把 `.mjs` 脚本当成 `text/plain` 返回，浏览器的模块脚本严格 MIME 检查会拒绝执行，同样导致页面空白。`tools/serve.py` 已经修正了这个 MIME 类型问题。
>
> 手机窄屏打开时，工具栏会自动收起为"侧栏/搜索/页码/缩放/更多"这种精简样式，这是 pdf.js 官方的响应式效果，不需要额外配置；配色统一是深色（见上面"唯一对官方文件做的改动"），不受手机系统主题影响。

### 用手机在同一 WiFi 下扫码测试

部署上线前，如果想先用手机扫码验证效果，可以让本地服务器监听局域网：

```bash
python tools/serve.py 8000 --lan
```

终端会打印出局域网地址（形如 `http://192.168.x.x:8000/`），把它拼成完整链接后用 [tools/make_qr.py](tools/make_qr.py) 生成二维码，手机在**同一个 WiFi** 下扫码即可打开。首次运行可能会弹出 Windows 防火墙提示，选"允许访问"（专用网络）。

> 注意：`--lan` 模式下，同一局域网内的其他设备也能访问到 `web/docs/` 里的所有 PDF，仅在信任当前网络（如自己家里）时使用，测试完 `Ctrl+C` 关掉即可。如果 PDF 内容比较私密，测试完成后没有必要再一直开着。

## 3. 部署到 GitHub Pages

1. 在 GitHub 新建一个仓库（或使用已有仓库），把本项目所有文件推送上去：

   ```bash
   git init
   git add .
   git commit -m "Add PDF viewer site"
   git branch -M main
   git remote add origin https://github.com/<你的用户名>/<仓库名>.git
   git push -u origin main
   ```

   （仓库已包含 `.nojekyll` 文件，避免 GitHub Pages 默认的 Jekyll 处理干扰 pdf.js 的静态资源，不需要额外配置。）

2. 打开仓库的 **Settings → Pages**。
3. 在 **Build and deployment** 下，Source 选择 **Deploy from a branch**，Branch 选择 `main`（目录选 `/root`），点击 **Save**。
4. 等待 1~2 分钟，Pages 会给出一条形如下面的线上链接：

   ```
   https://<你的用户名>.github.io/<仓库名>/
   ```

5. 最终阅读页链接（把 `<user>`、`<repo>`、`<pdf>` 换成实际值）：

   ```
   https://<user>.github.io/<repo>/web/viewer.html?file=docs/<pdf>
   ```

   例如：

   ```
   https://alice.github.io/my-pdf-site/web/viewer.html?file=docs/report.pdf
   ```

> GitHub Pages 默认几分钟内生效；如果打开是 404，先检查 Pages 是否已经 "Your site is live at ..."，或稍等重试。

## 4. 生成访问二维码

安装依赖（只需一次）：

```bash
pip install qrcode[pil]
```

生成二维码（把 URL 换成第 3 步得到的最终链接）：

```bash
python tools/make_qr.py "https://<user>.github.io/<repo>/web/viewer.html?file=docs/report.pdf" -o qr.png
```

会在当前目录生成 `qr.png`，纯黑白二维码，无 logo、无水印，扫码即可直接打开 PDF 阅读页。

## 关于访问控制的说明

这是一个**纯静态站点**，没有后端、没有登录鉴权。只要知道链接，任何人都能访问到你放在 `web/docs/` 里的 PDF——GitHub Pages 的仓库如果是 public，PDF 文件本身也可以被直接下载到（`.../web/docs/report.pdf`）。

如果你需要真正的访问控制（比如限制特定人查看、访问后失效、防止下载等），纯静态托管做不到，需要换成带后端的方案（例如加一层鉴权服务、签名的临时链接等）。这里不提供假的"登录/权限"实现，以免造成"文件受保护"的错觉。

## 常见问题

- **想用别的托管方式（Netlify、Vercel、自己的服务器）？** 完全可以，把 `build/`、`web/` 整个目录原样部署为静态资源即可，注意保持两者的同级关系，访问路径同样是 `.../web/viewer.html?file=...`。
- **想改阅读页标题？** 浏览器标签页标题默认显示当前 PDF 文件名，无需改动即可满足大多数需求；如需自定义，可在 PDF 的文档属性（Title 元数据）里设置。
- **pdf.js 版本更新了怎么办？** 去 [pdf.js Releases](https://github.com/mozilla/pdf.js/releases) 下载最新的 `pdfjs-x.x.x-dist.zip`，解压后用其中的 `build/` 和 `web/`（除 `web/docs/`）整体替换本仓库对应目录，然后记得在新的 `web/viewer.mjs` 里把 `viewerCssTheme` 的默认值改回 `2`（强制深色，见前面说明），其余官方文件不需要也不要手动改动。
