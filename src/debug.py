from algorithms import *
from utils import Utils

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    tmp = Utils.base_station_reader('data/基站经纬度.csv')
    bs = Utils.user_info_reader('data/上网信息输出表（日表）6月15号之后.csv', tmp)
    dist = Utils.distance_between_stations(tmp)
    kmeans_placer = KMeansServerPlacement(bs, dist)
    kmeans_placer.place_server(100)
    print(kmeans_placer.objective_latency(), kmeans_placer.objective_workload())
    top_k_placer = TopKServerPlacement(bs, dist)
    top_k_placer.place_server(100)
    print(top_k_placer.objective_latency(), top_k_placer.objective_workload())
    random_placer = RandomServerPlacement(bs, dist)
    random_placer.place_server(100)
    print(random_placer.objective_latency(), random_placer.objective_workload())
    pass
