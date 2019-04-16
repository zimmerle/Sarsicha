#!/usr/bin/env python

from flask import Flask, redirect, request
app = Flask(__name__)
import sys, getopt, json
from playhouse.shortcuts import model_to_dict, dict_to_model
from datetime import date, datetime

from src.configuration import loadProxyConfig, Configuration
loadProxyConfig()
conf = Configuration()
from src.logger import log
from src.database import *
from src.utils import json_serial


@app.before_request
def before_request():
    Database().connect()


@app.after_request
def after_request(response):
    Database().close()
    return response


@app.route('/pool/<node_id>', methods = ['POST', 'GET'])
def pool(node_id):
    """
    """
    n = None
    try:
        n = Node(Node.node_id == '').get()
    except:
        pass

    if n == None:
        n = Node.create(node_id, Node.CAPABILITIES_REACH_PROXY_VIA_HTTP)

    p = PoolingLogs()
    p.node_id = n.id
    p.pooling_type = PoolingLogs.TYPE_HTTP
    p.save()

    data = request.get_json()
    if data != None and len(data) > 0:
        try:
            c = CommandResponse.new(data['cmd'], data['data'])
            z = n.commands.select().where(CommandQueue.id == data['cmd']).get()
            z.status = CommandQueue.SUBMITTED
            z.save()
        except Exception as e:
            print(str(e))
            pass

    z = n.commands.select().where(CommandQueue.status == CommandQueue.WAITING).select()
    a = []
    for i in z:
        a.append(model_to_dict(i))
    if len(a) > 0:
        return json.dumps(a, default=json_serial)

    return '{"What?": "there are days better than others."}'


@app.route('/admin/node/list')
def admin_node_list():
    n = Node.select().order_by(Node.created_at.desc()).select()
    a = []
    for i in n:
        a.append(model_to_dict(i))
    return json.dumps(a, default=json_serial)


@app.route('/admin/node/<node_id>')
def admin_node_info(node_id):
    node = Node(node_id=node_id).get()
    n = model_to_dict(node)

    l = []
    for i in node.logs.order_by(PoolingLogs.created_at.asc()):
        l.append(model_to_dict(i))
    n['pooling'] = l

    c = []
    for i in node.commands:
        c.append(model_to_dict(i))
    n['commands'] = c
    return json.dumps(n, default=json_serial)


@app.route('/admin/node/cmd/send/<node_id>', methods = ['POST'])
def admin_node_cmd_send(node_id):
    obs = []
    ret = {}
    try:
        node = None
        try:
            node = Node.get(Node.node_id == node_id)
        except Node.DoesNotExist:
            pass
        if node == None:
            node = Node.create(node_id)
            obs.append('Never heard about: ' + node_id + 
                '. Adding the command to the queue just in case.')

        q = CommandQueue()
        q.node_id = node.id
        q.status = CommandQueue.WAITING
        q.command = request.get_json()
        q.save()
    except Exception as e:
        ret['status'] = "failed"
        ret['error'] = str(e)
        return json.dumps(ret)
    
    ret['status'] = "ok"
    ret['obs'] = obs
    return json.dumps(ret)


@app.route('/admin/cmd/queue/list')
def admin_cmd_queue_list():
    b = []
    for a in CommandQueue(status = CommandQueue.WAITING).select().order_by(CommandQueue.created_at):
        b.append(model_to_dict(a))
    return json.dumps(b, default=json_serial)


@app.route('/admin/cmd/response/<command_id>')
def admin_cmd_response(command_id):
    n = {
        'status': 'failed'
    }
    try:
        node = CommandQueue(command_id=command_id).get()
        resp = node.response.get()
        n['status'] = 'ok'
        n['command'] = model_to_dict(node)
        n['response'] = model_to_dict(resp)
    except Exception as e:
        print(str(e))
        pass
    
    return json.dumps(n, default=json_serial)


@app.route('/')
def index():
    return redirect(conf["proxy.home-redirection"], code=302)


def main():
    log(0, "Loading config: " + str(conf.get()))
    log(0, "Proxy " + conf['proxy.name'] + " is up and running.")
    log(0, "There are " + str(Node.select().count()) + " nodes around.")
    app.run(
        host=conf['proxy.listen.ip'],
        port=conf['proxy.listen.port'],
        debug=conf['proxy.debug']
    )


if __name__ == "__main__":
    """
    FIXME: There is no deamon mode here. Naturally, with the
           right amount of time, the implementation will be
           made. Important to notice that the architecture is
           already here.
    """        
    main()

