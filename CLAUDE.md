# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **documentation and template repository** for a YouTube training course focused on product specification and Jira dashboard development. It contains comprehensive guides for writing user stories, acceptance criteria, test cases, and feature specifications using spec-driven development methodologies.

**Core Purpose**: Provide structured templates and reference documentation for teaching agile product development workflows, particularly in the context of building a Jira Dashboard MVP.

**適用對象**: 本指南是給 Claude Code AI agent 用來開發此教學專案的指導文件。

### 在開始任何任務之前

- **保持獨立判斷**: 基於技術事實和最佳實踐做決策,不因用戶語氣或期望而改變立場
- **直接溝通**: 避免過度禮貌或模糊表達,直接說明問題和建議
- **承認不確定性**: 遇到不確定的情況時,明確說明並提出討論方案,而非猜測
- **挑戰假設**: 如果發現需求或方法有問題,主動提出質疑和替代方案

#### 技術決策原則

- **優先查閱文檔**: 使用 Context7 工具或其他資源獲取最新文檔,確保引導內容不過時
- **spec-driven**: 嚴格基於現有 PRD 和規格文件工作,不自行擴充需求
  
#### 協作模式

- **解釋決策**: 說明技術選擇的理由,不只是提供答案
- **記錄重要決策**: 主動建議應該記錄到文檔的重要討論點

#### Git 操作規則

- **永遠不要主動發動 git 指令**: 等待用戶發號施令，所有 git 操作必須由用戶明確要求
  - ❌ 不可：修改檔案後自動執行 `git add` 和 `git commit`
  - ✅ 可以：用戶明確說「git commit」時，才執行 git 操作
  - ✅ 可以：詢問用戶「要推送到 GitHub 嗎？」，然後等待指示

- **Commit 訊息使用台灣繁體中文**: 所有 git commit 訊息必須使用繁體中文
  - 第一行：簡潔的中文摘要（命令式，例如「修正 Windows 兼容性問題」）
  - 空行
  - 詳細說明：用中文列舉主要變更
  - 最後：Co-Authored-By 簽名

#### 語言和溝通

- **使用台灣繁體中文溝通**: 與用戶對話時必須使用繁體中文
- **代碼註解**: 遵循既有檔案的慣例
- **直接溝通風格**: 避免過度禮貌，直接說明問題和建議

#### 代碼質量要求

- **測試案例優先**: 實作前先撰寫測試案例供人工審查,以測試案例界定實作範圍和驗收標準
- **清晰命名**: 使用描述性變量和函數名稱
- **最小改動**: 每次修改範圍盡可能小且專注

## Repository Structure

```
training-pm-ai-flow/
├── docs/
│   ├── assets/                      # Demo images
│   ├── reference/                   # Reference documentation
│   │   ├── PRD.md                   # Product Requirements Document
│   │   ├── step0-painpoint-ref.md
│   │   ├── step1-painpoints-analysis.md
│   │   ├── step2-ost-v1-all.md
│   │   ├── step2-ost-v2-focus.md
│   │   ├── step3-userstory-v1.md
│   │   ├── step5-ac-scope-change-waterfall-v1.md
│   │   ├── step6-prd.md
│   │   └── CLAUDE-md-myRule.md
│   ├── template/                    # Reusable templates & prompts
│   │   ├── feature-spec-template-v2.md
│   │   ├── acceptance-criteria-guide.md
│   │   ├── prototype-guide.md
│   │   ├── gemini-gem-PM-1-painpoint-analysis-prompts.md
│   │   ├── gemini-gem-PM-2-ost-prompts.md
│   │   └── gemini-gem-PM-3-userstory-prompts.md
│   ├── prototype/                   # Prototype examples
│   ├── chat-note/                   # Development notes
│   ├── tech-overview.md
│   └── table-schema.md
```

## Key Concepts

### Documentation Language
- **Primary Language**: Traditional Chinese (繁體中文) for all documentation
- **Code Comments**: Follow the conventions in existing files
- **Communication Style**: Direct, objective, action-oriented (避免過度禮貌或模糊表達)

### Spec-Driven Development Workflow

This repository teaches a structured workflow:

1. **User Story** → Define user needs and value
2. **Acceptance Criteria** → Specify testable scenarios using Gherkin format
3. **Test Cases** → Generate detailed test steps from AC
4. **Implementation** → Develop based on validated specifications

### Reference Product: Jira Dashboard MVP v1.0

The templates reference a real product example:
- **Tech Stack**: Next.js 15, React 19, Python/FastAPI backend, Google Sheets integration
- **Data Architecture**: Strict 23-column rawData schema (A:W) with fixed field order
- **Core Features**: 4 metric cards + 1 status distribution bar chart + Sprint filter
- **Development Constraint**: 在嚴格資料 schema 限制下，快速迭代開發

## Working with Templates

### Feature Spec Template (`docs/template/feature-spec-template-v2.md`)

When creating new feature specifications:
- Use the structured format: 功能概述 → 用戶故事 → Acceptance Criteria → 產品規格
- Include Mermaid flowcharts for complex business logic
- Ensure each section links properly to acceptance criteria guide

### Acceptance Criteria Guide (`docs/template/acceptance-criteria-guide.md`)

Writing standards:
- Use **Gherkin format**: Given-When-Then structure
- Cover scenarios: ✅ Normal flow, ⚠️ Boundary conditions, ❌ Error cases, 🔒 Security controls
- Each AC must be directly testable and measurable
- Maintain 1:1 mapping with User Stories

### Prompt Templates for AI Assistants

Reference PM-focused prompt templates:
- `gemini-gem-PM-1-painpoint-analysis-prompts.md` - Pain point discovery
- `gemini-gem-PM-2-ost-prompts.md` - Opportunity sizing template
- `gemini-gem-PM-3-userstory-prompts.md` - User story generation

## Data Architecture (Reference)

The repository documents a strict data schema for the reference Jira Dashboard:

### rawData Table (23 columns, A:W)
- **Strict Access Pattern**: Use `row[index]` (0-22) for field access
- **Key Fields**: Key(0), Issue Type(1), Status(5), Sprint(6), Story Points(15)
- **Status Values**: Fixed 9 statuses in order: Backlog → Evaluated → To Do → In Progress → Waiting → Ready to Verify → Done → Invalid → Routine
- **Constraint**: Cannot add, delete, or rearrange columns

### GetJiraSprintValues Table (9 columns, A:I)
- **Purpose**: Provide Sprint filter options
- **Key Field**: Sprint Name (Column C) used for filtering rawData

## Important Conventions

### When Creating Documentation
- Avoid generic development practices that are obvious
- Do not list every file or component (easily discovered through exploration)
- Focus on "big picture" architecture requiring multiple file reads to understand
- Include specific technical constraints and business logic rules

### When Assisting with Specifications
- Encourage exploration of user roles and real needs
- Guide thinking: What pain point does this solve? What value does it bring?
- Reference the guides (user-story-guide.md, acceptance-criteria-guide.md) for examples
- Ensure specifications are testable and measurable

## Reference Documents

Critical context for understanding the product domain:
- **PRD.md** (`docs/reference/PRD.md`): Complete product requirements for Jira Dashboard MVP v1.0
- **Step-by-step workflow** (`docs/reference/step*.md`): PM development workflow from pain point analysis to PRD
- **tech-overview.md**: Technical architecture, tech stack, deployment configuration
- **table-schema.md**: Detailed data schema with field definitions and access patterns
- **CLAUDE-md-myRule.md** (`docs/reference/`): Additional AI interaction guidelines

