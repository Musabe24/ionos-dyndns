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
