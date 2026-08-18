# Smart Recycling Bin: AI‑gestuurde automatische afval detectie & scheiding
De Smart Recycling Bin is een AI‑toepassing die automatisch afvalobjecten herkent en deze indeelt in de juiste afvalcategorie. Het systeem gebruikt YOLOv8‑classificatie, een camera, en een Streamlit‑interface om realtime afvalherkenning mogelijk te maken.

Dit project is ontwikkeld voor Suriname, waar afvalbeheer en recycling een groeiende uitdaging vormen. Door middel van computer vision draagt dit systeem bij aan efficiëntere afvalscheiding en duurzaamheidsinitiatieven.

---

## Functionaliteiten
1. AI‑Classificatie (YOLOv8n‑cls)

**Herkent 10 afvalcategorieën:**
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

Model getraind op CPU met geoptimaliseerde instellingen. Automatische bak‑toewijzing op basis van categorie.

**2. Live Camera Stream**
- Realtime classificatie via webcam.
- Continu updates van label + confidence.
- Kleurcodes voor afvalbakken.

**3. Upload‑modus**
- Upload een afbeelding (JPG/PNG).
- Systeem classificeert het object.
- Toont confidence + toegewezen afvalbak.

**4. Dataset**
- Gestandaardiseerde dataset (256×256).
- YOLOv8 maakt automatisch train/val splits.
- Ondersteunt 10 klassen.

**5. CPU‑vriendelijke training**
- **Optimalisatie:**
    - epochs=15
    - imgsz=192
    - fraction=0.6
    - batch=8

- **Fine‑tuning:**
    - epochs=10
    - imgsz=224
    - fraction=1.0

---

## Projectstructuur
Smart Recycling Bin SR/
│
├── app/
│   └── streamlit_app.py
│
├── dataset/
│   ├── original/
│   ├── standardized_256/
│   ├── standardized_256_split/
│   ├── standardized_384/
│   └── data.yaml (niet gebruikt voor classificatie)
│
│
├── runs/
│   └── classify/
│       └── train-5/
│           └── weights/
│               ├── best.pt
│               └── last.pt
│
├── sorter.py
├── requirements.txt
└── README.md

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
runs/classify/train-5/weights/best.pt
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
- Realtime classificatie

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
