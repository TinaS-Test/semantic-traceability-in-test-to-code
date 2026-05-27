import { test, expect } from '@playwright/test';

test('Verify the page title to be Semantisk ordlista', async ({ page}) => {
    await page.goto('http://127.0.0.1:8000/semantic-wordlist.html')

    await expect(page).toHaveTitle(/Semantisk ordlista/);
});

test ('Verify search returns correct result in historyList when user clicks searchButton', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/semantic-wordlist.html');

    await page.searchInput.fill('Hantera');
    await page.searchButton.click();

    await expect(page.locator('#history-list li').first()).toHaveText('hantera');
});

test('Prevent access to wordlist from malicious search input', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/semantic-wordlist.html');

    await page.searchInput.fill('@@10XSS<x>');
    await page.searchButton.click();

    await expect(page.locator('#error-banner')).toBeVisible();
    await expect(page.locator('#error-banner')).toHaveText
    ('Inga matchande händelser funna i loggen.');
});

test('Assert history-list store the first and last search words', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/semantic-wordlist.html');

    await page.searchInput.fill('Hantera');
    await page.searchButton.click();
    await page.searchInput.fill('Skydd');
    await page.searchButton.click();
    await page.searchInput.fill('Förhindra');
    await page.searchButton.click();
    await page.searchInput.fill('Generera');
    await page.searchButton.click();
    await page.searchInput.fill('Fullständig');
    await page.searchButton.click();

    await expect(page.locator('#history-list li').first()).toHaveText('Fullständig');
    await expect(page.locator('#history-list li').last()).toHaveText('Hantera');
});

/*
Säkerhet
Validering -
Hantera
Omdirigera
Generera
Returnera -
Initiera
Lagra -
Rapport
Logg
Förhindra -
Åtkomst -
Otillgänglig
Ofullständig
Fullständig
*/