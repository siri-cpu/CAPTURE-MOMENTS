from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {
    'GAYATHRI': 'GPS123',
    'JYOSHNA': 'JYO123'
}

photographers = [
    {"id": "p1", "name": "Amit Lensman", "skills": ["Wedding", "Portrait"], "image": "amit.jpg"},
    {"id": "p2", "name": "Sana Clickz", "skills": ["Fashion", "Event"], "image": "sana.jpg"},
    {"id": "p3", "name": "Jyoshna Arts", "skills": ["Baby Shoot", "Traditional", "Pre-wedding"], "image": "jyoshna.jpg"},
    {"id": "p4", "name": "Rithik Shots", "skills": ["Wildlife", "Sports", "Drone"], "image": "Rithik.jpg"}
]



availability_data = {
    "p1": ["2025-06-20", "2025-06-23"],
    "p2": ["2025-06-19", "2025-06-22"],
    "p3": ["2025-06-21", "2025-06-25"],
    "p4": ["2025-06-24", "2025-06-26"]  # ← Rithik's available dates
}



@app.route('/')
def home():
    if session.get('logged_in'):
        return redirect(url_for('real_home'))
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    phone = request.form.get('phone')
    password = request.form.get('password')
    if users.get(phone) == password:
        session['logged_in'] = True
        session['user'] = phone
        return redirect(url_for('real_home'))
    return "<h3>Login Failed. Try again.</h3><a href='/'>Back to Login</a>"

@app.route('/real-home')
def real_home():
    if not session.get('logged_in'):
        return redirect(url_for('home'))
    return render_template('real_home.html', user=session.get('user'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/book', methods=['GET', 'POST'])
def book():
    if not session.get('logged_in'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        photographer_id = request.form.get('photographer_id')
        date = request.form.get('date')
        return f"<h2 style='color:green'>Booking Confirmed! For {photographer_id} on {date}.</h2>"

    return render_template('book.html', photographers=photographers)

@app.route('/show-photographers')
def show_photographers():
    if not session.get('logged_in'):
        return redirect(url_for('home'))

    return render_template('photographers.html', photographers=photographers, availability_data=availability_data)

if __name__ == '__main__':
    app.run(debug=True)