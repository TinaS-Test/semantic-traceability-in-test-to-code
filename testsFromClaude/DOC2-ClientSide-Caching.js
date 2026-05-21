// ============================================================
// Test Category  : Performance / Browser
// Requirement(s) : Doc 2 – Ch 2.1 (local cache must reduce redundant requests)
// Tool           : Playwright (JavaScript)
// ============================================================

const { test, expect } = require("@playwright/test");

const APP_URL = "https://tina.ethernettrip.com";

// "Redundant requests" replaces "unnecessary requests" ("onödiga anrop").
// Redundant is technically precise: the same request with the same expected result.
const REPEATED_INPUT_TEXT = "Hur mår du?";
const CACHE_STORAGE_KEY = "translation_cache"; // Expected localStorage key name

test.describe("Doc2 Ch2.1 – Client-side Cache Reduces Redundant Requests", () => {

  test.beforeEach(async ({ page }) => {
    await page.goto(`${APP_URL}/login`);
    await page.fill('[data-testid="email-input"]', "qa_test_user@example.com");
    await page.fill('[data-testid="password-input"]', "QaSecure!2024");
    await page.click('[data-testid="login-button"]');
    await page.waitForURL(`${APP_URL}/`);
  });

  test("test_local_cache_reduces_redundant_requests", async ({ page }) => {
    /**
     * Doc 2, Ch 2.1: After the first translation, the result must be cached locally.
     * A second identical request must not trigger a new /translate network call.
     *
     * Step 1: Submit translation — expect 1 network request.
     * Step 2: Clear the output, re-submit the same text — expect 0 network requests.
     * Step 3: Verify the cache entry exists in localStorage.
     */
    const translateRequests = [];

    // Intercept network requests to /translate
    page.on("request", (req) => {
      if (req.url().includes("/translate") && req.method() === "POST") {
        translateRequests.push(req.url());
      }
    });

    // Step 1: First translation — must hit the server
    await page.fill('[data-testid="source-text-input"]', REPEATED_INPUT_TEXT);
    await page.click('[data-testid="translate-submit-button"]');
    await page.waitForSelector('[data-testid="translation-output"]:not(:empty)');

    expect(translateRequests.length).toBe(1); // One real request expected

    // Step 2: Clear and re-submit the same text — must use cache
    translateRequests.length = 0; // Reset interceptor counter
    await page.fill('[data-testid="source-text-input"]', "");
    await page.fill('[data-testid="source-text-input"]', REPEATED_INPUT_TEXT);
    await page.click('[data-testid="translate-submit-button"]');
    await page.waitForSelector('[data-testid="translation-output"]:not(:empty)');

    expect(translateRequests.length).toBe(0); // Zero redundant requests expected

    // Step 3: Verify localStorage contains the cache entry
    const cacheEntry = await page.evaluate((key) => {
      return localStorage.getItem(key);
    }, CACHE_STORAGE_KEY);

    expect(cacheEntry).not.toBeNull();

    const parsed = JSON.parse(cacheEntry);
    expect(parsed).toHaveProperty(REPEATED_INPUT_TEXT);
  });

});