from utils import *

if __name__ == '__main__':
    bs = base_station_reader('data/基站经纬度.csv')
    tmp = user_info_reader('data/上网信息输出表（日表）6月15号之后.csv', bs)
    for i in tmp[:10]:
        print(i)
