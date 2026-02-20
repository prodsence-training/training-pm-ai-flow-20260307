/**
 * E2E Tests for User Story 3: Sprint Filter
 * 對應 tasks.md T040-T047
 *
 * Test Cases:
 * - TC-FILTER-001: Display sprint filter dropdown
 * - TC-FILTER-002: Display sprint options from API
 * - TC-FILTER-003: Handle duplicate sprint names with Sprint ID
 * - TC-FILTER-004: Filter metrics when "All" selected
 * - TC-FILTER-005: Filter metrics by specific Sprint name
 * - TC-FILTER-006: Filter metrics by "No Sprints" option
 * - TC-FILTER-007: Update charts on sprint change
 * - TC-FILTER-008: Display "No Sprints" option always
 */

import { test, expect } from '@playwright/test'
import { setupMockApi } from './utils/mock-api'
import {
  mockMetricsBasic,
  mockMetricsSprint1,
  mockMetricsNoSprints,
  mockStatusDistributionBasic,
  mockStatusDistributionSprint1,
  mockStatusDistributionNoSprints,
  mockSprintsBasic,
  mockSprintsWithDuplicates,
  mockSprintsEmpty,
} from './fixtures/test-data'

test.describe('User Story 3: Sprint Filter', () => {
  test('TC-FILTER-001: Display sprint filter dropdown', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Verify sprint filter label
    await expect(page.getByText(/Sprint.*篩選/i)).toBeVisible()

    // Verify dropdown exists
    const sprintFilter = page.locator('select[id*="sprint"]')
      .or(page.locator('[role="combobox"]'))
      .or(page.getByLabel(/sprint/i))

    await expect(sprintFilter.first()).toBeVisible()
  })

  test('TC-FILTER-002: Display sprint options from API', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Find the sprint filter select
    const sprintSelect = page.locator('select').first()

    // Verify "All" option
    await expect(sprintSelect).toContainText('All')

    // Verify Sprint options
    await expect(sprintSelect).toContainText('Sprint 1')
    await expect(sprintSelect).toContainText('Sprint 2')
    await expect(sprintSelect).toContainText('Sprint 3')

    // Verify "No Sprints" option
    await expect(sprintSelect).toContainText('No Sprints')
  })

  test('TC-FILTER-003: Handle duplicate sprint names with Sprint ID', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsWithDuplicates,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    const sprintSelect = page.locator('select').first()

    // Verify duplicate sprint names have IDs appended
    await expect(sprintSelect).toContainText('Sprint 1 (11)')
    await expect(sprintSelect).toContainText('Sprint 1 (15)')

    // Verify unique sprint doesn't have ID
    await expect(sprintSelect).toContainText('Sprint 2')
  })

  test('TC-FILTER-004: Filter metrics when "All" selected (default)', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Verify default selection is "All"
    const sprintSelect = page.locator('select').first()
    await expect(sprintSelect).toHaveValue('All')

    // Verify metrics show all issues (10 from mockMetricsBasic)
    await expect(page.locator('text=/\\b10\\b/')).toBeVisible()
  })

  test('TC-FILTER-005: Filter metrics by specific Sprint name', async ({ page }) => {
    // Setup initial "All" data
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Verify initial state (All)
    await expect(page.getByText('10', { exact: true }).first()).toBeVisible()

    // Change API responses for Sprint 1
    await setupMockApi(page, {
      metrics: mockMetricsSprint1,
      statusDistribution: mockStatusDistributionSprint1,
      sprints: mockSprintsBasic,
    })

    // Select Sprint 1
    const sprintSelect = page.locator('select').first()
    await sprintSelect.selectOption('Sprint 1')

    // Wait for data to update
    await page.waitForTimeout(500)

    // Verify metrics updated (3 issues for Sprint 1)
    await expect(page.getByText('3', { exact: true }).first()).toBeVisible()
  })

  test('TC-FILTER-006: Filter metrics by "No Sprints" option', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Change API for "No Sprints"
    await setupMockApi(page, {
      metrics: mockMetricsNoSprints,
      statusDistribution: mockStatusDistributionNoSprints,
      sprints: mockSprintsBasic,
    })

    // Select "No Sprints"
    const sprintSelect = page.locator('select').first()
    await sprintSelect.selectOption('No Sprints')

    await page.waitForTimeout(500)

    // Verify filtered data (1 issue with no sprint)
    await expect(page.getByText('1', { exact: true }).nth(0)).toBeVisible()
  })

  test('TC-FILTER-007: Update charts on sprint change', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Record initial chart state
    const initialChart = await page.locator('text=/Status Distribution/i').isVisible()
    expect(initialChart).toBe(true)

    // Change sprint filter
    await setupMockApi(page, {
      metrics: mockMetricsSprint1,
      statusDistribution: mockStatusDistributionSprint1,
      sprints: mockSprintsBasic,
    })

    const sprintSelect = page.locator('select').first()
    await sprintSelect.selectOption('Sprint 1')

    await page.waitForTimeout(500)

    // Verify chart is still visible (updated, not removed)
    await expect(page.getByText(/Status Distribution/i)).toBeVisible()

    // Verify both metrics and chart updated together
    await expect(page.getByText('3', { exact: true }).first()).toBeVisible()
  })

  test('TC-FILTER-008: Display "No Sprints" option always available', async ({ page }) => {
    // Test with empty sprint data
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsEmpty,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    const sprintSelect = page.locator('select').first()

    // Even with no sprint data, should show "All" and "No Sprints"
    await expect(sprintSelect).toContainText('All')
    await expect(sprintSelect).toContainText('No Sprints')
  })

  test('TC-FILTER-SYNC: Metrics and chart update synchronously', async ({ page }) => {
    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Change to Sprint 1
    await setupMockApi(page, {
      metrics: mockMetricsSprint1,
      statusDistribution: mockStatusDistributionSprint1,
      sprints: mockSprintsBasic,
    })

    const sprintSelect = page.locator('select').first()
    await sprintSelect.selectOption('Sprint 1')

    await page.waitForTimeout(500)

    // Both metrics and chart total should match
    // mockMetricsSprint1 has 3 issues
    // mockStatusDistributionSprint1 total is also 3
    const metricValue = await page.locator('text=/\\b3\\b/').first().textContent()
    expect(metricValue).toContain('3')

    // Chart total should also be 3
    await expect(page.getByText(/Total Issues:/i).locator('..')).toContainText('3')
  })

  test('TC-FILTER-RESPONSIVE: Sprint filter works on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })

    await setupMockApi(page, {
      metrics: mockMetricsBasic,
      statusDistribution: mockStatusDistributionBasic,
      sprints: mockSprintsBasic,
    })

    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Verify sprint filter is visible and functional on mobile
    const sprintSelect = page.locator('select').first()
    await expect(sprintSelect).toBeVisible()

    // Change selection
    await setupMockApi(page, {
      metrics: mockMetricsSprint1,
      statusDistribution: mockStatusDistributionSprint1,
      sprints: mockSprintsBasic,
    })

    await sprintSelect.selectOption('Sprint 1')
    await page.waitForTimeout(500)

    // Verify data updated on mobile
    await expect(page.getByText('3', { exact: true }).first()).toBeVisible()
  })
})
