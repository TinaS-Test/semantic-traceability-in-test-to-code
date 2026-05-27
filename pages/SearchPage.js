export class SearchPage {
    constructor(page) {
        this.page = page;
        this.searchInput = page.locator('#search-input');
        this.searchButton = page.locator('#btn-search');
        this.errorMessage = page.locator('#error-banner');
        this.resultItems = page.locator('#results-container tbody tr');
        this.historyItems = page.locator('#history-list li');
    }

    async searchFor(term) {
    await this.searchInput.fill(term);
    await this.searchButton.click();
    }

    async getResultCount() {
    return await this.resultItems.count();
    }

    async triggerRapidSearches(term, times) {
        await this.searchInput.fill(term);
        for (let i = 0; i < times; i++) {
            await this.searchButton.click();
        }
    }

    async getVisibleErrorMessage() {
        return await this.errorMessage.textContent();
    }
}