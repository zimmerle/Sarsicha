
import peewee, datetime
from playhouse.shortcuts import model_to_dict, dict_to_model

from src.singleton import Singleton
from src.configuration import Configuration


class Database(metaclass=Singleton):
    def __init__(self):
        self._database = peewee.SqliteDatabase(
            Configuration().get()['proxy']['database']
        )


    def connect(self):
        self._database.connect()


    def close(self):
        self._database.close()



class Node(peewee.Model):
    """
    """
    CAPABILITIES_REACH_PROXY_VIA_HTTP = 4

    name = peewee.CharField()
    created_at = peewee.DateField(default=datetime.date.today)
    node_id = peewee.CharField()
    version = peewee.IntegerField()
    capabilities = peewee.IntegerField()
    key = peewee.TextField()

    def create(node_id, cap = 0):
        n = Node()
        n.name = "no name"
        n.node_id = node_id
        n.version = 0
        n.capabilities = cap
        n.key = "not yet stablished"
        n.save()
        return n

    class Meta:
        database = Database()._database


class CommandQueue(peewee.Model):
    """
    """

    WAITING = 0
    SUBMITTED = 4

    node_id = peewee.ForeignKeyField(Node, backref='commands')
    status = peewee.IntegerField()
    command = peewee.TextField()
    created_at = peewee.DateField(default=datetime.date.today)
    downloaded_at = peewee.DateField(default=datetime.date.today)

    def statusName(t):
        if t == CommandQueue.WAITING:
            return "Waiting"
        elif t == CommandQueue.SUBMITTED:
            return "Submited"
        else:
            return "Done"

    class Meta:
        database = Database()._database


class CommandResponse(peewee.Model):
    """
    """
    command_id = peewee.ForeignKeyField(CommandQueue, backref='response')
    created_at = peewee.DateField(default=datetime.date.today)
    results = peewee.TextField()

    def new(command_id, data):
        cmd = CommandResponse()
        cmd.command_id = command_id
        cmd.results = data
        cmd.save()


    class Meta:
        database = Database()._database



class PoolingLogs(peewee.Model):
    """
    """

    TYPE_HTTP = 0
    TYPE_DNS = 4

    node_id = peewee.ForeignKeyField(Node, backref='logs')
    created_at = peewee.DateField(default=datetime.date.today)
    pooling_type = peewee.IntegerField()

    def poolingName(t):
        if t == PoolingLogs.TYPE_DNS:
            return "dns"
        else:
            return "http"

    class Meta:
        database = Database()._database

