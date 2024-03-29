import operations


def refresh(cfg):
    for item in list:
        item.recv_topic = cfg.SUB_TOPIC + "/" + item.operation
        item.send_topic = cfg.PUB_TOPIC + "/" + item.operation


class Route(object):
    def __init__(self, desc, operation, event_out):
        self.desc = desc
        self.operation = operation
        self.event_out = event_out
        self.func = getattr(operations, operation)


list = [
    # 样例：单事件
    #Route(desc="开始",
    #      operation="op1",
    #      event_out="inPosition"),
    # 样例：多事件
    #Route(desc="开始",
    #      operation="op2",
    #      event_out=["success", "fail"])
    Route(desc="""""",
          operation="detect",
          event_out="analyseDone")

]
