#parametrizace pro hodnoty titul (text), checkbox (pro vyhledávání v originálních názvech), 
#kategorie (dropdown menu), nakladatelstvi (autocomplete), vysledek (vnitřní text výsledného objektu)
parametry_vyhledavani = [
    ("hjvkjvgkv", False, "", "", None),                                     #neexistující titul
    ("", False, "", "", None),                                              #prázdné hledání
    ("fellowship of the ring", False, "Fantasy", "", None),                 #vyhledávání bez výsledku
    ("fellowship of the ring", True, "Fantasy", "", "Společenstvo prstenu"),#vyhledávání i v originálních názvech   
    ("return of the king", True, "", "Mladá Fronta", "Návrat krále"),       #vyhledávání podle nakladatelství
    ("", False, "Biografie", "Bonaventura", "Života běh s knihou"),         #vyhledávání bez názvu knihy
    ("", True, "Biografie", "Bonaventura", "Života běh s knihou"),          #vyhledávání bez názvu knihy i v originálních názvech
    ("Vango", False, "", "Baobab", "Vango"),                                #vyhledávání bez kategorie
    ("Murtagh", False, "", "", "Murtagh"),                                  #vyhledávání jen podle názvu, bez dalších filtrů
    ("Zlodějka knih", False, "Válečné", "Argo", "Zlodějka knih"),           #vyhledávání se všemi parametry
    ("zlodejka knih", False, "Válečné", "Argo", "Zlodějka knih"),           #vyhledávání bez diakritiky
]