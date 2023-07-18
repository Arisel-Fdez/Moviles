import random
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('/home/fdezdev/FdezDev/BACK-Movile/Back/config/credential.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

class Nodo:
    def __init__(self, nombre, email, contraseña, telefono):
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña
        self.telefono = telefono
        self.activo = False  
        self.izquierdo = None
        self.derecho = None

class Grupo:
    def __init__(self, id):
        self.id = id
        self.usuarios = []

    def agregar_usuario(self, token):
        self.usuarios.append(token)

class Chat:
    def __init__(self, sender_id, receiver_id, message, group_chat=False):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = message
        self.group_chat = group_chat

class ArbolBinario:
    def __init__(self):
        self.raiz = None
        self.chats = []
        self.grupos = []

    def agregar_grupo(self, id):
        grupo = Grupo(id)
        self.grupos.append(grupo)
        return grupo

    def encontrar_grupo(self, id):
        for grupo in self.grupos:
            if grupo.id == id:
                return grupo
        return None

    def agregar_usuario_a_grupo(self, grupo_id, usuario_id):
        grupo = self.encontrar_grupo(grupo_id)
        if grupo is not None:
            grupo.agregar_usuario(usuario_id)
            return True
        return False

    def agregar_chat(self, sender_id, receiver_id, message, group_chat=False):
        chat = Chat(sender_id, receiver_id, message, group_chat)
        self.chats.append(chat)
        self.agregar_chat_a_base_de_datos(sender_id, receiver_id, message, group_chat)

    def obtener_chat(self, sender_id, receiver_id, group_chat=False):
        if group_chat:
            relevant_chats = [chat.message for chat in self.chats if chat.group_chat and chat.receiver_id == receiver_id]
        else:
            relevant_chats = [chat.message for chat in self.chats if not chat.group_chat and ((chat.sender_id == sender_id and chat.receiver_id == receiver_id) or (chat.sender_id == receiver_id and chat.receiver_id == sender_id))]
        return relevant_chats

    def agregar_usuario(self, nombre, email, contraseña, telefono):
        token = random.randint(1000, 9999)
        nuevo_nodo = Nodo(nombre, email, contraseña, telefono)
        nuevo_nodo.key = token
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self._agregar_recursivo(self.raiz, nuevo_nodo)

        self.agregar_a_arbol(nombre, email, contraseña, telefono, token)
        self.agregar_a_base_de_datos(nombre, email, contraseña, telefono, token)

    def _agregar_recursivo(self, nodo_actual, nuevo_nodo):
        if nuevo_nodo.key < nodo_actual.key:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = nuevo_nodo
            else:
                self._agregar_recursivo(nodo_actual.izquierdo, nuevo_nodo)
        elif nuevo_nodo.key > nodo_actual.key:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = nuevo_nodo
            else:
                self._agregar_recursivo(nodo_actual.derecho, nuevo_nodo)
        else:
            print("La Token ya existe en el árbol.")

    def agregar_a_arbol(self, nombre, email, contraseña, telefono, token):
        nuevo_nodo = Nodo(nombre, email, contraseña, telefono)
        nuevo_nodo.key = token
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self._agregar_recursivo(self.raiz, nuevo_nodo)

    def agregar_a_base_de_datos(self, nombre, email, contraseña, telefono, token):
        try:
            usuario = {
                'nombre': nombre,
                'email': email,
                'contraseña': contraseña,
                'telefono': telefono,
                'token': token,
                'activo': False  # Nuevo campo para indicar el estado de activación del usuario
            }
            db.collection('usuarios').document(str(token)).set(usuario)
        except Exception as e:
            print("Error al conectar a la base de datos:", e)

    def agregar_chat_a_base_de_datos(self, sender_id, receiver_id, message, group_chat=False):
        try:
            chat = {
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'message': message,
                'group_chat': group_chat
            }
            db.collection('chats').add(chat)
        except Exception as e:
            print("Error al conectar a la base de datos:", e)

    def inicializar_arbol_desde_base_de_datos(self):
        try:
            usuarios = db.collection('usuarios').stream()

            for usuario in usuarios:
                usuario = usuario.to_dict()
                nombre = usuario['nombre']
                email = usuario['email']
                contraseña = usuario['contraseña']
                telefono = usuario['telefono']
                token = usuario['token']
                self.agregar_a_arbol(nombre, email, contraseña, telefono, token)

        except Exception as e:
            print("Error al conectar a la base de datos:", e)

    def inicializar_chats_desde_base_de_datos(self):
        try:
            chats = db.collection('chats').stream()

            for chat in chats:
                chat = chat.to_dict()
                sender_id = chat['sender_id']
                receiver_id = chat['receiver_id']
                message = chat['message']
                group_chat = chat['group_chat']
                self.agregar_chat(sender_id, receiver_id, message, group_chat)

        except Exception as e:
            print("Error al conectar a la base de datos:", e)

    def eliminar_usuario(self, token):
        db.collection('usuarios').document(str(token)).update({'activo': False})

    def activar_usuario(self, token):
        db.collection('usuarios').document(str(token)).update({'activo': True})
    
    def autenticar_usuario(self, email, contraseña):
        return self._autenticar_recursivo(self.raiz, email, contraseña)

    def _autenticar_recursivo(self, nodo_actual, email, contraseña):
        if nodo_actual is None:
            return None

        if nodo_actual.email == email and nodo_actual.contraseña == contraseña:
            return nodo_actual

        if email < nodo_actual.email:
            return self._autenticar_recursivo(nodo_actual.izquierdo, email, contraseña)
        else:
            return self._autenticar_recursivo(nodo_actual.derecho, email, contraseña)
    def obtener_usuarios_inorden(self):
        usuarios = []
        self._obtener_inorden(self.raiz, usuarios)
        return usuarios

    def obtener_usuarios_postorden(self):
        usuarios = []
        self._obtener_postorden(self.raiz, usuarios)
        return usuarios

    def obtener_usuarios_preorden(self):
        usuarios = []
        self._obtener_preorden(self.raiz, usuarios)
        return usuarios

    def _obtener_inorden(self, nodo_actual, usuarios):
        if nodo_actual:
            self._obtener_inorden(nodo_actual.izquierdo, usuarios)
            usuario = {
                "nombre": nodo_actual.nombre,
                "email": nodo_actual.email,
                "contraseña": nodo_actual.contraseña,
                "telefono": nodo_actual.telefono,
                "token": nodo_actual.key,
                "activo": nodo_actual.activo
            }
            usuarios.append(usuario)
            self._obtener_inorden(nodo_actual.derecho, usuarios)

    def _obtener_postorden(self, nodo_actual, usuarios):
        if nodo_actual:
            self._obtener_postorden(nodo_actual.izquierdo, usuarios)
            self._obtener_postorden(nodo_actual.derecho, usuarios)
            usuario = {
                "nombre": nodo_actual.nombre,
                "email": nodo_actual.email,
                "contraseña": nodo_actual.contraseña,
                "telefono": nodo_actual.telefono,
                "token": nodo_actual.key,
                "activo": nodo_actual.activo
            }
            usuarios.append(usuario)

    def _obtener_preorden(self, nodo_actual, usuarios):
        if nodo_actual:
            usuario = {
                "nombre": nodo_actual.nombre,
                "email": nodo_actual.email,
                "contraseña": nodo_actual.contraseña,
                "telefono": nodo_actual.telefono,
                "token": nodo_actual.key,
                "activo": nodo_actual.activo
            }
            usuarios.append(usuario)
            self._obtener_preorden(nodo_actual.izquierdo, usuarios)
            self._obtener_preorden(nodo_actual.derecho, usuarios)

    pass
