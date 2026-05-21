import { test, expect } from '@playwright/test';
import { SearchPage } from '../pages/SearchPage';

test('System serves queries from local storage without new API calls', async ({ page }) => {
  const searchPage = new SearchPage(page);
  const commonSearchTerm = "Lavender Soap"; 

  // Navigerar till målsidan
  await page.goto('https://fictitious-test-site.com');

  // Sökning 1: Normal sökning över nätverket
  await searchPage.searchFor(commonSearchTerm);
  await page.waitForResponse('**/api/search');

  // Verifierar att datan har sparats i Local Storage
  const isCached = await page.evaluate(() => {
    return window.localStorage.getItem('search_cache') !== null;
  });
  expect(isCached).toBeTruthy();

  // Bryter nätverksuppkopplingen för sök-API:et
  await page.route('**/api/search', route => route.abort());

  // Sökning 2: Identisk sökning som ska hämtas från cache
  await searchPage.searchFor(commonSearchTerm);

  // Verifierar att resultaten fortfarande visas trots strypt nätverk
  const resultCount = await searchPage.getResultCount();
  expect(resultCount).toBeGreaterThan(0);
});