import mysql.connector

# Conexión a la base de datos MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="practicadb"
)

# Crear cursor para ejecutar consultas SQL
mycursor = mydb.cursor()

# Constants para el resultado de las funciones
NOTROBAT = "NOTROBAT"
AFEGIT = "AFEGIT"
MODIFICAT = "MODIFICAT"
JAEXISTEIX = "JAEXISTEIX"

# Función para obtener el correo electrónico de un nombre
def getmaildict(nom):
    sql = "SELECT email FROM practica_jl WHERE nombre = %s"
    mycursor.execute(sql, (nom,))
    result = mycursor.fetchone()
    if result:
        return result[0]
    else:
        return NOTROBAT

# Función para agregar un nuevo registro o modificar uno existente
def addmaildict(nom, correu, modif=False):
    oldcorreu = getmaildict(nom)
    if oldcorreu == NOTROBAT:
        sql = "INSERT INTO practica_jl (nombre, email) VALUES (%s, %s)"
        val = (nom, correu)
        mycursor.execute(sql, val)
        mydb.commit()
        return AFEGIT
    elif oldcorreu != correu and modif:
        sql = "UPDATE practica_jl SET email = %s WHERE nombre = %s"
        val = (correu, nom)
        mycursor.execute(sql, val)
        mydb.commit()
        return MODIFICAT
    else:
        return JAEXISTEIX


