# Root

docker compose up -d

# Backend folder

pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend folder

npm install
ng serve
