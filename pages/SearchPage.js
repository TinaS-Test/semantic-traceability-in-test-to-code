export class SearchPage {
    constructor(page) {
        this.page = page;
        this.searchbutton = page.locator('#btn-search');
        this.errorMessage = page.locator('#error-banner');
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