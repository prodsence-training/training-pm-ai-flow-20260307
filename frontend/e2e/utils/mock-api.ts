/**
 * Mock API utilities for E2E tests
 * 用於攔截 API 請求並返回測試資料
 */

import { Page, Route } from '@playwright/test'

export interface MockApiOptions {
  metrics?: any
  statusDistribution?: any
  sprints?: any
  delay?: number
}

/**
 * 設置 API mock responses
 */
export async function setupMockApi(page: Page, options: MockApiOptions = {}) {
  const { metrics, statusDistribution, sprints, delay = 0 } = options

  // Mock metrics endpoint
  if (metrics) {
    await page.route('**/api/dashboard/metrics*', async (route: Route) => {
      await new Promise(resolve => setTimeout(resolve, delay))
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(metrics),
      })
    })
  }

  // Mock status distribution endpoint
  if (statusDistribution) {
    await page.route('**/api/dashboard/status-distribution*', async (route: Route) => {
      await new Promise(resolve => setTimeout(resolve, delay))
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(statusDistribution),
      })
    })
  }

  // Mock sprints endpoint
  if (sprints) {
    await page.route('**/api/sprints*', async (route: Route) => {
      await new Promise(resolve => setTimeout(resolve, delay))
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(sprints),
      })
    })
  }
}

/**
 * 模擬 API 錯誤
 */
export async function setupApiError(page: Page, endpoint: string, statusCode: number = 500) {
  await page.route(`**${endpoint}*`, async (route: Route) => {
    await route.fulfill({
      status: statusCode,
      contentType: 'application/json',
      body: JSON.stringify({
        error: 'Internal Server Error',
        message: 'Failed to fetch data',
      }),
    })
  })
}

/**
 * 清除所有 API mocks
 */
export async function clearMockApi(page: Page) {
  await page.unroute('**/api/**')
}
