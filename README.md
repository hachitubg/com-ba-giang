# 🍚 Cơm Bà Giang

Hệ thống đặt cơm trưa văn phòng với Vue.js + FastAPI + PayOS

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install fastapi uvicorn pandas openpyxl requests python-multipart
uvicorn main:app --reload
```
Backend: http://127.0.0.1:8000

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend: http://localhost:5173

## 📁 Project Structure
```
├── backend/
│   ├── main.py              # FastAPI server
│   ├── excel_handler.py     # Database logic
│   └── data/               # Excel files (auto-created)
├── frontend/
│   ├── src/
│   │   ├── App.vue         # Main app
│   │   └── components/     # Vue components
│   └── .env.development    # API config
```

## ⚙️ Configuration

### Backend Environment (Optional)
Create `backend/.env`:
```
PAYOS_CLIENT_ID=your_client_id
PAYOS_API_KEY=your_api_key
PAYOS_CHECKSUM_KEY=your_checksum_key
```

### Frontend Environment
Create `frontend/.env.development`:
```
VITE_API_URL=http://127.0.0.1:8000
```

## 🔑 Default Access
- **Admin Panel**: /admin (mã admin trong file Excel)
- **User**: Đăng ký tài khoản mới

## 🛠️ Features
- 👤 User authentication
- 👥 Group management
- 🍽️ Daily menu ordering
- 💳 PayOS payment integration
- 📱 Mobile responsive
- 📊 Admin dashboard

## 📞 Support
Check console logs and ensure both servers are running on correct ports.