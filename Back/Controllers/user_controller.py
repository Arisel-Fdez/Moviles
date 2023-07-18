from flask import Blueprint, jsonify, request
from models.models import ArbolBinario, db

user_bp = Blueprint('user_bp', __name__)
arbol = ArbolBinario()

@user_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    arbol.agregar_usuario(data['nombre'], data['email'], data['contraseña'], data['telefono'])
    return jsonify({'status': 'Usuario registrado con éxito'})

@user_bp.route('/usuarios/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    contraseña = data['contraseña']
    usuario = arbol.autenticar_usuario(email, contraseña)
    if usuario:
      #  token = usuario.token
        return jsonify({'message': 'Inicio de sesión exitoso token'})
    else:
        return jsonify({'message': 'Email o contraseña incorrectos'})

@user_bp.route('/activar-usuario', methods=['POST'])
def activar_usuario():
    data = request.get_json()
    usuario_id = data['id']
    arbol.activar_usuario(usuario_id)
    return jsonify({'status': 'Usuario activado con éxito'})
    pass

@user_bp.route('/usuarios-activos', methods=['GET'])
def obtener_usuarios_activos():
    usuarios_activos = []
    usuarios_ref = db.collection('usuarios').where('activo', '==', True).stream()
    for usuario in usuarios_ref:
        usuario_data = usuario.to_dict()
        usuarios_activos.append({'id': usuario.id, 'nombre': usuario_data['nombre']})
    return jsonify({'usuarios_activos': usuarios_activos})
    pass

@user_bp.route('/usuarios/inorden', methods=['GET'])
def ver_usuarios_inorden():
    usuarios = arbol.obtener_usuarios_inorden()
    return jsonify(usuarios)
    pass

@user_bp.route('/usuarios/postorden', methods=['GET'])
def ver_usuarios_postorden():
    usuarios = arbol.obtener_usuarios_postorden()
    return jsonify(usuarios)
    pass

@user_bp.route('/usuarios/preorden', methods=['GET'])
def ver_usuarios_preorden():
    usuarios = arbol.obtener_usuarios_preorden()
    return jsonify(usuarios)
    pass

@user_bp.route('/usuarios/eliminar/<int:token>', methods=['DELETE'])
def eliminar_usuario(token):
    arbol.eliminar_usuario(token)
    return jsonify({'message': 'Usuario eliminado exitosamente'})
    pass

arbol.agregar_a_base_de_datos