import logging
import random
from datetime import datetime
from typing import List

import numpy as np
import scipy.cluster.vq as vq

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

    def objective_workload(self):
        assert self.edge_servers


class MIPServerPlacement(ServerPlacement):
    def place_server(self, edge_server_num):
        pass


class KMeansServerPlacement(ServerPlacement):
    def place_server(self, edge_server_num):
        logging.info("{0}:Start running k-means".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        # data: ndarray
        base_stations = self.base_stations
        coordinates = list(map(lambda x: (x.latitude, x.longitude), base_stations))
        data = np.array(coordinates)
        k = edge_server_num

        # k-means
        centroid, label = vq.kmeans2(data, k, iter=100, minit='points')

        # process result
        edge_servers = [EdgeServer(i, row[0], row[1]) for i, row in enumerate(centroid)]
        for bs, es in enumerate(label):
            edge_servers[es].assigned_base_stations.append(base_stations[bs])

        self.edge_servers = edge_servers
        logging.info("{0}:End running  k-means".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


class TopKServerPlacement(ServerPlacement):
    def place_server(self, edge_server_num):
        """
        Top-K approach
        """
        logging.info("{0}:Start running Top-k".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
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
            closest_edge_server.assigned_base_stations.append(base_station)
        self.edge_servers = edge_servers
        logging.info("{0}:End running Top-k".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


class RandomServerPlacement(ServerPlacement):
    def place_server(self, edge_server_num):
        """
        Random approach
        """
        base_stations = self.base_stations
        logging.info("{0}:Start running Random".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        random_base_stations = random.sample(self.base_stations, edge_server_num)
        edge_servers = [EdgeServer(i, item.latitude, item.longitude, item.id) for i, item in
                        enumerate(random_base_stations)]
        for i, base_station in enumerate(base_stations):
            closest_edge_server = None
            min_distance = 1e10
            for j, edge_server in enumerate(edge_servers):
                tmp = self.distance_edge_server_base_station(edge_server, base_station)
                if tmp < min_distance:
                    min_distance = tmp
                    closest_edge_server = edge_server
            closest_edge_server.assigned_base_stations.append(base_station)
        self.edge_servers = edge_servers
        logging.info("{0}:End running Random".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
