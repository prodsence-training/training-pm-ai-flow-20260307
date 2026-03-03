'use client'

/**
 * 📚 動態路由 Prototype 索引頁面
 *
 * ⚠️ 教學設計 ONLY — 請勿複製到職場專案
 *
 * 本結構為了課堂示範方便而設計，讓學員能在一個文件中看到多個 prototype。
 *
 * 在實際職場專案中，應該根據貴公司的 repository 規則：
 * - 可能是各自獨立的子資料夾：prototype/pacing-bar/, prototype/dashboard-integrated/ 等
 * - 可能是獨立的 feature branch 或單獨的 repo
 * - 可能有特定的命名和組織規則
 *
 * 學員應該在職場中遵循團隊的約定，而不是複製本課程的結構。
 *
 * 路由列表：
 * - /prototype/pacing-bar → Pacing Bar Prototype
 * - /prototype/[新功能] → 學員創建的新 prototype
 */

import { useState } from 'react'

// ──────────────────────────────────────────────
// Pacing Bar 型別和假資料
// ──────────────────────────────────────────────

type AssigneeKey = 'team' | 'andy' | 'bob'

interface SprintData {
  label: string
  description: string
  sprintName: string
  totalDays: number
  elapsedDays: number
  team: { totalSP: number; doneSP: number }
  andy: { totalSP: number; doneSP: number }
  bob: { totalSP: number; doneSP: number }
  hasActiveSprint: boolean
}

type ScenarioKey = 'normal' | 'warning' | 'ahead' | 'zero_sp' | 'no_sprint'

const SCENARIOS: Record<ScenarioKey, SprintData> = {
  normal: {
    label: '✅ 正常（綠色）',
    description: '團隊落後少於 15%，進度條保持綠色',
    sprintName: 'Sprint 12',
    totalDays: 10,
    elapsedDays: 5,
    team: { totalSP: 50, doneSP: 20 },
    andy: { totalSP: 25, doneSP: 11 },
    bob: { totalSP: 25, doneSP: 9 },
    hasActiveSprint: true,
  },
  warning: {
    label: '🔴 預警（紅色）',
    description: '團隊落後超過 15%（理想進度 - 實際進度 > 15%），進度條轉紅',
    sprintName: 'Sprint 12',
    totalDays: 10,
    elapsedDays: 7,
    team: { totalSP: 50, doneSP: 20 },
    andy: { totalSP: 25, doneSP: 8 },
    bob: { totalSP: 25, doneSP: 12 },
    hasActiveSprint: true,
  },
  ahead: {
    label: '🚀 超前（綠色）',
    description: '實際進度超過理想進度，進度條保持綠色',
    sprintName: 'Sprint 12',
    totalDays: 10,
    elapsedDays: 4,
    team: { totalSP: 50, doneSP: 30 },
    andy: { totalSP: 25, doneSP: 16 },
    bob: { totalSP: 25, doneSP: 14 },
    hasActiveSprint: true,
  },
  zero_sp: {
    label: '⚪ 邊界：總 SP = 0',
    description: 'AC05：Sprint 總 Story Points 為零，實際進度顯示 0%，不計算落後比例',
    sprintName: 'Sprint 13（空 SP）',
    totalDays: 10,
    elapsedDays: 3,
    team: { totalSP: 0, doneSP: 0 },
    andy: { totalSP: 0, doneSP: 0 },
    bob: { totalSP: 0, doneSP: 0 },
    hasActiveSprint: true,
  },
  no_sprint: {
    label: '⬜ 無 Active Sprint',
    description: 'AC06：無 Active Sprint 時，進度條區域隱藏不顯示',
    sprintName: '（無）',
    totalDays: 0,
    elapsedDays: 0,
    team: { totalSP: 0, doneSP: 0 },
    andy: { totalSP: 0, doneSP: 0 },
    bob: { totalSP: 0, doneSP: 0 },
    hasActiveSprint: false,
  },
}

// ──────────────────────────────────────────────
// Pacing Bar 計算邏輯
// ──────────────────────────────────────────────

function calcProgress(data: SprintData, assignee: AssigneeKey) {
  const source = data[assignee]
  const idealPct =
    data.totalDays > 0 ? (data.elapsedDays / data.totalDays) * 100 : 0
  const actualPct =
    source.totalSP > 0 ? (source.doneSP / source.totalSP) * 100 : 0
  const gap = idealPct - actualPct
  const isWarning = source.totalSP > 0 && gap > 15
  const isZeroSP = source.totalSP === 0
  return { idealPct, actualPct, gap, isWarning, isZeroSP }
}

// ──────────────────────────────────────────────
// 共用 Sub-components
// ──────────────────────────────────────────────

function ProgressBar({
  pct,
  color,
  label,
  sublabel,
}: {
  pct: number
  color: string
  label: string
  sublabel?: string
}) {
  return (
    <div className="mb-3">
      <div className="flex justify-between items-center mb-1">
        <span className="text-sm font-medium text-gray-700">{label}</span>
        <span className={`text-sm font-bold ${color === 'blue' ? 'text-blue-600' : color === 'green' ? 'text-green-600' : 'text-red-600'}`}>
          {pct.toFixed(1)}%
          {sublabel && <span className="ml-1 font-normal text-gray-500">{sublabel}</span>}
        </span>
      </div>
      <div className="w-full h-5 bg-gray-200 rounded-full overflow-hidden relative">
        <div
          className={`h-full rounded-full transition-all duration-500 ${color === 'blue'
              ? 'bg-blue-400'
              : color === 'green'
                ? 'bg-green-500'
                : 'bg-red-500'
            }`}
          style={{ width: `${Math.min(pct, 100)}%` }}
        />
      </div>
    </div>
  )
}

function ACBadge({ id, label }: { id: string; label: string }) {
  return (
    <span className="inline-flex items-center gap-1 bg-blue-50 text-blue-700 text-xs font-medium px-2 py-0.5 rounded border border-blue-200">
      <span className="font-mono">{id}</span>
      <span className="text-blue-400">·</span>
      {label}
    </span>
  )
}

// ──────────────────────────────────────────────
// Pacing Bar Prototype Component
// ──────────────────────────────────────────────

function PacingBarPrototype() {
  const [scenario, setScenario] = useState<ScenarioKey>('normal')
  const [assignee, setAssignee] = useState<AssigneeKey>('team')

  const data = SCENARIOS[scenario]
  const { idealPct, actualPct, gap, isWarning, isZeroSP } = calcProgress(data, assignee)

  const actualColor = isWarning ? 'red' : 'green'
  const source = data[assignee]

  return (
    <main className="min-h-screen bg-gray-50">
      {/* ── Header ── */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-3xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-800">
              Sprint 健康度視覺化 · The Pacing Bar
            </h1>
            <p className="text-sm text-gray-500 mt-0.5">
              SPEC-001 Story 1 · Prototype（Direct Mode）
            </p>
          </div>
          <span className="bg-amber-100 text-amber-800 text-xs font-semibold px-3 py-1 rounded-full border border-amber-300">
            ⚠️ Prototype — 請勿 commit
          </span>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-6 py-6 space-y-5">
        {/* ── 控制列 ── */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* 場景切換 */}
            <div>
              <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">
                測試場景
              </label>
              <select
                id="scenario-select"
                className="w-full text-sm border border-gray-300 rounded-md px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={scenario}
                onChange={(e) => setScenario(e.target.value as ScenarioKey)}
              >
                {(Object.entries(SCENARIOS) as [ScenarioKey, SprintData][]).map(([key, val]) => (
                  <option key={key} value={key}>{val.label}</option>
                ))}
              </select>
            </div>
            {/* Assignee 切換 */}
            <div>
              <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">
                視角（AC04）
              </label>
              <div className="flex gap-2">
                {(['team', 'andy', 'bob'] as AssigneeKey[]).map((a) => (
                  <button
                    key={a}
                    id={`assignee-${a}`}
                    onClick={() => setAssignee(a)}
                    className={`flex-1 text-sm rounded-md py-2 font-medium border transition-colors ${assignee === a
                        ? 'bg-blue-600 text-white border-blue-600'
                        : 'bg-white text-gray-600 border-gray-300 hover:border-blue-400 hover:text-blue-600'
                      }`}
                  >
                    {a === 'team' ? '全隊' : a.charAt(0).toUpperCase() + a.slice(1)}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* 場景說明 */}
          <div className="mt-3 bg-blue-50 border border-blue-100 rounded-md px-3 py-2 text-sm text-blue-700">
            <span className="font-medium">場景說明：</span>{data.description}
          </div>
        </div>

        {/* ── 雙重進度條主區塊（或 AC06 隱藏狀態） ── */}
        {!data.hasActiveSprint ? (
          /* AC06：無 Active Sprint */
          <div className="bg-white rounded-lg shadow-sm border border-dashed border-gray-300 p-8 text-center">
            <div className="text-4xl mb-3">🏁</div>
            <p className="text-gray-500 text-sm font-medium">目前無 Active Sprint</p>
            <p className="text-gray-400 text-xs mt-1">進度條區域隱藏，不顯示（AC06）</p>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-5">
            {/* 標題列 */}
            <div className="flex items-start justify-between mb-4">
              <div>
                <h2 className="text-base font-bold text-gray-800 flex items-center gap-2">
                  Sprint 雙重進度條 · Pacing Bar
                  {isWarning && (
                    <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full font-semibold animate-pulse">
                      ⚠️ 落後預警
                    </span>
                  )}
                </h2>
                <p className="text-xs text-gray-400 mt-0.5">
                  {data.sprintName}　·　已過 {data.elapsedDays}/{data.totalDays} 工作天（排除週末，AC07）
                </p>
              </div>
              {/* SP 數字 */}
              <div className="text-right">
                <p className="text-xs text-gray-400">
                  {assignee === 'team' ? '全隊' : assignee === 'andy' ? 'Andy' : 'Bob'} Story Points
                </p>
                <p className="text-lg font-bold text-gray-700">
                  {source.doneSP}
                  <span className="text-sm font-normal text-gray-400"> / {source.totalSP} SP</span>
                </p>
              </div>
            </div>

            {/* 進度條 pair */}
            {isZeroSP ? (
              /* AC05：總 SP = 0 */
              <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4 text-center">
                <p className="text-yellow-700 text-sm font-medium">總 Story Points 為 0</p>
                <p className="text-yellow-600 text-xs mt-1">
                  AC05：實際進度顯示 0%，不計算落後比例
                </p>
                <div className="mt-3">
                  <ProgressBar pct={0} color="blue" label="理想進度（時間基礎）" />
                  <ProgressBar pct={0} color="green" label="實際完成進度（Done SP）" />
                </div>
              </div>
            ) : (
              <>
                <ProgressBar
                  pct={idealPct}
                  color="blue"
                  label="① 理想進度（時間基礎）"
                  sublabel={`第 ${data.elapsedDays} 天 / 共 ${data.totalDays} 天`}
                />
                <ProgressBar
                  pct={actualPct}
                  color={actualColor}
                  label={`② 實際完成進度（Done SP）${isWarning ? ' — 落後超過 15%，亮紅色警示（AC02/AC03）' : ''}`}
                  sublabel={`Done ${source.doneSP} / 總 ${source.totalSP} SP`}
                />

                {/* 落後比例顯示 */}
                <div className={`mt-3 rounded-md px-4 py-2 text-sm font-medium flex items-center justify-between
                  ${isWarning ? 'bg-red-50 border border-red-200 text-red-700' : 'bg-green-50 border border-green-200 text-green-700'}`}>
                  <span>
                    {gap > 0 ? `落後 ${gap.toFixed(1)}%` : gap < 0 ? `超前 ${Math.abs(gap).toFixed(1)}%` : '持平'}
                    {isWarning && '　→　超過 15% 閾值，觸發紅色警示'}
                    {!isWarning && gap <= 0 && '　→　超前或持平，保持綠色'}
                    {!isWarning && gap > 0 && '　→　落後但未超過 15% 閾值，保持綠色'}
                  </span>
                  <span className={`text-lg ${isWarning ? 'text-red-500' : 'text-green-500'}`}>
                    {isWarning ? '🔴' : '🟢'}
                  </span>
                </div>
              </>
            )}
          </div>
        )}

        {/* ── AC 對照表 ── */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <h3 className="text-sm font-semibold text-gray-600 mb-3">這個 Prototype 覆蓋的 AC</h3>
          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <ACBadge id="AC01" label="雙重進度條正常顯示" />
              <span className="text-gray-400 text-xs">理想進度 vs 實際完成比例並排</span>
            </div>
            <div className="flex items-center gap-2">
              <ACBadge id="AC02" label="落後未超閾值 → 綠色" />
              <ACBadge id="AC03" label="落後 &gt;15% → 紅色" />
            </div>
            <div className="flex items-center gap-2">
              <ACBadge id="AC04" label="Assignee 切換" />
              <span className="text-gray-400 text-xs">全隊 / Andy / Bob 三種個人視角</span>
            </div>
            <div className="flex items-center gap-2">
              <ACBadge id="AC05" label="總 SP=0 → 顯示 0%，不計落後" />
            </div>
            <div className="flex items-center gap-2">
              <ACBadge id="AC06" label="無 Active Sprint → 隱藏" />
            </div>
            <div className="flex items-center gap-2">
              <ACBadge id="AC07" label="理想進度排除週末" />
              <span className="text-gray-400 text-xs">工作天數已在假資料中排除週末計算</span>
            </div>
          </div>
        </div>

        {/* ── 操作說明 ── */}
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 text-sm text-amber-800">
          <h3 className="font-semibold mb-2">操作說明（供技術對齊）</h3>
          <ol className="list-decimal list-inside space-y-1 text-xs">
            <li>上方「測試場景」下拉，切換 5 種 AC 覆蓋情境</li>
            <li>「視角」按鈕切換全隊 / Andy / Bob 個人進度（AC04）</li>
            <li>「無 Active Sprint」場景驗證進度條區域整體隱藏（AC06）</li>
            <li>「邊界：總 SP=0」場景驗證 0% 顯示且無落後計算（AC05）</li>
          </ol>
          <p className="mt-2 text-amber-700 font-medium text-xs">
            ⚠️ 完成截圖後請執行 <code className="bg-amber-100 px-1 rounded">git checkout frontend/src/app/prototype/</code> 還原
          </p>
        </div>

        <p className="text-center text-xs text-gray-400 pb-4">
          此為 Prototype 頁面，使用 hardcode 假資料 · 完全隔離於 Production 邏輯
        </p>
      </div>
    </main>
  )
}

// ──────────────────────────────────────────────
// 404 頁面
// ──────────────────────────────────────────────

function NotFoundPrototype({ slug }: { slug: string }) {
  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center px-6">
        <div className="text-6xl mb-4">🤔</div>
        <h1 className="text-2xl font-bold text-gray-800 mb-2">
          找不到 Prototype: <code className="text-red-600">/{slug}</code>
        </h1>
        <p className="text-gray-600 mb-6">
          目前只有以下 prototype：
        </p>
        <ul className="text-left inline-block bg-white rounded-lg shadow p-6 space-y-2">
          <li className="text-gray-700">
            ✅ <a href="/prototype/pacing-bar" className="text-blue-600 hover:underline">
              /prototype/pacing-bar
            </a> — Pacing Bar（進度條雙重預警）
          </li>
          <li className="text-gray-500 text-sm">
            （學員應在此基礎上創建新的 prototype）
          </li>
        </ul>
        <p className="text-gray-400 text-xs mt-6">
          要新增 prototype，在此檔案加上條件即可
        </p>
      </div>
    </main>
  )
}

// ──────────────────────────────────────────────
// 主頁面：根據 slug 動態渲染
// ──────────────────────────────────────────────

export default function PrototypePage({ params }: { params: { slug: string } }) {
  const { slug } = params

  // 動態路由映射（教學用）
  switch (slug) {
    case 'pacing-bar':
      return <PacingBarPrototype />

    // ⬇️ 學員：在此添加新的 prototype
    // case 'your-feature-name':
    //   return <YourFeaturePrototype />

    default:
      return <NotFoundPrototype slug={slug} />
  }
}

// ──────────────────────────────────────────────────────────────────────────
// 📖 學員：如何新增新的 Prototype
// ──────────────────────────────────────────────────────────────────────────
/*

## 完整步驟：

### 步驟 1️⃣ 在此檔案頂部創建你的 Prototype 組件

根據 PRD 和 AC，在文件頂部（在 PrototypePage 之前）創建你的組件：

```tsx
// ── 你的新 Prototype ──
function YourFeaturePrototype() {
  const [state, setState] = useState('')

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-6 py-6">
        <h1 className="text-2xl font-bold mb-6">Your Feature Name</h1>
        // 根據 PRD 開發你的 UI
      </div>
    </main>
  )
}
```

### 步驟 2️⃣ 在上方 switch 語句中添加 case 映射

找到 PrototypePage 中的 switch 語句，取消註釋並修改：

```tsx
switch (slug) {
  case 'pacing-bar':
    return <PacingBarPrototype />

  case 'your-feature-name':      // ← 改成你的功能名稱（kebab-case）
    return <YourFeaturePrototype />  // ← 改成你的組件名稱

  default:
    return <NotFoundPrototype slug={slug} />
}
```

### 步驟 3️⃣ 訪問你的 Prototype

在瀏覽器打開：
http://localhost:3000/prototype/your-feature-name

### 步驟 4️⃣ 測試完後還原

```bash
git checkout frontend/src/app/prototype/
```

---

## ✅ 檢查清單

- [ ] 在此檔案創建 Prototype 組件（不新建資料夾）
- [ ] 在 switch 語句中添加 case 映射
- [ ] 路由名稱使用 kebab-case（如 dashboard-integrated, sprint-filter 等）
- [ ] 組件名稱使用 PascalCase（如 DashboardIntegrated, SprintFilter 等）
- [ ] 添加 'use client' directive（如果使用 React hooks）
- [ ] 根據 PRD 和 AC 開發功能
- [ ] 測試路由正常訪問
- [ ] 完成後 git checkout 還原

---

## 📍 更多資訊

詳見 frontend/src/app/prototype/README.md

*/
