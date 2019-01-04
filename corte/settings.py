# corte/settings.py
"""
Definições da aplicação

"""
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# ============================================================================
# Configuração do Celery
# ============================================================================
CELERY_BROKER_URL = 'sqla+sqlite:///' + os.path.join(BASE_DIR, 'celery_broker.db')
CELERY_RESULT_BACKEND = 'db+sqlite:///' + os.path.join(BASE_DIR, 'celery_results.db')