# FastAPI Conveyor & Sorting Controller

Files:
- app.py
- helpers/
- utils/

Install (on Raspberry Pi or dev env):
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Notes:
- If running on non-Raspberry Pi dev machine the hardware helpers will run in simulation mode (print statements).
- Place `yolov8n.pt` model in the working dir or let ultralytics download it.
