from algorithms import *
from utils import DataUtils

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    data = DataUtils('data/基站经纬度.csv', 'data/上网信息输出表（日表）6月15号之后.csv')
    mip_placer = MIPServerPlacement(data.base_stations, data.distances)
    mip_placer.place_server(100)
    # kmeans_placer = KMeansServerPlacement(data.base_stations, data.distances)
    # kmeans_placer.place_server(100)
    # print(kmeans_placer.objective_latency(), kmeans_placer.objective_workload())
    # top_k_placer = TopKServerPlacement(data.base_stations, data.distances)
    # top_k_placer.place_server(100)
    # print(top_k_placer.objective_latency(), top_k_placer.objective_workload())
    # random_placer = RandomServerPlacement(data.base_stations, data.distances)
    # random_placer.place_server(100)
    # print(random_placer.objective_latency(), random_placer.objective_workload())
    pass
