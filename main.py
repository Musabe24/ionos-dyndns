import configparser
import json
import requests

def load_api_key(config_file="config.ini"):
    """Lädt den API-Key aus der Konfigurationsdatei."""
    config = configparser.ConfigParser()
    config.read(config_file)
    try:
        return config.get("ionos", "api_key")
    except Exception as e:
        print(f"Fehler beim Laden des API-Keys: {e}")
        raise

def load_domains(domains_file="domains.txt"):
    """Lädt die Domains aus der domains.txt als Liste."""
    try:
        with open(domains_file, "r", encoding="utf-8") as file:
            domains = [line.strip() for line in file if line.strip()]
        return domains
    except Exception as e:
        print(f"Fehler beim Einlesen der domains.txt: {e}")
        raise

def update_dynamic_dns(domains, api_key):
    """Sendet einen POST-Request mit dem JSON-Payload, um die Dynamic DNS Einstellungen zu aktualisieren."""
    url = "https://api.hosting.ionos.com/dns/v1/dyndns"
    payload = {
        "domains": domains,
        "description": "My DynamicDns"
    }
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    print("Sende folgenden Payload:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code in (200, 201):
            print("Erfolgreich aktualisiert:")
            print(response.json())
        else:
            print(f"Update fehlgeschlagen (Status {response.status_code}):")
            try:
                error_info = response.json()
                print("Details:", error_info)
            except Exception:
                print("Fehlerhafte Antwort:", response.text)
    except Exception as e:
        print(f"Fehler beim Senden des Requests: {e}")

def main():
    try:
        api_key = load_api_key()
        domains = load_domains()
    except Exception:
        return

    update_dynamic_dns(domains, api_key)

if __name__ == "__main__":
    main()
