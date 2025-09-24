# Fitfinder: AIML Virtual Try-On & Wardrobe Visualizer

### Quick Start (Windows)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Visit http://localhost:5000/

### Structure
- `app.py`: Flask app and routes
- `templates/`: Bootstrap pages
- `static/`: CSS/JS/assets
- `aiml/`: Models and pipeline stubs
- `scrapers/`: External product fetchers
- `db/`: SQLite DB, uploads, outputs

### Notes
- Upload size limited to 16 MB
- AIML steps are currently stubs; they copy input to output
- History stored in SQLite at `db/fitfinder.sqlite3`


