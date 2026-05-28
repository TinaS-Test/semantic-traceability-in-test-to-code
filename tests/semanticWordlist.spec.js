import { test, expect } from '@playwright/test';
import { SearchPage } from '../SearchPage';
import fs from 'fs';

let searchPage;

test.beforeEach(async ({ page }) => {
    const wordlist = JSON.parse(fs.readFileSync('./wordlist.json', 'utf-8'));

    await page.route('**/wordlist.json', route => {
        route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify(wordlist)
        });
    });
    
    searchPage = new SearchPage(page);
    await page.goto('/semantic-wordlist.html');
});

test('Verify the page title to be Semantisk ordlista', async ({ page }) => {
    await expect(page).toHaveTitle(/Semantisk ordlista/);
});

test ('Verify search returns correct result in historyList when user clicks searchButton', async ({ page }) => {
    await searchPage.searchFor('Hantera');
    await expect(searchPage.historyItems.first().toHaveText('Hantera'));
});

test('Prevent access to wordlist from malicious search input', async ({ page }) => {
    await searchPage.searchFor('@@10XSS<x>');
    await expect(searchPage.errorMessage).toBeVisible();
    await expect(searchPage.errorMessage).toHaveText
    ('Inga matchande händelser funna i loggen.');
});

test('Assert history-list store the first and last search words', async ({ page }) => {
    for (const word of ['Hantera', 'Skydd', 'Förhindra', 'Generera', 'Fullständig']) {
        await searchPage.searchFor(word);
    }

    await expect(searchPage.historyItems).first().toHaveText('Fullständig');
    await expect(searchPage.historyItems).last().toHaveText('Hantera');
});