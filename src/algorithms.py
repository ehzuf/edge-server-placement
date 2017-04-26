import random
from typing import List

from base_station import BaseStation
from edge_server import EdgeServer
from utils import Utils


class ServerPlacement(object):
    def __init__(self, base_stations: List[BaseStation], distances: List[List[float]]):
        self.base_stations = base_stations.copy()
        self.distances = distances
        self.edge_servers = None

    def place_server(self, edge_server_num):
        raise NotImplementedError

    def distance_edge_server_base_station(self, edge_server: EdgeServer, base_station: BaseStation) -> float:
        if edge_server.base_station_id:
            return self.distances[edge_server.base_station_id][base_station.id]
        return Utils.calc_distance(edge_server.latitude, edge_server.longitude, base_station.latitude,
                                   base_station.longitude)

    def objective_latency(self):
        assert self.edge_servers

        pass

    def objective_workload(self):
        assert self.edge_servers


class MIPServerPlacement(ServerPlacement):
    def place_server(self, edge_server_num):
        pass


class KMeansServerPlacement(ServerPlacement):
    def place_server(self, edge_server_num):
        pass


class TopKServerPlacement(ServerPlacement):
    def place_server(self, edge_server_num):
        """
        Top-K approach
        """
        sorted_base_stations = sorted(self.base_stations, key=lambda x: x.workload, reverse=True)
        edge_servers = [EdgeServer(i, item.latitude, item.longitude, item.id) for i, item in
                        enumerate(sorted_base_stations[:edge_server_num])]
        for i, base_station in enumerate(sorted_base_stations):
            closest_edge_server = None
            min_distance = 1e10
            for j, edge_server in enumerate(edge_servers):
                tmp = self.distance_edge_server_base_station(edge_server, base_station)
                if tmp < min_distance:
                    min_distance = tmp
                    closest_edge_server = edge_server
            closest_edge_server.assgined_base_stations.append(base_station)
        self.edge_servers = edge_servers


class RandomServerPlacement(ServerPlacement):
    def place_server(self, edge_server_num):
        """
        Random approach
        """
        random_base_stations = random.sample(self.base_stations, edge_server_num)
        edge_servers = [EdgeServer(i, item.latitude, item.longitude, item.id) for i, item in
                        enumerate(random_base_stations)]
        for i, base_station in enumerate(random_base_stations):
            closest_edge_server = None
            min_distance = 1e10
            for j, edge_server in enumerate(edge_servers):
                tmp = self.distance_edge_server_base_station(edge_server, base_station)
                if tmp < min_distance:
                    min_distance = tmp
                    closest_edge_server = edge_server
            closest_edge_server.assgined_base_stations.append(base_station)
        self.edge_servers = edge_servers
