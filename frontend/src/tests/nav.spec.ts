import { test, expect } from '@playwright/test'
test('Login', async ({ page }) => {
    await page.goto('/login')
    await expect(page).toHaveURL(/login/i)

})

test('Portfolio', async ({ page }) => {
    await page.goto('/portfolio')
    await expect(page).toHaveURL(/portfolio/i)
})

test('Stocks', async ({ page }) => {
    await page.goto('/stocks')
    await expect(page).toHaveURL(/stocks/i)
})

test('stock details', async ({ page }) => {
    await page.goto('/stocks/TSLA')
    await expect(page).toHaveURL(/stocks\/TSLA/i)
})

test('Register', async ({ page }) => {
    await page.goto('/register')
    await expect(page).toHaveURL(/register/i)
})

test('Leaderboard', async ({ page }) => {
    await page.goto('/leaderboard')
    await expect(page).toHaveURL(/leaderboard/i)
})