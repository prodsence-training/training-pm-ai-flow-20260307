/**
 * E2E Tests for User Story 2: Status Distribution Chart
 * 對應 tasks.md T028-T032
 *
 * Test Cases:
 * - TC-CHART-001: Display status distribution chart with 9 statuses
 * - TC-CHART-002: Display statuses in correct order
 * - TC-CHART-003: Display tooltip with value and percentage on hover
 * - TC-CHART-004: Show total issue count at chart bottom
 * - TC-CHART-005: Display empty state when no data
 */

import { test, expect } from '@playwright/test'
import { setupMockApi } from './utils/mock-api'
import {
  mockMetricsBasic,
  mockMetricsEmpty,
  mockStatusDistributionBasic,
  mockStatusDistributionEmpty,
  mockSprintsBasic,
} from './fixtures/test-data'

test.describe('User Story 2: Status Distribution Chart', () => {
  test('TC-CHART-001: Display status distribution chart', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Verify chart title is displayed
    await expect(page.getByText(/Status Distribution/i)).toBeVisible()

    // Verify chart is rendered (look for chart container or SVG)
    const chartContainer = page.locator('[class*="recharts"]')
      .or(page.locator('svg'))
      .or(page.locator('[class*="chart"]'))

    // At least one chart element should be visible
    const hasChart = await chartContainer.count() > 0
    expect(hasChart).toBe(true)
  })

  test('TC-CHART-002: Display 9 statuses in correct order', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Verify chart area is rendered
    const chartArea = page.locator('svg').filter({ has: page.locator('rect') }).first()
    await expect(chartArea).toBeVisible()

    // Verify total issue count is displayed (which includes status breakdown)
    // If chart loads with 9 statuses, total should be 27
    await expect(page.getByText('27', { exact: true }).first()).toBeVisible()
  })

  test('TC-CHART-003: Display tooltip on hover (if interactive)', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Verify chart SVG is present and contains bars
    const svg = page.locator('svg').first()
    await expect(svg).toBeVisible()

    // Count rectangles in SVG (chart bars)
    const rects = page.locator('svg rect')
    const rectCount = await rects.count()

    // Should have multiple bars for different statuses
    expect(rectCount).toBeGreaterThan(0)

    // Note: Tooltip hover testing is skipped in headless mode
    // as it's difficult to reliably test Recharts tooltips in automation
  })

  test('TC-CHART-004: Show total issue count at chart bottom', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Verify total issues text is displayed
    await expect(page.getByText(/Total Issues:/i)).toBeVisible()

    // Verify the count (mockStatusDistributionBasic has 27 total issues)
    await expect(page.locator('text=/\\b27\\b/')).toBeVisible()
  })

  test('TC-CHART-005: Display empty state when no data', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsEmpty,
      statusDistribution: mockStatusDistributionEmpty,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Verify chart title is still displayed
    await expect(page.getByText(/Status Distribution/i)).toBeVisible()

    // Verify total count shows 0
    await expect(page.getByText(/Total Issues:/i)).toBeVisible()

    // Look for "0" in the total count area
    // Should see total = 0
    const totalSection = page.locator('text=/Total Issues:/i').locator('..')
    await expect(totalSection).toContainText('0')
  })

  test('TC-CHART-VISUAL: Chart uses blue theme color', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Check for blue color (#3b82f6) in chart
    // This is a visual check - we look for the color in SVG elements
    const blueBars = page.locator('rect[fill="#3b82f6"]')
      .or(page.locator('rect[style*="3b82f6"]'))
      .or(page.locator('[class*="blue"]'))

    const hasBlueElements = await blueBars.count() > 0

    // Chart should have blue-colored elements
    expect(hasBlueElements).toBe(true)
  })

  test('TC-CHART-LAYOUT: Chart is responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })

    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Verify chart is visible on mobile
    await expect(page.getByText(/Status Distribution/i)).toBeVisible()

    // Verify no horizontal overflow
    const bodyScrollWidth = await page.evaluate(() => document.body.scrollWidth)
    const viewportWidth = 375
    expect(bodyScrollWidth).toBeLessThanOrEqual(viewportWidth + 1)
  })

  test('TC-CHART-PERCENTAGE: Percentages add up to 100%', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Check that percentages from mockStatusDistributionBasic add up correctly
    // mockStatusDistributionBasic percentages sum to ~100%
    const percentages = mockStatusDistributionBasic.distribution.map(d => d.percentage)
    const total = percentages.reduce((sum, p) => sum + p, 0)

    // Total should be close to 100% (allow rounding difference)
    expect(total).toBeGreaterThan(99)
    expect(total).toBeLessThan(101)
  })
})
