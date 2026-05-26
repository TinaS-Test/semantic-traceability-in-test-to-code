export class SearchPage {
    constructor(page) {
        this.page = page;
        this.searchInput = page.locator('#search-input');
        this.searchButton = page.locator('#btn-search');
        this.errorMessage = page.locator('#error-banner');
        this.resultItems = page.locator('.search-result-item');
    }

    async searchFor(term) {
    await this.searchInput.fill(term);
    await this.searchButton.click();
    }

    async getResultCount() {
    return await this.resultItems.count();
    }

    async triggerRapidSearches(times) {
        for (let i = 0; i < times; i++) {
            await this.searchbutton.click();
        }
    }

    async getVisibleErrorMessage() {
        return await this.errorMessage.textContent();
    }
}