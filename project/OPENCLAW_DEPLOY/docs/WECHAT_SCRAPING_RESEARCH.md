# 微信公众号爬取方案调研报告

**调研时间**：2026-04-07  
**调研人**：AI雷达站 agent  
**结论**：微信公号直接爬取在现网环境不可行，但存在高质量替代方案

---

## 一、测试过的方案及结果

### 方案A：搜狗微信搜索 → follow 跳转链接
| 步骤 | 结果 | 说明 |
|------|------|------|
| 搜索结果页 (`weixin.sogou.com`) | ✅ 可访问 | 返回标题/公众号名/日期 |
| follow 跳转链接 | ❌ antispider 拦截 | Sogou 返回 302→301→反爬虫页面 |

**根因**：搜狗对 `/link?url=...` 跳转目标做了人机校验，程序访问一律拦截。

---

### 方案B：直接 `mp.weixin.qq.com` URL
| 结果 | 说明 |
|------|------|
| ❌ 不可行 | 微信文章 URL 含加密 token（`__biz`、`mid`、`sn`），无法预测 |

微信文章永久链接格式为 `https://mp.weixin.qq.com/s/xxxxxxxxxxxxx`，其中 `xxxxxxxxxxxxx` 无法通过公开接口生成。

---

### 方案C：`wechatsogou` 库
| 状态 | 说明 |
|------|------|
| ⚠️ pip 安装超时 | PyPI 网络访问超时（`files.pythonhosted.org`） |
| 待手动安装验证 | 库本身基于搜狗搜索，理论上能解析真实 mp.weixin.qq.com URL |

**结论**：需先解决 pip 安装问题，或通过其他方式安装 wechatsogou。

---

### 方案D：Playwright / 浏览器自动化
| 状态 | 说明 |
|------|------|
| ⚠️ 待验证 | scrapling 底层已用 Playwright，但 Sogou 反爬可能识别并拦截无头浏览器特征 |

---

## 二、推荐替代方案：苏商银行研究院 (sif.suning.com)

### 为什么选这个平台

1. **内容质量高**：以薛洪言（星图金融研究院副院长）为例，2023-11 至 2024-06 共 20+ 篇专栏，主题覆盖 A 股分析、银行板块、存款利率等，**与对公雷达站高度相关**
2. **完全可访问**：无需登录，无反爬，scrapling 200 OK
3. **已有入口**：当前 `analyst_sources.json` 中「薛洪言」(`analyst-deposit-002`) 的 profile URL (`sif.suning.com/author/detail/8002`) 已经存在
4. **文章列表可枚举**：profile 页含完整历史文章列表，可直接提取 URL

### 实测数据

| 指标 | 数值 |
|------|------|
| profile 页面 | 200 OK，68KB HTML |
| 文章列表页 | 200 OK，9 篇/页 |
| 文章正文页 | 200 OK，1466 字干货，107 行 |
| 页面稳定性 | ✅ 长期稳定，无反爬 |

### 文章示例（薛洪言，2024-06-18）
> 今年以来，银行板块表现很强。1-5月，申万银行指数累计上涨19.41%……历史是一面镜子。在发掘未来之星之前，先看看过去十年银行股的表现。2013-2023年10年间，有数据的16家上市银行中，宁波银行、招商银行、南京银行累计涨幅靠前……

---

## 三、其他可访问平台（补充来源）

| 平台 | 可访问性 | 内容类型 | 备注 |
|------|---------|---------|------|
| 苏商银行研究院 (sif.suning.com) | ✅ 200 OK | 分析师专栏 | 已有入口，高度相关 |
| 东方财富网 (eastmoney.com) | ✅ 200 OK | 财经新闻/研报 | 需进一步验证内容结构 |
| 雪球 (xueqiu.com) | ✅ 200 OK | 投资者观点 | 搜索 API 需要认证 |
| 财新网 (caixin.com) | ❌ 跳 404 | 频道关闭 | 不可用 |

---

## 四、现有系统评估

**`fetch_analyst_articles.py` 现状**：
- ✅ 已能抓取 `sif.suning.com` profile 页面
- ✅ scrapling 升级已完成（0.2.99）
- ⚠️ profile 页文章链接已可发现，但需确认 fetch 逻辑是否正确解析

**`analyst_sources.json` 现有 8 个来源**：

| ID | 姓名 | 平台 | profile 可访问 |
|----|------|------|--------------|
| analyst-deposit-001 | 董希淼 | shifd.net | ✅ 200 OK |
| analyst-deposit-002 | 薛洪言 | sif.suning.com | ✅ 200 OK，文章丰富 |
| analyst-deposit-003 | 娄飞鹏 | chinapost.com.cn | ✅ 200 OK |
| analyst-deposit-004 | 连平 | saif.sjtu.edu.cn | ✅ 200 OK |
| analyst-deposit-005 | 周茂华 | jingpt.com | ✅ 200 OK |
| analyst-loan-001 | 温彬 | cfau.edu.cn | ✅ 200 OK |
| analyst-loan-002 | 曾刚 | shifd.net | ✅ 200 OK |
| analyst-overall-001 | 朱太辉 | nifd.cn | ❌ SSL 握手失败 |
| analyst-overall-002 | 孙扬 | sif.suning.com | ✅ 200 OK |

---

## 五、建议执行路径

### 短期（立即可做）

1. **修复 nifd.cn SSL 问题**：朱太辉来源需换 URL 或跳过
2. **确认 fetch_analyst_articles.py 能从 profile 页提取文章列表并抓取全文**（验证薛洪言 20 篇文章能被抓入 analyst_cache）
3. **补充其他分析师的 sif.suning.com 入口**（如孙扬已有）

### 中期（1-2周）

4. **在 `analyst_sources.json` 中补充高价值苏商银行分析师**（覆盖存款/贷款/整体对公三个维度）
5. **在 `fetch_analyst_articles.py` 中增加"从 profile 页自动发现文章列表"的功能**，覆盖 sif.suning.com 的翻页场景

### 长期（需要外部依赖）

6. **安装 wechatsogou**（解决 pip 超时问题后验证）→ 打通微信公众号直接内容
7. **调研 Playwright 绕过 antispider 的可行性**

---

## 六、关键待确认问题

| 问题 | 优先级 | 说明 |
|------|--------|------|
| pip 安装 wechatsogou 超时 | P1 | 网络问题，需找安装源 |
| nifd.cn SSL 失败 | P2 | 朱太辉来源无法抓取 |
| fetch 脚本是否完整解析 profile 文章列表 | P2 | 需跑一次 dry-run 验证 |
| scrapling 在 sif.suning.com 上是否能保持长期稳定 | P2 | 需监控 |
