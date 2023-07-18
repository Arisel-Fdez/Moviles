from flask import Blueprint, jsonify, request
from models.models import ArbolBinario, db

chat_bp = Blueprint('chat_bp', __name__)
arbol = ArbolBinario()

@chat_bp.route('/chat/grupo', methods=['POST'])
def enviar_chat_de_grupo():
    data = request.get_json()
    grupo_id = data['grupo_id']
    sender_id = data['sender_id']
    message = data['message']
    arbol.agregar_chat(sender_id, grupo_id, message, group_chat=True)
    return jsonify({'status': 'Mensaje enviado al grupo con éxito'})
    pass

@chat_bp.route('/chat/grupo/<grupo_id>', methods=['GET'])
def obtener_chat_de_grupo(grupo_id):
    chats = arbol.obtener_chat(None, grupo_id, group_chat=True)
    return jsonify({'chats': chats})
    pass

@chat_bp.route('/chat/<sender_id>/<receiver_id>', methods=['POST'])
def enviar_chat(sender_id, receiver_id):
    message = request.get_json()['message']
    arbol.agregar_chat(sender_id, receiver_id, message)
    return jsonify({'status': 'Mensaje enviado con éxito'})
    pass

@chat_bp.route('/chat/<sender_id>/<receiver_id>', methods=['GET'])
def obtener_chat(sender_id, receiver_id):
    chats = arbol.obtener_chat(sender_id, receiver_id)
    return jsonify({'chats': chats})
    pass

arbol.inicializar_arbol_desde_base_de_datos()

arbol.inicializar_chats_desde_base_de_datos()
