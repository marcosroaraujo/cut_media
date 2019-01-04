# corte/views.py
from flask import request, jsonify
from corte import app
from corte.tasks import cut_media, save_media

## API GloboPlay - Recebe informação do arquivo cortado
@app.route('/api/v1/globoplay', methods=['POST'])
def gplay():
    data = request.json
    print('globoplay ---------')
    print(data)
    return jsonify(data)

## API de corte de arquivos - Dispara tarefa em background
@app.route('/api/v1/cutmedia', methods=['POST'])
def cutmedia():
    data = request.json
    try:
        task = cut_media.apply_async(link=save_media.s(data))
        res = {
            'job_id': task.id,
            'state': task.state,
            'message': 'Tarefa iniciada com sucesso'}

        return jsonify(res), 202
    except Exception as e:
        res = {
            'job_id': '',
            'state': 'ERROR',
            'message': 'Ocorreu um erro ao iniciar uma tarefa'}

        return jsonify(res), 501


## API de acompanhamento do status da tarefa
@app.route('/api/v1/status/<task_id>')
def status(task_id):
    task = cut_media.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info), 
        }

    return jsonify(response)

