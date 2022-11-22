import meta
import gateway.gate as gate


class TronGateway(meta.Singleton):
    node = gate.tron.Node

