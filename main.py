import configparser
import requests

# Lese den API-Key aus der Konfigurationsdatei
def load_api_key(config_file="config.ini"):
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
        api_key = config.get("ionos", "api_key")
        if not api_key:
            raise ValueError("API-Key nicht gefunden")
        return api_key
    except Exception as e:
        print(f"Fehler beim Laden des API-Keys: {e}")
        raise

API_KEY = load_api_key()
BASE_URL = "https://api.hosting.ionos.com/dns"  # Basis-URL der IONOS DNS API

def get_external_ip():
    """
    Ermittelt die aktuelle externe IP-Adresse.
    """
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=10)
        response.raise_for_status()
        ip = response.json().get("ip")
        if not ip:
            raise ValueError("Keine IP-Adresse in der Antwort gefunden")
        return ip
    except Exception as e:
        print(f"Fehler beim Abrufen der externen IP: {e}")
        raise

def update_dynamic_dns(hostname, ip):
    url = f"{BASE_URL}/v1/dyndns"
    payload = {
        "hostname": hostname,
        "ip": ip
    }
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code in (200, 201):
            print(f"Erfolgreich aktualisiert: {hostname} -> {ip}")
        else:
            print(f"Update fehlgeschlagen für {hostname} (Status {response.status_code}): {response.text}")
            # Optionale: Weitere Informationen aus der Antwort extrahieren
            try:
                error_info = response.json()
                print("Details:", error_info)
            except Exception:
                pass
    except Exception as e:
        print(f"Fehler beim Aktualisieren von {hostname}: {e}")

def main():
    try:
        ip = get_external_ip()
        print(f"Aktuelle externe IP: {ip}")
    except Exception:
        return

    # Lese alle Domains aus der Datei, leere Zeilen werden ignoriert
    try:
        with open("domains.txt", "r", encoding="utf-8") as file:
            domains = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Fehler beim Einlesen der domains.txt: {e}")
        return

    # Für jede Domain wird die IP-Adresse aktualisiert
    for domain in domains:
        update_dynamic_dns(domain, ip)

if __name__ == "__main__":
    main()
