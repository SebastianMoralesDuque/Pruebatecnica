# 🚀 StockPro: Inventory Intelligence & Blockchain Integrity

StockPro is a high-performance inventory management system that leverages **Artificial Intelligence** for executive analysis and **Blockchain Technology** for data immutability.

---

## 🏗️ Technical Architecture

### Tech Stack
- **Backend**: Django 5.x + Django Rest Framework
- **Database**: PostgreSQL (Hosted on **Supabase** via IPv4 Transaction Pooler)
- **Frontend**: React + Vite + Tailwind CSS + Framer Motion
- **AI Engine**: Google Gemini (generative-ai)
- **Blockchain**: Solana Protocol (Devnet)

---

## ⛓️ Solana Blockchain Integration

StockPro uses the Solana blockchain to provide **Proof of Integrity** for every inventory report.

### How it works:
1. **Hashing**: We generate a unique SHA-256 fingerprint (Hash) of the inventory data and the AI analysis.
2. **On-Chain Recording**: This hash is sent to the **Solana Memo Program** (`MemoSq4gqABvAn9NoSKeyJv6Ysl7R8L34KxyTqQuX9A`).
3. **Immutability**: Once recorded, the transaction hash (TxHash) serves as a permanent, timestamped receipt that proves the data has not been altered.

### 🚰 Solana Faucet (Devnet)
To perform certifications, you need **Devnet SOL**.
1. Visit [faucet.solana.com](https://faucet.solana.com/).
2. Paste your public key: `4ThzNAZJkndwjS6AuULjT2mgeWeM82tEJVQrFoy5aCKn`.
3. Select "Devnet" and request tokens.
4. Verify your balance:
   ```bash
   solana balance 4ThzNAZJkndwjS6AuULjT2mgeWeM82tEJVQrFoy5aCKn --url https://api.devnet.solana.com
   ```

---

## 🛠️ Installation & Setup

### 📦 Backend Deployment
1. **Virtual Env**: `python -m venv venv` && `source venv/bin/activate`
2. **Install**: `pip install -r requirements.txt`
3. **Environment**: Create a `.env` file in `backend/` based on the template:
   ```env
   DB_NAME=postgres
   DB_USER=postgres.zngvnppcnybhnzjwevtz
   DB_PASSWORD=your_password
   DB_HOST=aws-1-eu-west-1.pooler.supabase.com
   DB_PORT=6543
   GOOGLE_API_KEY=your_key
   RESEND_API_KEY=your_key
   SOLANA_PRIVATE_KEY=your_hex_key
   ```
4. **Database**: `python manage.py migrate`
5. **Start**: `python manage.py runserver`

### 💻 Frontend Deployment
1. **Install**: `npm install`
2. **Start**: `npm run dev`

---

## 🧪 Testing Suite
Ensure system reliability with Pytest:
```bash
cd backend
pytest -v
```
*Current Coverage: Models, ViewSets, AI Mocking, and Solana Transaction Proofs.*

---

## 📖 API Documentation
- **Swagger UI**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **ReDoc**: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)

---

## 👤 Credits & Integrity
Developed as a premium solution for inventory transparency using cutting-edge technologies.
# Pruebatecnica
