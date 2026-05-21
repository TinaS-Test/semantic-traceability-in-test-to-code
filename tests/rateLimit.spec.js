import { test, expect } from '@playwright/test';
import { SearchPage } from '../pages/SearchPage';
// --- GENERERAD AV GEMINI ---
// Krav 3.1: API och pålitlighet - Överbelastningsskydd
// Krav 3.1.1: Max 10 anrop per 5 sekunder
// Krav 3.1.2: HTTP 429 vid överträdelse
// Krav 3.1.3: Användargränssnittet visar felmeddelande
test('System blocks more than 10 requests with HTTP 429', async ({page}) => {
    const searchPage = new SearchPage(page);
    let received429Error = false;

    //Lyssnar efter svar från API i bakgrunden (Validerar Krav 3.1.2)
    page.on('response', response => {
        if (response.url().includes('/api/search') && response.status() === 429) {
            received429Error = true;
        }
    });

    //Navigera till påhittad sida
    await page.goto('https://a-made-up-page.com');

    //Klicka snabbt 11 gånger (Triggar Krav 3.1.1)
    await searchPage.triggerRapidSearches(11);

    //Verifierar nätverkskravet (Validerar Krav 3.1.2)
    expect(received429Error).toBeTruthy();

    //Verifiera UI-kravet (Validerar Krav 3.1.3)
    const errorText = await searchPage.getVisibleErrorMessage();
    expect(errorText).toContain('wait');
});
