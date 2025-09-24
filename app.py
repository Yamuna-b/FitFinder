from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import sqlite3
from werkzeug.utils import secure_filename
import os


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('config.Config')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/gallery')
    def gallery():
        return render_template('gallery.html')

    @app.route('/try-on')
    def try_on():
        return render_template('tryon.html')

    @app.post('/upload-photo')
    def upload_photo():
        file = request.files.get('photo')
        if not file or file.filename == '':
            flash('Please select a photo to upload.', 'warning')
            return redirect(url_for('try_on'))
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        # Stub: run AIML pipeline to generate output image
        output_filename = f"result_{filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        # For now just copy uploaded file as placeholder output
        with open(upload_path, 'rb') as src, open(output_path, 'wb') as dst:
            dst.write(src.read())

        # Save to history
        save_history(filename, output_filename)

        flash('Photo processed (stub).', 'success')
        return redirect(url_for('history'))

    @app.route('/room')
    def room():
        return render_template('room.html')

    @app.post('/upload-room')
    def upload_room():
        file = request.files.get('room')
        if not file or file.filename == '':
            flash('Please select a room image to upload.', 'warning')
            return redirect(url_for('room'))
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        flash('Room uploaded (stub).', 'success')
        return redirect(url_for('room'))

    @app.route('/history')
    def history():
        rows = fetch_history()
        return render_template('history.html', items=rows)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.post('/contact')
    def contact_post():
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        message = (request.form.get('message') or '').strip()
        if not name or not email or not message:
            flash('Please fill in all fields.', 'warning')
            return redirect(url_for('contact'))
        flash('Thanks for reaching out! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))

    @app.route('/outputs/<path:filename>')
    def serve_output(filename: str):
        return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=False)

    @app.post('/history/<int:item_id>/delete')
    def delete_history(item_id: int):
        # Fetch filename first
        conn = get_db_connection()
        row = conn.execute('SELECT output_filename FROM history WHERE id = ?', (item_id,)).fetchone()
        if row:
            conn.execute('DELETE FROM history WHERE id = ?', (item_id,))
            conn.commit()
            # Remove file if exists
            try:
                os.remove(os.path.join(app.config['OUTPUT_FOLDER'], row['output_filename']))
            except FileNotFoundError:
                pass
        conn.close()
        flash('History item deleted.', 'success')
        return redirect(url_for('history'))

    @app.route('/privacy')
    def privacy():
        return render_template('privacy.html')

    @app.route('/terms')
    def terms():
        return render_template('terms.html')

    return app


def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'fitfinder.sqlite3')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            output_filename TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()


def save_history(filename: str, output_filename: str) -> None:
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO history (filename, output_filename) VALUES (?, ?)",
        (filename, output_filename),
    )
    conn.commit()
    conn.close()


def fetch_history():
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT id, filename, output_filename, created_at FROM history ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return rows


if __name__ == '__main__':
    init_db()
    app = create_app()
    app.run(debug=True)


