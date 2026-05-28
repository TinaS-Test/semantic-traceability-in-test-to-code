class PageObjects {
    constructor(page) {
        //Locators
        this.searchInput        = page.locator('#search-input');
        this.searchButton       = page.locator('#btn-search');
        this.errorMessage       = page.locator('#error-banner');
        this.resultsContainer   = page.locator('#results-container');
        this.resultsTable       = page.locator('#results-container table');
        this.tableHeaders       = page.locator('#results-container thead th');
        this.resultItems        = page.locator('#results-container tbody tr');
        this.historyList        = page.locator('#history-list');
        this.historyItems       = page.locator('#history-list li');
        this.wordClassTags      = page.locator('.tag');
        this.codeHighTrace      = page.locator('td code');

        //Methods
        page.goto(url);
        page.locator(selector).fill(value);
        page.locator(selector).click();
        page.locator(selector).first();
        page.locator(selector).last();
        page.locator(selector).count();
        page.locator(selector).textContent();

        //Assertions
        expect(page).toHaveTitle(title);
        expect(page.locator(selector)).toHaveText(text);
        expect(page.locator(selector)).toBeVisible();
        expect(page.locator(selector)).toHaveCount(n);
        expect(page.locator(selector)).toBeHidden();
    }

}