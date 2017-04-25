class BaseStation:
    """基站
    
    Attributes:
        id: 编号
        address: 名称 地址
        latitude: 纬度
        longitude: 经度
        user_num: 用户数量
    """

    def __init__(self, id, addr, lat, lng, users=0):
        self.id = id
        self.address = addr
        self.latitude = lat
        self.longitude = lng
        self.user_num = users  # TODO 使用 用户上网时间 代替 用户数量

    def __str__(self):
        return "No.{0}: {1}".format(self.id, self.address)
