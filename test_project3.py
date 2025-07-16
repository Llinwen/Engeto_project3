import pytest
from playwright.sync_api import Page
from playwright.sync_api import expect
from test_project3_parametrize import parametry_vyhledavani

#test, zda stránka zobrazí chybovou hlášku při pokusu o přihlášení bez hesla
def test_prihlaseni_bez_hesla(page: Page):
    page.locator("div.login_box input#log_name").fill("uzivatel")
    page.locator("div.login_box input#log_pass").fill("")
    page.get_by_role("button", name="Přihlásit se").click()
 
    assert page.url == "https://www.cbdb.cz/prihlaseni", "Stránka se nepřesměrovala do přihlášení"
    page.wait_for_selector(".alert.alert-danger", timeout=5000)
    error_alert = page.locator(".alert.alert-danger")
    assert error_alert.is_visible(), "Chybová hláška se nezobrazila"

#test, zda se zobrazí přihlašovací pop-up okno při pokusu přidat komentář bez přihlášení
def test_zobrazeni_popup(page: Page):
    page.locator("div.index_header_search input.index_search_text").fill("ronja dcera loupeznika") 
    page.press("input.index_search_text", "Enter")
    assert page.url == "https://www.cbdb.cz/kniha-709-ronja-dcera-loupeznika-ronja-rovardotter"
    pridat_komentar=page.locator("input.login_trigger[value='Přidat komentář']")
    pridat_komentar.scroll_into_view_if_needed()            #firefox v headless režimu nemusí mít pridat_komentar ve viewportu
    expect(pridat_komentar).to_be_visible(timeout=10000)    #čekáme na viditelnost pro headless firefox
    expect(pridat_komentar).to_be_enabled()                 #čekáme až bude tlačítko aktivní 
    page.wait_for_timeout(200)                              #krátké čekání - zpomalení layoutu v headless režimu firefoxu
    pridat_komentar.hover()                                 #hover pro jistotu kvůli firefox
    pridat_komentar.click(force=True)                       #force=True kvůli firefox
    page.wait_for_timeout(200)                              #krátké čekání na vykreslení pro firefox
    popup_window = page.locator("body > div.login_area")
    expect(popup_window).to_be_visible(timeout=10000)
    assert popup_window.is_visible(), "Přihlašovací pop-up okno se nezobrazilo"

#test responzivity - v širokém režimu je vidět login box, search box, odkazy registrovat a přihlásit
#v úzkém režimu je vidět ikona vyhledávání
def test_responzivita(page: Page):
    login_box = page.locator(".login_box")
    search_box = page.locator("header .search_box")
    search_icon = page.locator("header .header_mobile_trigger_search")
    registrovat_link = page.locator(".header_wrapper .header_account_link[href='/registrace']")
    prihlasit_link = page.locator(".header_wrapper .header_account_link.login_trigger")
    #široký režim
    page.set_viewport_size({"width": 1920, "height":1080})
    page.wait_for_selector(".login_box")
    assert login_box.is_visible()
    assert search_box.is_visible()
    assert not search_icon.is_visible()
    assert registrovat_link.is_visible()
    assert prihlasit_link.is_visible()
    #úzký režim
    page.set_viewport_size({"width": 375, "height":812})
    page.wait_for_selector("header .header_mobile_trigger_search")
    assert not login_box.is_visible()
    assert not search_box.is_visible()
    assert search_icon.is_visible()
    assert not registrovat_link.is_visible()
    assert not prihlasit_link.is_visible()


#parametrizovaný test pokročilého vyhledávání
@pytest.mark.parametrize("titul, checkbox, kategorie, nakladatelstvi, vysledek", parametry_vyhledavani)
def test_pokrocile_vyhledavani(page: Page, titul, checkbox, kategorie, nakladatelstvi, vysledek):
    #přejít do pokročilého vyhledávání
    page.locator("body > div.header_wrapper > header > div > div.header_search_area > a").click() 
    #vyhledávání
    page.locator("#name").fill(titul)
    if checkbox:
        page.locator("input#orig").check()
    if kategorie:
        page.locator("#category_1").select_option(label=kategorie)
    if nakladatelstvi:
        page.locator("input.publishers_select_filter").fill(nakladatelstvi)
        vybrane_nakladatelstvi=page.locator(
            "div.publisher_select_items span:not([style*='display: none'])", 
            has_text=nakladatelstvi
            ).first
        vybrane_nakladatelstvi.scroll_into_view_if_needed()
        expect(vybrane_nakladatelstvi).to_be_visible(timeout=10000)
        vybrane_nakladatelstvi.click() 
    page.locator("#ok").click()
    nalezena_kniha=page.locator("#adv_search_results > tbody > tr > td.search_col2")
    if vysledek is None:
        assert page.locator("#adv_search_results > tbody > tr").count() == 0
    else:
        assert vysledek in nalezena_kniha.first.inner_text()
