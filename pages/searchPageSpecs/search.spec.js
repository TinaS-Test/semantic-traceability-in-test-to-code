import { test, expect } from '@playwright/test';
import {SearchPage} from './SearchPage.js';

test('Verify semantic search from local HTML-layer', async ({ page }) => {
    await page.goto('localhost:8080/semantic-layer.html');
    const searchPage = new SearchPage(page);
    await searchPage.searchFor('Security');
});