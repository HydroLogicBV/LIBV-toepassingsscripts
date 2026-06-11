# -*- coding: utf-8 -*-


def validate_settings(STARTDATUM, EINDDATUM, DIR_SECRETS):
    
    # Controleert of de instellingen geldig zijn voordat de download start
    if EINDDATUM < STARTDATUM:
        raise ValueError("EINDDATUM moet op of na STARTDATUM liggen.")
 
    aantal_dagen = (EINDDATUM - STARTDATUM).days + 1
    if aantal_dagen > 30:
        print(
            f"\n  ⚠️  Waarschuwing: je vraagt {aantal_dagen} dagen op in één run.\n"
            "     Overweeg de periode op te splitsen in kleinere batches\n"
            "     van maximaal 30 dagen om API-problemen te voorkomen.\n"
        )
 
    if not DIR_SECRETS.exists():
        raise FileNotFoundError(
            f"Secrets-bestand niet gevonden op: {DIR_SECRETS}\n"
            "Maak een .env-bestand aan met CLIENT_ID_WIWB en CLIENT_SECRET_WIWB."
        )

def get_summary(STARTDATUM, EINDDATUM, DATABRON, VARIABELEN, DIR_OUTPUT):

     # Toont een overzicht van de geconfigureerde instellingen
    aantal_dagen = (EINDDATUM - STARTDATUM).days + 1
    print()
    print("=" * 55)
    print("  WIWB Data Downloader")
    print("=" * 55)
    print(f"  Databron   : {DATABRON}")
    print(f"  Variabelen : {', '.join(VARIABELEN)}")
    print(f"  Periode    : {STARTDATUM.date()} t/m {EINDDATUM.date()} ({aantal_dagen} dag(en))")
    print(f"  Uitvoermap : {DIR_OUTPUT}")
    print("=" * 55)
    print()