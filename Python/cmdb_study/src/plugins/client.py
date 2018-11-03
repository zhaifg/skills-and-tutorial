
# 1. 获取今日未采集主机列表
# 2. 采集资产
# 3. 将资产数据发送到API(POST)
class BaseClient:
    pass


class Agent(BaseClient):
    def file_host(self):
        pass


class SBaseClient(BaseClient):
    pass


class SSH(SBaseClient):
    pass


class Salt(SBaseClient):
    pass
