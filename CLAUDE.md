# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **documentation and template repository** for a YouTube training course focused on product specification and Jira dashboard development. It contains comprehensive guides for writing user stories, acceptance criteria, test cases, and feature specifications using spec-driven development methodologies.

**Core Purpose**: Provide structured templates and reference documentation for teaching agile product development workflows, particularly in the context of building a Jira Dashboard MVP.

### 在開始任何任務之前

- **保持獨立判斷**: 基於技術事實和最佳實踐做決策,不因用戶語氣或期望而改變立場
- **直接溝通**: 避免過度禮貌或模糊表達,直接說明問題和建議
- **承認不確定性**: 遇到不確定的情況時,明確說明並提出討論方案,而非猜測
- **挑戰假設**: 如果發現需求或方法有問題,主動提出質疑和替代方案

#### 技術決策原則

- **優先查閱文檔**: 使用 Context7 工具獲取 React/Python 最新文檔,避免過時建議
- **spec-driven**: 嚴格基於現有 PRD 和規格文件工作,不自行擴充需求
  
#### 協作模式

- **解釋決策**: 說明技術選擇的理由,不只是提供答案
- **記錄重要決策**: 主動建議應該記錄到文檔的重要討論點
- **永遠不要主動發動 git 指令**: 等待用戶發號施令，所有 git 操作必須由用戶明確要求
- **使用台灣繁體中文溝通**: 與用戶對話時必須使用繁體中文

#### 代碼質量要求

- **測試案例優先**: 實作前先撰寫測試案例供人工審查,以測試案例界定實作範圍和驗收標準
- **清晰命名**: 使用描述性變量和函數名稱
- **最小改動**: 每次修改範圍盡可能小且專注

## Repository Structure

```
training-youtube-spec-kit/
├── docs/
│   ├── assets/           # Demo images (sprint burndowns, progress charts)
│   ├── reference/        # Reference documentation
│   │   ├── PRD.md                      # Product Requirements Document
│   │   ├── painpoint1-progress.md      # Problem analysis: lack of progress awareness
│   │   ├── CLAUDE-md-myRule.md         # AI interaction guidelines
│   │   └── constitution-md-myRule.md   # Workspace conventions
│   ├── template/         # Reusable templates
│   │   ├── feature-spec-template.md    # Feature specification template
│   │   ├── user-story-guide.md         # User story writing guide
│   │   ├── acceptance-criteria-guide.md # AC writing guide (Gherkin format)
│   │   └── testcase-guide.md           # Test case generation guide
│   ├── tech-overview.md  # Technical architecture documentation
│   └── table-schema.md   # Google Sheets data schema (rawData, GetJiraSprintValues)
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
- **Development Constraint**: "Vibe Coding" approach with strict data schema limitations

## Working with Templates

### Feature Spec Template (`docs/template/feature-spec-template.md`)

When creating new feature specifications:
- Use the structured format: 功能概述 → 用戶故事 → Acceptance Criteria → 產品規格
- Include Mermaid flowcharts for complex business logic
- Ensure each section links properly to guides (user-story-guide.md, acceptance-criteria-guide.md)

### User Story Guide (`docs/template/user-story-guide.md`)

Key principles:
- Follow format: `作為 [角色]，我希望 [功能]，以便 [價值]`
- Must satisfy INVEST principles (especially V-Valuable and T-Testable)
- **Common Mistake**: Avoid putting "what" as "why" (e.g., "以便我有客戶名單" is wrong)
- **Correct Approach**: Clearly articulate the actual value or pain point being solved

### Acceptance Criteria Guide (`docs/template/acceptance-criteria-guide.md`)

Writing standards:
- Use **Gherkin format**: Given-When-Then structure
- Cover scenarios: ✅ Normal flow, ⚠️ Boundary conditions, ❌ Error cases, 🔒 Security controls
- Each AC must be directly testable and measurable
- Maintain 1:1 mapping with User Stories

### Test Case Guide (`docs/template/testcase-guide.md`)

Test case generation:
- Each AC scenario should map to at least one test case
- Include fields: Test ID, Objective, Related US/AC, Pre-conditions, Steps, Expected Results, Test Data, Type, Automation Level
- Consider automation feasibility (Unit/Integration/E2E)

## AI Interaction Guidelines

From `docs/reference/CLAUDE-md-myRule.md`:

### Before Starting Any Task
- **保持獨立判斷**: Base decisions on technical facts and best practices, not user tone
- **直接溝通**: Avoid excessive politeness or vague expressions
- **承認不確定性**: Explicitly state uncertainties and propose discussion
- **挑戰假設**: Proactively question problematic requirements and offer alternatives

### Technical Decision Principles
- **spec-driven**: Strictly base work on existing PRD and specification documents, do not expand requirements independently
- **測試案例優先**: Write test cases before implementation for human review

### Code Quality Requirements
- **清晰命名**: Use descriptive variable and function names
- **最小改動**: Keep each modification small and focused

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
- **PRD.md**: Complete product requirements for Jira Dashboard MVP v1.0
- **painpoint1-progress.md**: Deep analysis of the "lack of progress awareness" problem
- **tech-overview.md**: Technical architecture, tech stack, deployment configuration
- **table-schema.md**: Detailed data schema with field definitions and access patterns

## Language & Communication Standards

See `.specify/memory/constitution.md` **Output Standards** section for:
- Documentation language preference (Traditional Chinese)
- Code comment conventions
- Communication style (direct, objective, action-oriented)
