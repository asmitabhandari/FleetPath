# Folder Setup

## Backend
```bash
cd Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Frontend
```bash
cd Frontend
npm install
```

## Run
```bash
# Terminal 1
cd Backend
venv\Scripts\activate
uvicorn main:app --reload

# Terminal 2
cd Frontend
npm start
```

## Verify
- Backend: http://localhost:8000/docs
- Frontend: http://localhost:3000
