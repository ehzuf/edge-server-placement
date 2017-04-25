from utils import *

if __name__ == '__main__':
    bs = base_station_reader('data/基站经纬度.csv')
    tmp = user_info_reader('data/上网信息输出表（日表）6月15号之后.csv', bs)
    with open('data/info.txt', 'w') as f:
        for item in tmp:
            f.write("id={0}, address={1}, user_num={2}, workload={3}\n".format(item.id, item.address, item.user_num, item.workload))
        f.close()
