# pip install flask
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from pyrsistent import field

app = Flask(__name__)  # aplicacion
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/bdpythonapi'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Crear tabla modelo Categoria
class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))

    def __init__(self, cat_nom, cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp


db.create_all()

# Esquema
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nom', 'cat_desp')


# Una sola respuesta/registro
categoria_schema = CategoriaSchema()
# Muchas respuestas/registros
categorias_schema = CategoriaSchema(many=True)

# GET ####################
@app.route('/categoria', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)
##########################

# GET POR ID #############
@app.route('/categoria/<id>', methods=['GET'])
def get_categoria_por_id(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)
#########################

# POST ####################
@app.route('/categoria', methods=['POST'])
def insertar_categoria():
    cat_nom = request.json['cat_nom']
    cat_desp = request.json['cat_desp']

    nuevo_registro = Categoria(cat_nom, cat_desp)
	
    db.session.add(nuevo_registro)
    db.session.commit()
    return categoria_schema.jsonify(nuevo_registro)

# PUT ####################
@app.route('/categoria/<id>', methods=['PUT'])
def update_categoria(id):
    actualizarCategoria = Categoria.query.get(id)

    cat_nom = request.json['cat_nom']
    cat_desp = request.json['cat_desp']

    actualizarCategoria.cat_nom = cat_nom
    actualizarCategoria.cat_desp = cat_desp

    db.session.commit()

    return categoria_schema.jsonify(actualizarCategoria)

# DELETE ####################
@app.route('/categoria/<id>', methods=['DELETE'])
def delete_categoria(id):
    eliminarCategoria = Categoria.query.get(id)
    db.session.delete(eliminarCategoria)
    db.session.commit()
    return categoria_schema.jsonify(eliminarCategoria)

#############################
# Mensaje de Bienvenida
@app.route('/', methods=['GET'])
def index():
    return jsonify({'Mensaje': 'Bienvenido'})


if __name__ == "__main__":  # Iniciar aplicacion
    app.run(debug=True)
