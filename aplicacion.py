from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

mydb = None

def connect_to_database():
    global mydb
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="projectedb"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connect_to_database()
        mycursor = mydb.cursor()
        sql = "SELECT id FROM projecte_jl WHERE nombre = %s AND contrasenya = %s"
        val = (username, password)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()
        mycursor.close()
        if user:
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connect_to_database()
        mycursor = mydb.cursor()
        sql = "SELECT id FROM projecte_jl WHERE nombre = %s"
        val = (username,)
        mycursor.execute(sql, val)
        existing_user = mycursor.fetchone()
        if existing_user:
            return "El usuario ya existe. Por favor, elige otro nombre de usuario."
        else:
            sql = "INSERT INTO projecte_jl (nombre, contrasenya) VALUES (%s, %s)"
            val = (username, password)
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        sport = request.form['sport']
        return redirect(url_for('sport_info', sport=sport))
    return render_template('dashboard.html')

@app.route('/sport_info/<sport>')
def sport_info(sport):
    return render_template('sport_info.html', sport=sport)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/paroimpar/<int:numero>")
def show_post(numero):
    # Verificar si el número es par o impar
    if numero % 2 == 0:
        return f"El número {numero} es par."
    else:
        return f"El número {numero} es impar."

@app.route("/cumple100/<nombre>/<int:edad>")
def calcular_cumple100(nombre, edad):
    # Obtener el año actual
    año_actual = 2024

    # Calcular el año en que cumplirá 100 años
    año_cumple_100 = año_actual + (100 - edad)

    # Renderizar la plantilla 
    return render_template('about_me.html', nombre=nombre, año_cumple_100=año_cumple_100)


if __name__ == '__main__':
    app.run(debug=True)
