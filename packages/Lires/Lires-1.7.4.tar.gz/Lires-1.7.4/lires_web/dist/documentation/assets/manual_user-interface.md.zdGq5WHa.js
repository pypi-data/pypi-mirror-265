import{_ as a,c as e,o as i,a3 as l}from"./chunks/framework.CXhrtaSR.js";const _=JSON.parse('{"title":"界面元素","description":"","frontmatter":{},"headers":[],"relativePath":"manual/user-interface.md","filePath":"manual/user-interface.md"}'),s={name:"manual/user-interface.md"},t=l('<h1 id="界面元素" tabindex="-1">界面元素 <a class="header-anchor" href="#界面元素" aria-label="Permalink to &quot;界面元素&quot;">​</a></h1><p>本页面介绍软件的用户界面元素，供读者参考，以便于阅读后续使用说明。</p><p>目前本软件主要实现了以下界面：</p><ul><li>登录页面</li><li>主页面</li><li>阅读器</li><li>推送页面</li><li>关于页面</li></ul><p>可通过点击导航栏中的链接，或界面中的相应按钮，进入相应页面。<br> 以下是各个页面的界面元素介绍。</p><h2 id="工具栏" tabindex="-1">工具栏 <a class="header-anchor" href="#工具栏" aria-label="Permalink to &quot;工具栏&quot;">​</a></h2><p>工具栏是所有页面中的通用元素， 在工具栏左侧包含设置和返回/退出登陆按钮， 右侧是页面导航。 例如，下图是主界面中的工具栏：</p><p><img class="lires-manual-screenshot" style="width:100%;" src="https://limengxun-imagebed.oss-cn-wuhan-lr.aliyuncs.com/pic/lires-toolbar-dark-v1.7.3.png" alt="lires-toolbar"></p><h2 id="数据卡片" tabindex="-1">数据卡片 <a class="header-anchor" href="#数据卡片" aria-label="Permalink to &quot;数据卡片&quot;">​</a></h2><p>数据卡片（Data Card）是Lires的数据条目展示形式，是主页中的数据内容，也是其他页面中的可编辑数据展示形式。 以下为一张数据卡片： <img class="lires-manual-screenshot" style="width:100%;" src="https://limengxun-imagebed.oss-cn-wuhan-lr.aliyuncs.com/pic/lires-datacard-dark-v1.3.0.png" alt="lires-datacard"></p><p>数据卡片包含了文献标题和作者的基本信息以及操作按钮：</p><ul><li>阅读器（Reader）：点击<code>Reader</code>按钮，可以打开该阅读器对文献信息阅读，同时记录笔记。</li><li>链接（Link）：点击<code>Link</code>按钮，可以在新窗口打开文献链接，当文献没有URL字段时不显示。</li><li>概览（Summary）：点击<code>Summary</code>按钮，可以显示文献的详细信息，尝试使用AI进行总结。</li><li>引用（Cite）：点击<code>Cite</code>按钮，可以显示数种引用格式，点击即可复制。</li><li>操作（Actions）：点击<code>Actions</code>按钮，可以展开操作菜单，包含了编辑条目信息、添加和删除文档、 以及删除条目等操作。</li></ul><p>通过点击<code>Actions</code>和<code>Abstract</code>按钮，可将数据卡片完全展开如下： <img class="lires-manual-screenshot" style="width:100%;" src="https://limengxun-imagebed.oss-cn-wuhan-lr.aliyuncs.com/pic/lires-datacardExpand-dark-v1.3.0.png" alt="lires-datacardExpand"></p><p>摘要（Abstract）处用于填入文献的摘要信息，点击摘要正文部分即可进行编辑，当编辑完成后自动保存。</p><p>概览（Summary）界面中展示了包括全部作者、期刊、数据大小等详细信息，尝试使用AI进行自动总结， 并基于语义搜索展示文献库中所有最相关文献。下图是概览界面的展示： <img class="lires-manual-screenshot" style="width:100%;" src="https://limengxun-imagebed.oss-cn-wuhan-lr.aliyuncs.com/pic/lires-datacardSummary-dark-v1.3.0.png" alt="lires-datacardSummary"></p><p>若文献库中有同名作者，会在作者名后面标注数字，点击数字即可展开作者的其他条目数据卡片。</p><hr><div class="info custom-block"><p class="custom-block-title">INFO</p><p>待完善</p></div>',18),r=[t];function c(n,o,d,p,m,u){return i(),e("div",null,r)}const b=a(s,[["render",c]]);export{_ as __pageData,b as default};
