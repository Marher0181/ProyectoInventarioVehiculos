from flask import Flask, render_template, request, redirect, url_for
from models import db
from datetime import datetime
from config import Config
from datetime import date

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

class Vehiculo(db.Model):
    __tablename__ = 'Vehiculo'
    idVehiculo = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    disponibilidad = db.Column(db.Integer, nullable=False)
    ventas = db.relationship('Venta', back_populates='vehiculo')

class Cliente(db.Model):
    __tablename__ = 'Cliente'
    idCliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dpi = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(4), nullable=False)
    telefono = db.Column(db.String(100), nullable=False)
    ventas = db.relationship('Venta', back_populates='cliente')

class Venta(db.Model):
    __tablename__ = 'Venta'
    idVenta = db.Column(db.Integer, primary_key=True)
    idVehiculo = db.Column(db.Integer, db.ForeignKey('Vehiculo.idVehiculo'), nullable=False)
    idCliente = db.Column(db.Integer, db.ForeignKey('Cliente.idCliente'), nullable=False)
    fechaVenta = db.Column(db.DateTime, default=datetime.utcnow) 
    vehiculo = db.relationship('Vehiculo', back_populates='ventas')
    cliente = db.relationship('Cliente', back_populates='ventas')



@app.route('/')
@app.route('/vehiculo')
def vehiculo():
    marca = request.args.get('marca')
    modelo = request.args.get('modelo')
    anio = request.args.get('anio')
    precio_min = request.args.get('precio_min')
    precio_max = request.args.get('precio_max')

    query = Vehiculo.query.filter_by(disponibilidad=1)

    if marca:
        query = query.filter(Vehiculo.marca.like(f'%{marca}%'))
    if modelo:
        query = query.filter(Vehiculo.modelo.like(f'%{modelo}%'))
    if anio:
        query = query.filter(Vehiculo.anio == anio)
    if precio_min:
        query = query.filter(Vehiculo.precio >= float(precio_min))
    if precio_max:
        query = query.filter(Vehiculo.precio <= float(precio_max))
    else:
        vehiculos = query.all()

    return render_template('vehiculos/vehiculos.html', vehiculos=vehiculos)

@app.route('/agregar_vehiculo', methods=['GET', 'POST'])
def agregar_vehiculo():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        anio = request.form['anio']
        precio = request.form['precio']
        disponibilidad = 1
        nuevo_vehiculo = Vehiculo(marca=marca, modelo=modelo, anio=anio, precio=precio, disponibilidad=disponibilidad)
        db.session.add(nuevo_vehiculo)
        db.session.commit()
        return redirect(url_for('vehiculo'))
    return render_template('vehiculos/agregar_vehiculo.html')

@app.route('/modificar_vehiculo/<int:id>', methods=['GET', 'POST'])
def modificar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)

    if request.method == 'POST':
        vehiculo.marca = request.form['marca']
        vehiculo.modelo = request.form['modelo']
        vehiculo.anio = request.form['anio']
        vehiculo.precio = request.form['precio']
        vehiculo.disponibilidad = 1 

        db.session.commit()
        return redirect(url_for('vehiculo'))

    return render_template('vehiculos/modificar_vehiculo.html', vehiculo=vehiculo)


@app.route('/eliminar_vehiculo/<int:id>', methods=['GET', 'POST'])
def eliminar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(vehiculo)
        db.session.commit()
        return redirect(url_for('vehiculo'))

    return render_template('vehiculos/eliminar_vehiculo.html', vehiculo=vehiculo)


@app.route('/clientes')
def cliente():
    nombre = request.args.get('nombre')
    dpi = request.args.get('dpi')

    query = Cliente.query

    if nombre:
        query = query.filter(Cliente.nombre.like(f'%{nombre}%'))
    if dpi:
        query = query.filter(Cliente.dpi.like(f'%{dpi}%'))

    clientes = query.all()
    return render_template('clientes/clientes.html', clientes=clientes)

@app.route('/agregar_cliente', methods=['GET','POST'])
def agregar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        dpi = request.form['dpi']
        correo = request.form['correo']
        telefono = request.form['telefono']
        nuevo_cliente = Cliente(nombre=nombre, dpi=dpi, correo=correo, telefono=telefono)
        db.session.add(nuevo_cliente)
        db.session.commit()
        return redirect(url_for('cliente'))
    return render_template('clientes/agregar_cliente.html')


@app.route('/modificar_cliente/<int:id>', methods=['GET', 'POST'])
def modificar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.dpi = request.form['dpi']
        cliente.correo = request.form['correo']
        cliente.telefono = request.form['telefono']

        db.session.commit()
        return redirect(url_for('cliente'))

    return render_template('clientes/modificar_cliente.html', cliente=cliente)


@app.route('/eliminar_cliente/<int:id>', methods=['GET', 'POST'])
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(cliente)
        db.session.commit()
        return redirect(url_for('cliente'))

    return render_template('clientes/eliminar_cliente.html', cliente=cliente)

@app.route('/venta')
def venta():
    ventas = (db.session.query(Venta, Vehiculo, Cliente)
          .join(Vehiculo, Venta.idVehiculo == Vehiculo.idVehiculo)
          .join(Cliente, Venta.idCliente == Cliente.idCliente)
          .all())
    clientes = Cliente.query.all()
    vehiculos = Vehiculo.query.filter_by(disponibilidad=1)
    return render_template('ventas/ventas.html', ventas=ventas, clientes=clientes, vehiculos=vehiculos)

@app.route('/agregar_venta', methods=['GET', 'POST'])
def agregar_venta():
    
    clientes = Cliente.query.all()
    vehiculos = Vehiculo.query.filter_by(disponibilidad=1)
    if request.method == 'POST':
        idVehiculo = request.form['idVehiculo']
        idCliente = request.form['idCliente']
        sql = db.text("EXECUTE sp_RegistrarVenta :idVehiculo, :idCliente")
        try:
            db.session.execute(sql, {'idVehiculo': int(idVehiculo), 'idCliente': int(idCliente)})
            db.session.commit()
            return redirect(url_for('venta'))
        except Exception as e:
            print(f"Error al realizar la venta: {e}")
    return render_template('ventas/agregar_venta.html', clientes=clientes, vehiculos=vehiculos)

if __name__ == '__main__':
    app.run(debug=True)