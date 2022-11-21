import meta
import src.daemon.node as node


class BaseDaemonCore:
    node_client: node.BaseNode


class TronDaemonCore(BaseDaemonCore, meta.Singleton):

    node_client = node.TronNode

    def __init__(self):
        self.node = self.node_client()
