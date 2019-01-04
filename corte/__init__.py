from flask import Flask
from flask_mail import Mail
from celery import Celery

# ============================================================================
# Inicia a aplicação Flask
# ============================================================================
app = Flask(__name__)

# ============================================================================
# Carrega as configurações a partir de um arquivo
# ============================================================================
app.config.from_object('corte.settings')

# ============================================================================
# Configura a fila de tarefas do Celery
# ============================================================================
celery = Celery(
	app.name, 
	broker=app.config['CELERY_BROKER_URL'], 
	backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

# ============================================================================
# Importa a view da aplicação
# ============================================================================
import corte.views
