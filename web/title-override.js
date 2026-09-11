// 自定义项目功能(非 pdf.js 官方文件):支持用 URL 的 title 参数覆盖抬头，
// 与文件名完全无关。用法: viewer.html?file=docs/xxx.pdf&title=自定义标题
// pdf.js 加载文档过程中会多次自行设置 document.title，这里拦截 title 属性的
// 写入，确保后续任何赋值都不会覆盖自定义标题。
(function () {
  var params = new URLSearchParams(window.location.search);
  var customTitle = params.get("title");
  if (!customTitle) {
    return;
  }
  var titleEl = document.querySelector("title");
  if (!titleEl) {
    titleEl = document.createElement("title");
    document.head.appendChild(titleEl);
  }
  function applyFixedTitle() {
    titleEl.textContent = customTitle;
  }
  Object.defineProperty(document, "title", {
    configurable: true,
    get: function () {
      return customTitle;
    },
    set: function () {
      applyFixedTitle();
    },
  });
  applyFixedTitle();
})();
