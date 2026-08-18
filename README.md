# Smart Recycling Bin: AI‑gestuurde automatische afval detectie & scheiding

De Smart Recycling Bin is een AI‑toepassing die automatisch afvalobjecten herkent en deze indeelt in de juiste afvalcategorie. Het systeem gebruikt **YOLOv8‑classificatie**, een **camera**, een **punten‑systeem**, **badges**, een **gebruikerslogin met database**, en een **mobiele‑vriendelijke Streamlit‑interface** om realtime afvalherkenning mogelijk te maken.

Dit project is ontwikkeld voor Suriname, waar afvalbeheer en recycling een groeiende uitdaging vormen. Door middel van computer vision draagt dit systeem bij aan efficiëntere afvalscheiding en duurzaamheidsinitiatieven.

---

## Functionaliteiten

### 1. AI‑Classificatie (YOLOv8n‑cls)
Herkenning van **10 afvalcategorieën**:
- battery  
- biological  
- cardboard  
- clothes  
- glass  
- metal  
- paper  
- plastic  
- shoes  
- trash  

Het model is getraind met YOLOv8‑classificatie en geoptimaliseerd voor CPU‑training.  
Automatische bak‑toewijzing gebeurt op basis van categorie.

---

### 2. Live Camera Stream
- Realtime classificatie via webcam  
- Continu updates van label + confidence  
- Kleurcodes per afvalbak  
- Mobiele‑vriendelijke interface  

---

### 3. Upload‑modus
- Upload een afbeelding (JPG/PNG)  
- Systeem classificeert het object  
- Confidence + toegewezen afvalbak worden getoond  

---

### 4. Login‑systeem 
Gebruikers kunnen:

- een eigen account aanmaken  
- inloggen met gebruikersnaam + wachtwoord  
- veilig opgeslagen wachtwoorden (SHA‑256 hashing)  
- punten worden per gebruiker opgeslagen  
- badges worden automatisch toegekend  


#### 1. Registratieproces
Gebruikers kunnen een nieuw account aanmaken via het registratieformulier in de app.

Tijdens registratie worden de volgende stappen uitgevoerd:
- De gebruiker voert een gebruikersnaam en wachtwoord in.
- Het wachtwoord wordt gehasht met SHA‑256.
- De gebruikersgegevens worden opgeslagen in app/users.json.
- De gebruiker krijgt standaard 0 punten toegewezen.

Voorbeeld van een opgeslagen gebruiker:
```bash
{
    "gebruiker1": {
        "password": "<gehasht_wachtwoord>",
        "points": 0
    }
}
```

#### 2. Inlogproces
Bij het inloggen voert de gebruiker een gebruikersnaam en wachtwoord in.
Het systeem controleert vervolgens:
- Bestaat de gebruikersnaam in de database?
- Komt het gehashte wachtwoord overeen met het opgeslagen wachtwoord?

**Als beide controles slagen:**
- de gebruiker wordt ingelogd
- de punten worden geladen
- de sessie wordt opgeslagen in st.session_state

Als de gegevens niet kloppen, wordt een foutmelding getoond.


#### 3. Wachtwoordbeveiliging
Wachtwoorden worden nooit in platte tekst opgeslagen.
In plaats daarvan worden ze gehasht met:
```bash
hashlib.sha256(password.encode()).hexdigest()
```
Dit zorgt ervoor dat wachtwoorden niet leesbaar zijn in de database en niet terug te herleiden zijn naar de originele tekst.

#### 4. Sessiebeheer
Streamlit gebruikt `st.session_state` om de loginstatus vast te houden.
Hierin worden onder andere opgeslagen:
- `logged_in`
- `username`
- `points`

Zolang de sessie actief is, blijft de gebruiker ingelogd.
Bij het herstarten van de app moet opnieuw worden ingelogd.

#### 5. Punten opslaan
Wanneer een gebruiker een object classificeert, worden punten toegevoegd.
Deze punten worden direct teruggeschreven naar de database:
```bash
update_points(username, nieuwe_punten)
```
Hierdoor blijft de voortgang van elke gebruiker bewaard, ook na het sluiten van de app.

#### 6. Databasebestand
De database bevindt zich in:
```bash
app/users.json
```
Dit bestand wordt automatisch aangemaakt wanneer de eerste gebruiker wordt geregistreerd.

#### 7. Overzicht van loginfuncties
De loginmodule bestaat uit de volgende functies:
- hash_password(password)
- load_users()
- save_users(users)
- register_user(username, password)
- login_user(username, password)
- update_points(username, points)

**Deze functies zorgen samen voor:**
- veilige opslag
- correcte authenticatie
- sessiebeheer
- puntensynchronisatie

---

### 5. JSON‑database
Alle gebruikers worden opgeslagen in:
```bash
users.json
```

---

### 6. Live Camera Stream
- Realtime classificatie via webcam  
- Continu updates van label + confidence  
- Kleurcodes per afvalbak  
- Mobiele‑vriendelijke interface  

---

### 7. Upload‑modus
- Upload een afbeelding (JPG/PNG)  
- Systeem classificeert het object  
- Confidence + toegewezen afvalbak worden getoond  

---

### 8. Puntensysteem
Gebruikers verdienen **10 punten per gerecycled object**.

Punten worden opgeslagen in `st.session_state` per gebruiker.

---

### 9. Badge‑systeem
Badges worden automatisch toegekend op basis van punten:

| Badge | Punten | Emoji |
|-------|--------|--------|
| Bronze Recycler | 0–99 | 🥉 |
| Silver Recycler | 100–249 | 🥈 |
| Gold Recycler | 250–499 | 🥇 |
| Platinum Recycler | 500–999 | 🔱 |
| Diamond Recycler | 1000+ | 💎 |

---

## Projectstructuur

```text
smart-recycling-bin/
│
├── app/
│   └── streamlit_app.py
│
├── runs/
│   └── classify/
│       └── train-7/
│           └── weights/
│               └── best.pt
│
├── sorter.py
├── camera.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml

---

## Installatie
**1. Virtuele omgeving**
```bash 
python -m venv venv
venv\Scripts\activate
```

**2. Dependancies**
```bash
pip install -r requirements.txt 
```

---

## Model trainen:
- **Stap 1: Eerste training**
```bash
yolo classify train data=dataset/standardized_256 model=yolov8n-cls.pt epochs=15 imgsz=192 batch=8 fraction=0.6
```

- **Stap 2: Fine‑tuning**
```bash
yolo classify train data=dataset/standardized_256 model=runs/classify/train-5/weights/best.pt epochs=10 imgsz=224 batch=8 fraction=1.0
```

**Het uiteindelijke model staat in:**
```bash
runs/classify/train-7/weights/best.pt
```

---

### App starten
```bash
streamlit run app/streamlit_app.py
```

**Functionaliteiten:**
- Live camera feed
- Upload‑modus
- Confidence‑score
- Kleurcodes per afvalbak
- Login + registratie
- Puntensysteem
- Badge‑systeem
- Mobiele‑vriendelijke UI

---

## Surinaamse context
- **Dit project sluit aan bij actuele uitdagingen in Suriname:**
    - Onvoldoende afvalscheiding.
    - Gebrek aan recyclinginfrastructuur.
    - Initiatieven zoals Suresur Green, Amazonia Recycling en Green Circle.
    - Overheidsprojecten voor vuilcontainers en afvalbakken.
    - Discussies over afvalrekken bij scholen en gebouwen.

- **De Smart Recycling Bin ondersteunt deze initiatieven door:**
    - automatisering
    - educatie
    - duurzaamheid
    - efficiëntie

---

## Conclusie
- **De Smart Recycling Bin combineert:**
    - AI‑classificatie
    - realtime computer vision
    - een gebruiksvriendelijke interface
    - Surinaamse duurzaamheidsdoelen

- **Het systeem is klaar voor:**
    - implementatie
    - demonstraties
    - uitbreiding naar fysieke prototypes

---

## Bronnen
- Suresur Green. (z.d.). Homepage. https://suresur.green/
- Amazonia Recycling. (z.d.). Homepage. https://www.amazonarecycling.sr/
- Green Circle. (z.d.). Homepage. https://www.green-circle.net/
- Ministerie van Openbare Werken Suriname. (z.d.). Openbare Werken schaft vuilcontainers en afvalbakken aan. https://gov.sr/openbare-werken-schaft-vuilcontainers-en-afvalbakken-aan/
- DB Suriname. (2024, 15 juni). De huidige uitdagingen in Suriname met betrekking tot afvalbeheer en recycling. https://www.dbsuriname.com/2024/06/15/de-huidige-uitdagingen-in-suriname-met-betrekking-tot-afvalbeheer-en-recycling/
- DB Suriname. (2025, 16 april). Afvalrekken voor gebouwen of scholen: is dat wel een goed idee? https://www.dbsuriname.com/2025/04/16/afvalrekken-voor-gebouwen-of-scholen-is-dat-wel-een-goed-idee/
- Chen, Z., Li, Y., & Wang, X. (2023). YOLOv8: A new state-of-the-art real-time object detector. arXiv. https://arxiv.org/abs/2302.02976        
- Zhang, H., Wu, C., & Zhou, Y. (2020). Garbage classification using deep learning: A survey and benchmark. arXiv. https://arxiv.org/abs/2006.05873
