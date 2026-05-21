// ============================================================
// Test Category  : UI / Functional
// Requirement(s) : Doc 1 – FR2.1 (HTML page), FR2.2 (source input),
//                  FR2.3 (translation output), FR2.4 (submit button)
// Tool           : Playwright (JavaScript)
// ============================================================

const { test, expect } = require("@playwright/test");

const APP_URL = "https://tina.ethernettrip.com";

// Renamed from generic "submit" to "translate_submit_button" in data-testid.
// Recommendation: add these data-testid attributes to templates/index.html.
const SELECTORS = {
  sourceTextInput:       '[data-testid="source-text-input"]',      // FR2.2
  translationOutput:     '[data-testid="translation-output"]',     // FR2.3
  translateSubmitButton: '[data-testid="translate-submit-button"]' // FR2.4
};

test.describe("FR2 – Translation Interface Elements", () => {

  test.beforeEach(async ({ page }) => {
    // Login required to access the interface (FR1.2 dependency)
    await page.goto(`${APP_URL}/login`);
    await page.fill('[data-testid="email-input"]', "qa_test_user@example.com");
    await page.fill('[data-testid="password-input"]', "QaSecure!2024");
    await page.click('[data-testid="login-button"]');
    await page.waitForURL(`${APP_URL}/`);
  });

  test("test_translation_ui_elements_present", async ({ page }) => {
    /**
     * Verifies all required UI elements from FR2 are visible and interactive.
     * FR2.1: The page itself must load (implicit in page.goto succeeding).
     * FR2.2: Source text input field must be visible.
     * FR2.3: Translation output field must be visible.
     * FR2.4: Translate submit button must be visible and enabled.
     */

    // FR2.2 – Source text input
    await expect(page.locator(SELECTORS.sourceTextInput)).toBeVisible();

    // FR2.3 – Translation output field
    await expect(page.locator(SELECTORS.translationOutput)).toBeVisible();

    // FR2.4 – Translate submit button — must be enabled, not just present
    const submitButton = page.locator(SELECTORS.translateSubmitButton);
    await expect(submitButton).toBeVisible();
    await expect(submitButton).toBeEnabled();
  });

});