import Models
SEARCH_EDGE=32
class Protocol:
    # 单例
    # 应当改写为状态机形式
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'instance'):
            cls.instance=super(Protocol,cls).__new__(cls)
        return cls.instance
    def __init__(self):#这里应当记录协议状态
        self.notified=False
        self.mark=False #标志是否为同一轮二分搜索
    def handle(self,node,events):
        self.notify(node,events)
        for event in events:
            if event.sender==node:
                node.load(event) #把未发送的事件存储起来
    def retry(self,node):
        global SEARCH_EDGE
        self.notified=False
        if not self.mark:
            SEARCH_EDGE=SEARCH_EDGE//2
            self.mark=True
        if node.id<SEARCH_EDGE:
            while(node.sendBuffer):
                event=node.sendBuffer.pop(0)
                node.resend(event,node.buffer,node.time)
    def notify(self,node,events):
        self.mark=False #在每轮二分搜索结束后更新一轮
        isNeighbor=True
        if node.status==Models.LINSTENING_STATE and not self.notified:
            for event in events:
                if node == event.sender:
                    return
            if isNeighbor:
                params={
                    'startTime':node.time,
                    'endTime':node.time+1,
                    'code':Models.NOTICE_EVENT,
                    'sender':node,
                    'receiver':Models.Node(9999), #假设广播节点为9999
                    'body':'notify'
                }
                print("notify")
                node.send(params,node.buffer)
                self.notified=True
    def flush(self):
        pass #在冲突解决后需要初始化协议状态