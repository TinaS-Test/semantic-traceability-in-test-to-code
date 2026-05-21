import { test, expect } from '@playwright/test';
import { SearchPage } from '../pages/SearchPage';

test('System neutralizes input and returns 200 OK with zero results', async ({ page }) => {
  const searchPage = new SearchPage(page);
  const testPayload = "<script>alert('XSS')</script> OR 1=1 --";

  // Förbereder avlyssning av API-svaret (Validerar HTTP 200)
  const responsePromise = page.waitForResponse(response => 
    response.url().includes('/api/search')
  );

  // Navigerar till målsidan
  await page.goto('https://fictitious-test-site.com');
  
  // Matar in skadlig kod i sökfältet
  await searchPage.searchFor(testPayload);
  const response = await responsePromise;

  // Verifierar att servern hanterar anropet utan att krascha
  expect(response.status()).toBe(200);

  // Verifierar att systemet returnerar noll träffar
  const resultCount = await searchPage.getResultCount();
  expect(resultCount).toBe(0);
});