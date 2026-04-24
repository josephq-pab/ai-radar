# FRONTEND_SHARED_BLOCK_SPEC_V1.md

## 文档信息

- **版本**：V1
- **阶段**：PHASE5-1（STAGE257）
- **日期**：2026-04-24
- **前提**：PHASE4_BASELINE_FREEZE_NOTE（Phase 4 基线已冻结，不得回退）

---

## 一、共性 Block 定义原则

以下 Block 在十页中以相同或高度相似的方式出现，视为**共性 Block**。

共性 Block 必须满足：
1. 标题口径统一
2. 职责边界清晰
3. 出现位置可预测
4. 不得被页面本地内容降级或替换

---

## 二、Block-01：首屏判定区（SHARED-FIRST-SCREEN）

### 2.1 职责
回答四问：
1. 现在有没有事
2. 值不值得继续读
3. 当前最重要的结论是什么
4. 下一眼该看哪里

### 2.2 标准标题
`🎯 首屏判定（P4-5）`

### 2.3 标准结构

```html
<!-- P4-5 首屏判定区 -->
<div style="background:linear-gradient(135deg,#0f2747 0%,#1a3a6b 100%);color:#fff;padding:18px 22px;border-radius:8px;margin-bottom:16px;font-size:13px;">
  <div style="font-weight:700;font-size:14px;margin-bottom:10px;display:flex;align-items:center;gap:8px;">
    🎯 首屏判定（P4-5）
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
    <!-- 四问内容 -->
  </div>
</div>
```

### 2.4 四问标准措辞

| 问题 | 标准措辞 | 适用模板 |
|------|---------|---------|
| 现在有没有事 | 现在有没有事 | 全部 |
| 值不值得继续读 | 值不值得继续读 | 全部 |
| 最重要结论 | 当前最重要的结论是什么 | 全部 |
| 下一眼看哪 | 下一眼该看哪里 | 全部 |

### 2.5 出现条件
- **所有十页均必备**，不得省略，不得折叠，不得移入 details

### 2.6 推荐顺序
页面最顶部，`<div class="main">` 之前

### 2.7 组件候选
✅ **适合抽象为组件**：首屏判定区的 2×2 结构、四问措辞、标题格式均高度统一，可抽象为 `FirstScreenJudge` 组件。

---

## 三、Block-02：Footer Navigation（SHARED-FOOTER-NAV）

### 3.1 职责
提供十页间的导航能力。

### 3.2 标准标题
`七页导航：` 或 `十页导航：`

### 3.3 标准结构

**七页版**（主链路页）：
```html
<div style="background:#fafafa;border-top:1px solid #d9d9d9;padding:12px 16px;display:flex;align-items:center;gap:16px;font-size:13px;">
  <span style="color:#595959;font-weight:600;">七页导航：</span>
  <a href="radar-home.html">首页</a>
  <a href="config-status.html">配置</a>
  <a href="single-chain-ops.html">运营</a>
  <a href="ops-evidence.html">证据</a>
  <a href="ops-decision.html">决策</a>
  <a href="ops-playbook.html">流程</a>
  <a href="ops-routes.html" style="font-weight:600;">路径</a>
</div>
```

**十页版**（首页/支援页）：
全部10个页面链接。

### 3.4 出现条件
- 首页和支援页：十页导航
- 主链路/决策/快报/证据/配置：七页导航
- 支援页（routes/glossary/registry）：可选

### 3.5 组件候选
✅ **适合抽象为组件**：`FooterNav` 组件，接受 `mode:7|10` 参数。

---

## 四、Block-03：P4-6 治理折叠区（SHARED-GOVERNANCE-FOLD）

### 4.1 职责
收纳 L5 背景补充、P3 历史治理说明，防止治理噪音干扰主阅读流。

### 4.2 标准标题
`🔽 P4-6 治理折叠区（模块说明、句子规范、维护索引 — 维护人员按需展开）`

### 4.3 标准结构

```html
<!-- P4-6 治理折叠区（L5，维护用，按需展开） -->
<details style="margin:16px 0;">
<summary style="cursor:pointer;padding:8px 12px;background:#f5f5f5;border:1px solid #d9d9d9;border-radius:6px;font-size:12px;color:#8c8c8c;font-weight:600;list-style:none;">
🔽 P4-6 治理折叠区（模块说明、句子规范、维护索引 — 维护人员按需展开）
</summary>

<!-- P3-41/42/43/44 治理内容 -->
</details>
```

### 4.4 出现条件
- **所有十页均必备**，位于页面底部，`</body>` 之前

### 4.5 组件候选
✅ **适合抽象为组件**：`GovernanceFold` 组件，统一收纳 P3-41/42/43/44 内容。

---

## 五、Block-04：Page Meta（SHARED-META）

### 5.1 职责
提供页面版本、角色、快照属性等元信息。

### 5.2 标准结构

```html
<div class="meta-label">版本标识</div>
<div class="meta-value">P4-6 · v1.0</div>
```

### 5.3 出现条件
- 所有十页均位于页面顶部 header 区

### 5.4 组件候选
✅ **适合抽象为组件**：`PageMeta` 组件，接受 `version`、`role` 参数。

---

## 六、Block-05：停止条件区（SHARED-STOP-CONDITION）

### 6.1 职责
明确告知用户在什么条件下可以停止当前页面阅读。

### 6.2 标准标题
在首屏判定区内标注：`✅ [条件满足] 即可停止`

### 6.3 标准结构（主链路/决策类）

```
判断已完成 → [执行/等待/升级] 结论已给出 → 即可停止
```

### 6.4 标准结构（支援页）

```
查到[对象] → [确认动作] → 即可返回
```

### 6.5 出现条件
- 主链路/决策/快报/证据/配置：**必备**
- 支援页：出现在首屏判定区和 footer 内

### 6.6 组件候选
⚠️ **部分适合抽象**：停止语口径（"即可停止/即可返回"）可抽象，但具体条件因页面而异，适合保留为模板参数。

---

## 七、Block-06：支援页定位区（SHARED-SUPPORT-LOCATION）

### 7.1 职责
向用户说明当前页是支援页，找到答案即返回，不承载延伸任务。

### 7.2 标准标题
`✅ 支援页定位`

### 7.3 标准结构

```html
<div style="padding:6px 10px;background:#ffe7ba;border-radius:4px;font-size:11px;color:#d46b08;">
  ✅ <strong>支援页定位：</strong>支援页，找到答案即返回。不承载延伸任务，不变成独立中心。
</div>
```

### 7.4 出现条件
- **仅支援页（routes/glossary/registry/config）必备**
- 主链路/首页不得出现

### 7.5 组件候选
✅ **适合抽象为组件**：`SupportLocationBanner` 组件。

---

## 八、Block-07：当前动作/路径区（SHARED-ACTION）

### 8.1 职责
告知用户当前应执行的动作或页面间的跳转路径。

### 8.2 标准标题
因页面而异，无统一标题，但格式统一为：`[动作标签] → [目标页面/结论]`

### 8.3 出现条件
- 主链路/决策/快报/证据页：**L2 必备**
- 首页/支援页：无

### 8.4 组件候选
⚠️ **不适合抽象**：动作内容因页面差异大，适合保留为模板内语义。

---

## 九、共性 Block 汇总矩阵

| Block | 代码 | 适用模板 | 出现条件 | 组件候选 |
|-------|------|---------|---------|---------|
| 首屏判定区 | SHARED-FIRST-SCREEN | 全部十页 | 必备 | ✅ FirstScreenJudge |
| Footer Navigation | SHARED-FOOTER-NAV | 全部 | 必备（七/十页）| ✅ FooterNav(mode) |
| 治理折叠区 | SHARED-GOVERNANCE-FOLD | 全部十页 | 必备 | ✅ GovernanceFold |
| Page Meta | SHARED-META | 全部十页 | 必备 | ✅ PageMeta |
| 停止条件 | SHARED-STOP-CONDITION | 主链路/决策/支援 | 必备 | ⚠️ 部分抽象 |
| 支援页定位 | SHARED-SUPPORT-LOCATION | 支援页 | 支援页必备 | ✅ SupportLocationBanner |
| 当前动作区 | SHARED-ACTION | 主链路/决策/快报 | L2 必备 | ⚠️ 不适合抽象 |

---

## 十、Block 优先级规则

共性 Block 的 L1~L5 层级归属：

| Block | 默认层级 | 说明 |
|-------|---------|------|
| SHARED-FIRST-SCREEN | L0（页面入口）| 页面最顶部，不可降级 |
| SHARED-META | L0（页面入口）| 页面顶部 |
| SHARED-ACTION | L2 | 默认展开，不可折叠 |
| SHARED-STOP-CONDITION | L2 | 首屏判定区内，默认可见 |
| SHARED-FOOTER-NAV | L4 | 页面底部导航 |
| SHARED-SUPPORT-LOCATION | L2（支援页）| 首屏判定区附近 |
| SHARED-GOVERNANCE-FOLD | L5 | 强制折叠至 details |
