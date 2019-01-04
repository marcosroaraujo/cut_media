# corte/tasks.py
"""
Definição das tarefas do Celery

"""
import os
import random
import time
import unicodedata
import re
import celery
import requests
from corte import app

LOCAL_DIR = os.path.abspath(os.path.dirname(__file__))


# ============================================================================
# Remove acentuação de uma string
# ============================================================================
def remove_accents(txt):
    try:
        txt = unicode(txt, 'utf-8')
    except (TypeError, NameError):
        pass
    txt = unicodedata.normalize('NFD', txt)
    txt = txt.encode('ascii', 'ignore')
    txt = txt.decode("utf-8")
    return str(txt)


# ============================================================================
# Remove espaços e caracteres especiais de uma string
# ============================================================================
def normalize_text(txt):
    txt = remove_accents(txt.lower())
    txt = re.sub('[ ]+', '_', txt)
    txt = re.sub('[^0-9a-zA-Z_-]', '', txt)
    return txt



# ============================================================================
# Tarefa de corte - Simula uma tarefa que pode demorar de 10 a 40 segundos
# ============================================================================
@celery.task(bind=True)
def cut_media(self):
    total = random.randint(10, 40)
    for i in range(total):
        self.update_state(state='PROGRESS')

        time.sleep(1)

    return {}


# ============================================================================
# Tarefa de movimentação de media - Simula a gravação de um arquivo em pasta
# pré-determinada e envia título, duração e nome do arquivo gerado para a API
# do Globo Play
# ============================================================================
@celery.task(bind=True)
def save_media(self, x, data):
    print('save media')
    filename = normalize_text(data['title']) + '.mp4'
    path = data['path']
    file_path = os.path.join(LOCAL_DIR, path, filename)
    file = open(file_path, 'w+')
    file.writelines(u'Arquivo de exemplo')
    file.close()
    gplay = {
        "title": data["title"],
        "duration": data["duration"],
        "filename": filename
    }

    req = requests.post('http://localhost:5000/api/v1/globoplay', json=gplay)


