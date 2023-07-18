from flask import Flask
from Controllers.user_controller import user_bp
from Controllers.chat_controller import chat_bp
#from models.models import ArbolBinario

app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(chat_bp)

if __name__ == '__main__':
  #  arbol = ArbolBinario()
   # arbol.inicializar_arbol_desde_base_de_datos()
    #arbol.inicializar_chats_desde_base_de_datos()
    app.run()
