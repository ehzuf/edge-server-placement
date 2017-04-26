import logging

from utils import Utils

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    tmp = Utils.base_station_reader('data/基站经纬度.csv')
    bs = Utils.user_info_reader('data/上网信息输出表（日表）6月15号之后.csv', tmp)
    dist = Utils.distance_between_stations(tmp)
    pass
