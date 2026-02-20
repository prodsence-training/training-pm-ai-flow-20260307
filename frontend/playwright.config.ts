import { defineConfig, devices } from '@playwright/test'

/**
 * Playwright E2E Test Configuration
 * 用於測試 Jira Dashboard MVP v1.0
 */
export default defineConfig({
  testDir: './e2e',

  // 測試超時設定
  timeout: 30 * 1000, // 30 seconds per test
  expect: {
    timeout: 5000, // 5 seconds for assertions
  },

  // 失敗時重試次數
  retries: process.env.CI ? 2 : 0,

  // 並行執行設定
  workers: process.env.CI ? 1 : undefined,

  // Reporter
  reporter: [
    ['html'],
    ['list'],
  ],

  // 共享設定
  use: {
    // Base URL
    baseURL: 'http://localhost:3000',

    // 截圖設定
    screenshot: 'only-on-failure',

    // 錄影設定
    video: 'retain-on-failure',

    // Trace 設定
    trace: 'on-first-retry',
  },

  // 測試專案配置
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    // 可選：其他瀏覽器
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },
  ],

  // Web Server 設定（自動啟動開發伺服器）
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000, // 2 minutes
  },
})
