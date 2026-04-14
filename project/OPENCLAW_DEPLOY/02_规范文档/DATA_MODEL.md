# 对公 AI 雷达站数据模型 v0.1

## 1. 设计原则

数据模型既要支持原始信息保留，也要支持观点加工、人工确认、报告输出和后续复盘升级。

## 2. 核心实体

### 2.1 SourceItem（原始信息项）

字段建议：
- id
- sourceType（peer / policy / industry / internal_upload）
- sourceName
- sourceFile
- sourceSheet
- title
- rawContent
- observedAt
- importedAt
- confidenceLevel
- tags
- metadata

### 2.2 AnalysisCandidate（分析候选项）

字段建议：
- id
- sourceItemId
- businessArea（overall / deposit / loan）
- impactTarget（product / industry / pricing / competition / strategy）
- importanceLevel
- timelinessLevel
- relevanceScore
- candidateStatus
- initialReason

### 2.3 InsightDraft（观点草稿）

字段建议：
- id
- candidateId
- factSummary
- businessMeaning
- impactAnalysis
- preliminaryJudgment
- strategySuggestion
- actionSuggestion
- evidenceFor
- evidenceAgainst
- uncertaintyNotes
- modelInfo
- createdAt

### 2.4 HumanReview（人工确认记录）

字段建议：
- id
- insightDraftId
- reviewer
- reviewDecision
- editedConclusion
- editedSuggestion
- modificationType
- modificationReason
- approvedAt

### 2.5 ReportIssue（报告版本）

字段建议：
- id
- reportType（weekly / special）
- reportTitle
- reportScope
- reportPeriod
- keyInsights
- status
- finalReviewer
- finalizedAt
- exportFormat

### 2.6 PreferenceFeedback（偏好反馈）

字段建议：
- id
- targetType
- targetId
- roleType
- expectedStyle
- dissatisfactionPoint
- desiredAddition
- feedbackAt

## 3. 首期数据输入模型

### 3.1 同业对标数据

预期覆盖：
- 存款余额
- 年日均
- 同业对比指标

### 3.2 贷款对标数据

预期覆盖：
- 贷款余额或投放相关对标口径
- 股份行之间的贷款比较

### 3.3 贷款利率数据

预期覆盖：
- 产品或口径维度的利率信息
- 时间维度对比
- 行内外对比

## 4. 后续扩展方向

- InternalMetric（内部经营指标）
- CompetitorAction（同业动作事件）
- PolicyImpact（政策影响映射）
- IndustryTheme（行业主题）
- ReportTemplate（报告模板）
- ModelVersion（模型与规则版本）
