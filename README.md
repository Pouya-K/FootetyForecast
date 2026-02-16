<div align="center">

<!-- Animated Header -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0e17,50:3b82f6,100:22c55e&height=220&section=header&text=FooteyForecast&fontSize=72&fontColor=f1f5f9&fontAlignY=35&desc=Premier%20League%20predictions%20powered%20by%20ML&descSize=20&descAlignY=55&animation=fadeIn" width="100%" />

<br/>

<!-- Badges -->
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![Next.js](https://img.shields.io/badge/Next.js_16-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS_4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)

<br/>

<p>
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=3B82F6&center=true&vCenter=true&repeat=true&width=400&height=40&lines=Predict.+Watch.+Repeat.+%E2%9A%BD" alt="Typing SVG" />
</p>

<br/>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="700">

</div>

<br/>

## ⚡ What is FooteyForecast?

FooteyForecast is a **full-stack machine learning application** that predicts English Premier League match outcomes in real time. A custom **PyTorch neural network** is trained on 4+ seasons of historical EPL data and produces predictions for every upcoming matchweek — including **win/draw/loss probabilities**, **expected goals**, **corners**, and **cards**.

The model automatically **retrains itself every week** via GitHub Actions, pulling the latest results and refreshing its knowledge — so predictions stay sharp all season long.

<br/>

<div align="center">
<table>
<tr>
<td align="center"><b>🎯 Match Outcomes</b><br/><sub>Win / Draw / Loss<br/>probabilities</sub></td>
<td align="center"><b>⚽ Goals</b><br/><sub>Expected goals for<br/>each team</sub></td>
<td align="center"><b>🚩 Corners</b><br/><sub>Predicted corner<br/>counts</sub></td>
<td align="center"><b>🟨 Cards</b><br/><sub>Yellow & red card<br/>predictions</sub></td>
</tr>
</table>
</div>

<br/>

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FooteyForecast                              │
├──────────────┬──────────────────┬──────────────┬───────────────────┤
│              │                  │              │                   │
│   Frontend   │     Backend      │   Database   │    ML Pipeline    │
│   (Next.js)  │    (FastAPI)     │  (Postgres)  │    (PyTorch)      │
│              │                  │              │                   │
│  ┌────────┐  │  ┌────────────┐  │  ┌────────┐  │  ┌─────────────┐ │
│  │ React  │──│──│  REST API  │──│──│ SQLAlch │  │  │ Data Ingest │ │
│  │  19    │  │  │  Endpoints │  │  │  emy    │  │  │ football-   │ │
│  └────────┘  │  └────────────┘  │  └────────┘  │  │ data.co.uk  │ │
│  ┌────────┐  │  ┌────────────┐  │              │  └──────┬──────┘ │
│  │Tailwind│  │  │  Fixtures  │  │              │  ┌──────▼──────┐ │
│  │ CSS 4  │  │  │  Service   │  │              │  │  Feature    │ │
│  └────────┘  │  │ (live API) │  │              │  │  Engine     │ │
│              │  └────────────┘  │              │  │  (45 feats) │ │
│              │  ┌────────────┐  │              │  └──────┬──────┘ │
│              │  │ Prediction │  │              │  ┌──────▼──────┐ │
│              │  │  Engine    │──│──────────────│──│  Neural Net │ │
│              │  └────────────┘  │              │  │  Multi-Head │ │
│              │                  │              │  └─────────────┘ │
├──────────────┴──────────────────┴──────────────┴───────────────────┤
│                    Docker Compose · GitHub Actions                  │
└─────────────────────────────────────────────────────────────────────┘
```

<br/>

## 🧠 The ML Model

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/216122041-518ac897-8d92-4c6b-9b3f-ca01dcaf38ee.png" width="80" />
</div>

The prediction engine is a **multi-head neural network** built with PyTorch. A shared backbone extracts match context, then four specialized heads produce different prediction targets simultaneously:

```
Input (45 features)
        │
        ▼
┌───────────────┐
│  Linear(128)  │
│  ReLU + Drop  │
│  Linear(64)   │
│  ReLU + Drop  │
└───────┬───────┘
        │ Shared Representation
   ┌────┼────┬─────────┐
   ▼    ▼    ▼         ▼
 ┌───┐┌───┐┌───┐   ┌───┐
 │WDL││GLS││CRN│   │CRD│
 │(3)││(2)││(2)│   │(2)│
 └───┘└───┘└───┘   └───┘
  ↓    ↓    ↓       ↓
 Soft  Soft  Soft   Soft
 max   Plus  Plus   Plus
```

| Component | Details |
|:--|:--|
| **Architecture** | Multi-head MLP with shared trunk (128 → 64) |
| **WDL Head** | 3-class softmax with temperature scaling (T=1.3) for calibrated probabilities |
| **Goals / Corners / Cards** | Softplus activation → always non-negative, smooth gradients |
| **Loss Function** | CrossEntropy (WDL) + Poisson NLL (Goals, Corners, Cards) |
| **Loss Weights** | WDL: 1.0 · Goals: 2.0 · Corners: 0.5 · Cards: 0.5 |
| **Optimizer** | AdamW (lr=5e-4) · 300 epochs |
| **Scaler** | StandardScaler fitted on training features |

<br/>

### 📊 The 45 Features

Every prediction is driven by a rich feature vector engineered from historical data:

<details>
<summary><b>🔍 Click to expand full feature list</b></summary>

<br/>

| Category | Features | Window |
|:--|:--|:--|
| **Rest Days** | Days since last match (home & away) | — |
| **Elo Ratings** | Home Elo, Away Elo, Elo difference | Rolling |
| **Head-to-Head** | H2H win rates, H2H avg goals | Last 5 meetings |
| **Overall Form** | Goals scored/conceded, corners, cards, points | Last 5 & 10 |
| **Venue Form** | Home/away-specific goals, corners, cards, points | Last 5 & 10 |

</details>

<br/>

### 🔄 Weekly Retraining

A **GitHub Actions** workflow runs every **Sunday at 10 PM UTC**:

```
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Download │───▶│  Build   │───▶│  Train   │───▶│  Commit  │
  │ Latest   │    │ Features │    │  Model   │    │  & Push  │
  │ Results  │    │ (45 cols)│    │ (300 ep) │    │  to repo │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

> The model always has the freshest data — form, Elo ratings, and head-to-head records update automatically.

<br/>

## 🖥️ Tech Stack

<div align="center">

| Layer | Technology | Role |
|:--|:--|:--|
| 🎨 **Frontend** | Next.js 16 · React 19 · Tailwind CSS 4 | Dark-themed UI with match cards & probability bars |
| ⚙️ **Backend** | FastAPI · SQLAlchemy · Uvicorn | REST API for fixtures & predictions |
| 🗄️ **Database** | PostgreSQL 16 | Persistent prediction storage |
| 🧠 **ML** | PyTorch · scikit-learn · pandas | Multi-head neural network |
| 📦 **Infra** | Docker Compose · GitHub Actions | Containerized deployment & weekly CI/CD |
| 📡 **Data** | football-data.co.uk · football-data.org | Historical CSVs & live fixture API |

</div>

<br/>

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- A free API key from [football-data.org](https://www.football-data.org/client/register)

### 1️⃣ Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/FooteyForecast.git
cd FooteyForecast
```

### 2️⃣ Set up environment variables

```bash
echo "FOOTBALL_DATA_KEY=your_api_key_here" > .env
```

### 3️⃣ Launch with Docker Compose

```bash
docker compose up --build
```

That's it! Three containers spin up:

| Service | URL | Description |
|:--|:--|:--|
| **Frontend** | [localhost:3000](http://localhost:3000) | Next.js web app |
| **Backend** | [localhost:8000](http://localhost:8000) | FastAPI server |
| **Database** | `localhost:5432` | PostgreSQL |

<br/>

## 📡 API Endpoints

<details>
<summary><b>View all endpoints</b></summary>

<br/>

| Method | Endpoint | Description |
|:--|:--|:--|
| `GET` | `/` | Health check |
| `GET` | `/api/fixtures?week_offset=0` | Fixtures for a week (0=current, -1=last, 1=next) |
| `GET` | `/api/teams` | List all known teams |
| `GET` | `/api/predictions?matchweek=15` | Stored predictions for a matchweek |
| `POST` | `/api/predict` | Predict a single match |
| `POST` | `/api/predict/matchweek` | Predict an entire matchweek |

**Example — predict a single match:**

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"home_team": "Arsenal", "away_team": "Chelsea", "match_date": "2026-02-21"}'
```

**Response:**

```json
{
  "home_team": "Arsenal",
  "away_team": "Chelsea",
  "match_date": "2026-02-21",
  "home_win": 52.3,
  "draw": 24.1,
  "away_win": 23.6,
  "home_goals": 1.7,
  "away_goals": 1.1,
  "home_corners": 5.8,
  "away_corners": 4.2,
  "home_cards": 1.9,
  "away_cards": 2.3
}
```

</details>

<br/>

## 📁 Project Structure

```
FooteyForecast/
├── frontend/                    # Next.js 16 web application
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx         # Main page — matchweek view
│   │   │   ├── layout.tsx       # Root layout (dark theme)
│   │   │   └── globals.css      # CSS variables & dark palette
│   │   ├── components/
│   │   │   ├── MatchCard.tsx    # Match card with probability bar & stats
│   │   │   └── WeekNavigation.tsx  # Week selector with date range
│   │   └── lib/
│   │       └── api.ts           # API client (fixtures + predictions)
│   └── Dockerfile
│
├── backend/                     # FastAPI REST API
│   ├── app/
│   │   ├── main.py              # App entry point & CORS config
│   │   ├── database.py          # SQLAlchemy engine & session
│   │   ├── models/
│   │   │   └── prediction.py    # Prediction DB model
│   │   ├── schemas/
│   │   │   └── prediction.py    # Pydantic request/response schemas
│   │   ├── routers/
│   │   │   ├── fixtures.py      # /api/fixtures endpoint
│   │   │   └── predictions.py   # /api/predict endpoints
│   │   └── services/
│   │       └── fixtures_service.py  # football-data.org API client
│   ├── requirements.txt
│   └── Dockerfile
│
├── ml/                          # Machine learning pipeline
│   ├── data/
│   │   └── download_csv.py      # Download EPL data (5 seasons)
│   ├── features/
│   │   └── build_features.py    # 45-feature engineering + Elo ratings
│   ├── model/
│   │   ├── architecture.py      # Multi-head MatchPredictor network
│   │   ├── train.py             # Training loop (Poisson + CE loss)
│   │   └── predict.py           # Inference engine
│   └── models/
│       └── matchweek_v1.pt      # Trained model weights
│
├── .github/workflows/
│   └── weekly.yml               # Automated weekly retraining pipeline
│
└── docker-compose.yml           # Full-stack orchestration
```

<br/>

## 🔧 Local Development

<details>
<summary><b>Run without Docker</b></summary>

<br/>

**Backend:**

```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:pass@localhost:5432/matchweek
export FOOTBALL_DATA_KEY=your_key
uvicorn app.main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

**ML Pipeline:**

```bash
# Download data
python ml/data/download_csv.py

# Build features
python ml/features/build_features.py

# Train model
cd ml/model && python train.py
```

</details>

<br/>

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

<br/>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0e17,50:3b82f6,100:22c55e&height=120&section=footer" width="100%" />

<br/>

**Built with ❤️ and PyTorch**

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=14&pause=1000&color=64748B&center=true&vCenter=true&repeat=true&width=400&lines=Predict.+Watch.+Repeat.+%E2%9A%BD" alt="Footer typing" />

</div>
