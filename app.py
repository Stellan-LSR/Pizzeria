from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


config = {
    'user': 'root',
    'password': 'samuel',
    'host': 'localhost',
    'database': 'pizzeria'
}


cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        
        # Insertar pedido en la base de datos
        query = "INSERT INTO pedidos (nombre, descripcion) VALUES (%s, %s)"
        cursor.execute(query, (nombre, descripcion))
        cnx.commit()
        
        return redirect(url_for('listado'))
    return render_template('registro.html')


@app.route('/listado')
def listado():
    # Consultar pedidos en la base de datos
    query = "SELECT * FROM pedidos"
    cursor.execute(query)
    pedidos = cursor.fetchall()
    
    return render_template('listado.html', pedidos=pedidos)


@app.route('/eliminar/<int:id>')
def eliminar(id):
    # Eliminar pedido de la base de datos
    query = "DELETE FROM pedidos WHERE id = %s"
    cursor.execute(query, (id,))
    cnx.commit()
    
    return redirect(url_for('listado'))

if __name__ == '__main__':
    app.run(debug=True)