# FarmersHub Project

## Projektbeschreibung
Das Projekt **FarmersHub** verwendet ein **Django**-Backend und ein **Next.js**-Frontend. Die PostgreSQL-Datenbank wird über **Supabase** gehostet. Dieses Dokument beschreibt, wie das Projekt eingerichtet wird, welche Technologien verwendet wurden und wie man damit arbeitet.

---

## Technologien

### Frontend
- **Next.js**
- **Tailwind CSS**

### Backend
- **Django**
- **PostgreSQL** (gehostet auf Supabase)

---

## Installation und Einrichtung

### Voraussetzungen
- **Python** (>= 3.10)
- **Node.js** (>= 16.x)
- **npm**
- **PostgreSQL**-Datenbank (Supabase-Account erforderlich)

---

### Projektstruktur

```
FarmersHub/
├── backend/       # Django-Backend
│   ├── backend/   # Projektordner (Settings, URL-Konfiguration etc.)
│   ├── farmers/   # App mit Models und Logik
│   ├── venv/      # Virtuelle Umgebung
│   └── manage.py  # Django-Management-Skript
├── frontend/      # Next.js-Frontend
└── README.md      # Dokumentation
```

---

### Backend (Django)

1. **Repository klonen**:
   ```bash
   git clone <repository-url>
   cd FarmersHub/backend/backend
   ```

2. **Virtuelle Umgebung erstellen und aktivieren**:
   ```bash
   python3 -m venv venv # Windows: py -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Supabase-Datenbank konfigurieren**:
   Passe die `DATABASES`-Einstellung in `backend/backend/settings.py` an:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'postgres',
           'USER': 'postgres',
           'PASSWORD': 'xfwRlG2itV8l@yB8',
           'HOST': 'db.qbqnlcmndkrpwmdepmft.supabase.co',
           'PORT': '5432',
       }
   }
   ```

5. **Migrationen synchronisieren**:
   Da die Tabellen bereits in der Datenbank existieren, führe Folgendes aus:
   ```bash
   python manage.py makemigrations
   python manage.py migrate --fake
   ```

6. **Server starten**:
   ```bash
   python manage.py runserver
   ```

7. **Admin-Interface einrichten (optional)**:
   Erstelle einen Superuser, falls erforderlich:
   ```bash
   python manage.py createsuperuser
   ```

   Rufe das Admin-Interface unter [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) auf.

---

### Frontend (Next.js)

1. **Repository klonen und in das Frontend-Verzeichnis wechseln**:
   ```bash
   cd FarmersHub/frontend
   ```

2. **Abhängigkeiten installieren**:
   ```bash
   npm install
   ```

3. **Entwicklungsserver starten**:
   ```bash
   npm run dev
   ```

4. **Frontend im Browser aufrufen**:
   Gehe zu [http://localhost:3000](http://localhost:3000).

---

### Kommunikation zwischen Frontend und Backend

Das Frontend kommuniziert über API-Endpunkte mit dem Django-Backend. Beispiel:

```javascript
// Beispiel-API-Aufruf
import axios from 'axios';

const fetchData = async () => {
    const response = await axios.get('http://127.0.0.1:8000/api/endpoint/');
    return response.data;
};
```

Um Cross-Origin-Anfragen zu ermöglichen, wurden folgende Einstellungen in `settings.py` vorgenommen:

```python
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

---

## Nützliche Befehle

### Backend
- Server starten:
  ```bash
  python manage.py runserver
  ```
- Migrationen erstellen:
  ```bash
  python manage.py makemigrations
  ```
- Migrationen anwenden:
  ```bash
  python manage.py migrate
  ```
- Django-Shell starten:
  ```bash
  python manage.py shell
  ```

### Frontend
- Entwicklungsserver starten:
  ```bash
  npm run dev
  ```
- Produktions-Build erstellen:
  ```bash
  npm run build
  ```
- Statisches Deployment testen:
  ```bash
  npm run start
  ```

---

## To-Do für das Team
- **Datenbankmodell überprüfen**: Stellt sicher, dass die Modelle in `farmers/models.py` korrekt sind.
- **APIs erweitern**: Zusätzliche API-Endpunkte für die Kommunikation zwischen Frontend und Backend erstellen.
- **Frontend-Komponenten bauen**: UI-Komponenten und Integrationen erstellen, um Backend-Daten im Frontend darzustellen.
- **Tests schreiben**: Unit-Tests für Backend und Frontend implementieren.

---

## FAQ

**1. Warum wird ein Fehler "Relation does not exist" angezeigt?**
   - Stelle sicher, dass die Datenbanktabellen korrekt eingerichtet und die Fake-Migrationen angewendet wurden (`python manage.py migrate --fake`).

**2. Wie erstelle ich einen neuen Endpunkt im Backend?**
   - Erstelle eine View in `farmers/views.py` und registriere sie in `farmers/urls.py`.

**3. Kann ich das Projekt in der Produktion verwenden?**
   - Passe die `settings.py`-Einstellungen an (z. B. `DEBUG=False` und sichere Konfigurationen wie `SECRET_KEY`), bevor du es live stellst.

---

Viel Erfolg mit FarmersHub! 🚜

---

# Leitfaden: Migrationen und Datenbank-Änderungen in Django

Django verwendet Migrationen, um Änderungen an der Datenbankstruktur zu verwalten. Dieser Leitfaden erklärt Schritt für Schritt, wie du neue Datenbankeinträge hinzufügst, Migrationen erstellst und alles synchron hältst.

---

## **Grundlagen**

### Was sind Migrationen?
Migrationen sind Dateien, die die Änderungen an deinen Django-Modellen beschreiben und es Django ermöglichen, die Datenbankstruktur entsprechend anzupassen. Sie synchronisieren den Python-Code (Modelle) mit der tatsächlichen Datenbank.

### Typische Szenarien:
- Du fügst ein neues Modell hinzu.
- Du änderst ein bestehendes Modell (z. B. neue Felder, Feldtypen, Beziehungen).
- Du entfernst ein Modell oder ein Feld.

---

## **Ablauf bei Änderungen an den Modellen**

1. **Änderungen in den Modellen vornehmen**
   - Öffne die Datei `farmers/models.py`.
   - Bearbeite ein vorhandenes Modell oder erstelle ein neues Modell. Beispiel:

   ```python
   class Crop(models.Model):
       id = models.BigAutoField(primary_key=True)
       name = models.CharField(max_length=100)
       planting_date = models.DateField()
   ```

2. **Neue Migrationen erstellen**
   - Nachdem du die Änderungen gespeichert hast, führe den folgenden Befehl aus:
     ```bash
     python manage.py makemigrations
     ```
   - Django analysiert die Änderungen und erstellt eine neue Migrationsdatei (z. B. `farmers/migrations/0002_add_crop.py`).

3. **Migrationen anwenden**
   - Führe den folgenden Befehl aus, um die Änderungen in der Datenbank zu übernehmen:
     ```bash
     python manage.py migrate
     ```
   - Django wendet die Migrationsdateien an und aktualisiert die Datenbank entsprechend.

---

## **Was tun, wenn Konflikte auftreten?**

### Problem: "Relation does not exist"
   - Stelle sicher, dass alle Migrationsdateien korrekt angewendet wurden:
     ```bash
     python manage.py showmigrations
     ```
   - Falls Migrationen fehlen, wende sie an:
     ```bash
     python manage.py migrate
     ```

### Problem: "Conflicting migrations detected"
   - Das passiert, wenn mehrere Entwickler gleichzeitig Änderungen vornehmen. Lösung:
     1. **Migrationen zusammenführen**:
        ```bash
        python manage.py makemigrations --merge
        ```
     2. Wende die zusammengeführte Migration an:
        ```bash
        python manage.py migrate
        ```

---

## **Synchronisation zwischen Teammitgliedern**

### 1. **Nach neuen Änderungen suchen**
   - Ziehe die neuesten Änderungen aus dem Repository:
     ```bash
     git pull
     ```
   - Überprüfe, ob es neue Migrationen gibt:
     ```bash
     python manage.py showmigrations
     ```

### 2. **Migrationen anwenden**
   - Wenn neue Migrationen vorhanden sind, wende sie an:
     ```bash
     python manage.py migrate
     ```

### 3. **Eigene Änderungen durchführen**
   - Nimm Änderungen an den Modellen vor und erstelle Migrationen wie oben beschrieben.

### 4. **Migrationen teilen**
   - Nachdem du Migrationen erstellt hast, füge sie zum Repository hinzu:
     ```bash
     git add farmers/migrations
     git commit -m "Add migrations for new models"
     git push
     ```

---

## **Best Practices**

1. **Migrationen immer erstellen und anwenden**:
   - Vergiss nicht, nach Änderungen in den Modellen immer `makemigrations` und `migrate` auszuführen.

2. **Migrationen ins Repository aufnehmen**:
   - Migrationen sollten immer im Versionskontrollsystem (z. B. Git) gespeichert werden.

3. **Datenbankänderungen synchron besprechen**:
   - Bei größeren Änderungen (z. B. Löschen von Tabellen oder Feldern) stimme dich vorher mit dem Team ab, um Datenverlust zu vermeiden.

4. **Fake-Migrationen nur für bestehende Tabellen**:
   - Wenn die Tabelle bereits existiert (z. B. bei einer neuen Datenbankanbindung), verwende:
     ```bash
     python manage.py migrate --fake
     ```

5. **Lokale Tests durchführen**:
   - Stelle sicher, dass Änderungen lokal getestet werden, bevor sie in das Repository gepusht werden.

---

## **Zusammenfassung**
- **Neue Migrationen**: `python manage.py makemigrations`
- **Migrationen anwenden**: `python manage.py migrate`
- **Migrationen prüfen**: `python manage.py showmigrations`
- **Konflikte lösen**: `python manage.py makemigrations --merge`

Mit diesem Leitfaden bleibt die Datenbank immer synchron, und das Arbeiten im Team wird reibungsloser. 🚀

