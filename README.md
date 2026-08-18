# Smart Recycling Bin: AI‑gestuurde automatische afval detectie & scheiding

De Smart Recycling Bin is een AI‑toepassing die automatisch afvalobjecten herkent en deze indeelt in de juiste afvalcategorie. Het systeem gebruikt **YOLOv8‑classificatie**, een **camera**, een **punten‑systeem**, **badges**, **QR‑login**, en een **mobiele‑vriendelijke Streamlit‑interface** om realtime afvalherkenning mogelijk te maken.

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

### 4. Puntensysteem
Gebruikers verdienen **10 punten per gerecycled object**.

Punten worden opgeslagen in `st.session_state` per gebruiker.

---

### 5. Badge‑systeem
Badges worden automatisch toegekend op basis van punten:

| Badge | Punten | Emoji |
|-------|--------|--------|
| Bronze Recycler | 0–99 | 🥉 |
| Silver Recycler | 100–249 | 🥈 |
| Gold Recycler | 250–499 | 🥇 |
| Platinum Recycler | 500–999 | 💎 |
| Diamond Recycler | 1000+ | 🔱 |

---

### 6. QR‑code Login
- Gebruiker scant een QR‑code met een unieke gebruikers‑ID  
- Gebruiker voert de code in → app logt hem in  
- Punten worden per gebruiker opgeslagen  
- Later uitbreidbaar naar Firebase of database  

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
- QR‑login
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

## Hoe werkt de QR‑code login?
- Gebruiker scant een QR‑code (bijv. met hun telefoon).
- QR‑code bevat een unieke gebruikers‑ID (bijv. user123).
- Gebruiker voert deze code in → app logt hem in.
- Punten worden opgeslagen per gebruiker in st.session_state.
- Later kun je dit uitbreiden naar Firebase of een database.

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
