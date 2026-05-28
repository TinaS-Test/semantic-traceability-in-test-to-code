import { test, expect } from '@playwright/test';
import { PageObjects } from '../pageObjects/page-objects.js';

test.beforeEach(async ({ page }) => {
    const wordlist = JSON.parse(fs.readFileSync('./wordlist.json', 'utf-8'));

    await page.route('**/wordlist.json', route => {
        route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify(wordlist)
        });
    });
    await page.goto('http://127.0.0.1:8000/semantic-wordlist.html');
});

test('Verify the page title to be Semantisk ordlista', async ({ page}) => {
    const searchPage = new SearchPage(page);
    await page.goto('http://127.0.0.1:8000/semantic-wordlist.html')

    await expect(page).toHaveTitle(/Semantisk ordlista/);
});

test ('Verify search returns correct result in historyList when user clicks searchButton', async ({ page }) => {
    const searchPage = new SearchPage(page);
    await page.goto('http://127.0.0.1:8000/semantic-wordlist.html');

    await page.searchInput.fill('Hantera');
    await page.searchButton.click();

    await expect(page.locator('#history-list li').first()).toHaveText('hantera');
});

test('Prevent access to wordlist from malicious search input', async ({ page }) => {
    const searchPage = new SearchPage(page);
    await page.goto('http://127.0.0.1:8000/semantic-wordlist.html');

    await page.searchInput.fill('@@10XSS<x>');
    await page.searchButton.click();

    await expect(page.locator('#error-banner')).toBeVisible();
    await expect(page.locator('#error-banner')).toHaveText
    ('Inga matchande händelser funna i loggen.');
});

test('Assert history-list store the first and last search words', async ({ page }) => {
    const searchPage = new SearchPage(page);
    await page.goto('http://127.0.0.1:8000/semantic-wordlist.html');

    for (const word of ['Hantera', 'Skydd', 'Förhindra', 'Generera', 'Fullständig']) {
        await page.searchPage.searchFor(word);
    }

    await expect(page.historyItems('#history-list li').first()).toHaveText('Fullständig');
    await expect(page.historyItems('#history-list li').last()).toHaveText('Hantera');
});