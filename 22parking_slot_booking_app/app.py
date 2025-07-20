from flask import Flask, render_template, request, redirect, url_for, abort
import uuid

app = Flask(__name__)

# In-memory data
slots = [
    {'id': 'A1', 'location': 'Zone A', 'date': '2025-07-21'},
    {'id': 'B2', 'location': 'Zone B', 'date': '2025-07-21'},
    {'id': 'C3', 'location': 'Zone C', 'date': '2025-07-22'}
]

bookings = []

@app.route('/')
def home():
    selected_date = request.args.get('date')
    available_slots = [s for s in slots if not any(b['slot_id'] == s['id'] for b in bookings)]
    if selected_date:
        available_slots = [s for s in available_slots if s['date'] == selected_date]
    dates = sorted({slot['date'] for slot in slots})
    return render_template('home.html', slots=available_slots, dates=dates, selected_date=selected_date)

@app.route('/book/<slot_id>', methods=['GET', 'POST'])
def book(slot_id):
    slot = next((s for s in slots if s['id'] == slot_id), None)
    if not slot:
        abort(404)
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        bookings.append({
            'slot_id': slot_id,
            'name': name,
            'phone': phone
        })
        return redirect(url_for('confirmation', name=name, slot=slot_id))
    return render_template('book.html', slot=slot)

@app.route('/confirmation')
def confirmation():
    name = request.args.get('name')
    slot = request.args.get('slot')
    return render_template('confirmation.html', name=name, slot=slot)

if __name__ == '__main__':
    app.run(debug=True)
