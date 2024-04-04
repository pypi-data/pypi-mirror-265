from agt_server.agents.base_agents.agent import Agent
import json
import pandas as pd
import threading
import pkg_resources
import numpy as np
import random
from itertools import product

class MyLSVMAgent(Agent):
    def __init__(self, name=None, timestamp=None, config_path = 'configs/handin_configs/lsvm_config.json'):
        super().__init__(name, timestamp)
        
        config_path = pkg_resources.resource_filename('agt_server', config_path)
        with open(config_path) as cfile:
            server_config = json.load(cfile)
            
        self.response_time = server_config['response_time']
        self.shape = tuple(server_config['shape']) 
        self.num_goods = np.prod(self.shape)
        self._is_national_bidder = None
        self.valuations = None
        self.min_bids = np.zeros(self.shape)
        self.current_prices = np.zeros(self.shape)
        self.regional_good = None
        self._regional_size = int(server_config['regional_size'])
       
        self._goods_to_index = MyLSVMAgent._name_goods(self.shape)
        self.goods = set(self._goods_to_index.keys())
        self._index_to_goods = {value: key for key, value in self._goods_to_index.items()}
        self._current_round = 0 
        
        self.tentative_allocation = set()
    
    def get_regional_good(self): 
        return self.regional_good
    
    def get_goods(self): 
        return self.goods 
    
    def is_national_bidder(self): 
        return self._is_national_bidder
    
    def get_shape(self): 
        return self.shape 
    
    def get_num_goods(self): 
        return self.num_goods
        
    def get_goods_to_index(self): 
        return self._goods_to_index
    
    def get_tentative_allocation(self): 
        return self.tentative_allocation
    
    def calc_utility(self, bundle):
        """
        Calculate the valuation of a bundle for the regional or national bidder.
        
        :param bundle: A set of tuples, where each tuple represents the indices in self.valuations of a good.
        :return: The valuation of the bundle.
        """
        if self._is_national_bidder:
            a = 320
            b = 10
        else:
            a = 160
            b = 4
        
        base_values = {good: self.valuations[self._goods_to_index[good]] for good in bundle}
        
        def _is_adjacent(item1, item2):
            return sum(abs(sum(self._goods_to_index[a]) - sum(self._goods_to_index[b])) for a, b in zip(item1, item2)) == 1

        def _dfs(current, visited, component, all_goods):
            visited.add(current)
            component.add(current)
            for neighbor in all_goods:
                if neighbor not in visited and _is_adjacent(current, neighbor):
                    _dfs(neighbor, visited, component, all_goods)

        def _get_partitions(all_goods):
            visited = set()
            partitions = []
            for good in all_goods:
                if good not in visited:
                    component = set()
                    _dfs(good, visited, component, all_goods)
                    partitions.append(component)
            return partitions
    
        partitions = _get_partitions(list(bundle))
        
        valuation = 0
        for C in partitions:
            partition_valuation = sum(base_values[idx] for idx in C)
            valuation += (1 + a / (100 * (1 + np.exp(b - len(C))))) * partition_valuation
        return valuation

    def calculate_tentative_utility(self): 
        return self.calc_utility(self.tentative_allocation)
        
    def get_current_round(self): 
        return self._current_round
        
    def get_goods_in_proximity(self): 
        """
        Returns the names goods that are in your proximity! Will contain all goods if you are the National Bidder.
        """
        if self._is_national_bidder:
            return list(self._index_to_goods.values())
        else:
            non_zero_indices = np.argwhere(self.valuations != 0)
            non_zero_indices_tuples = [tuple(idx) for idx in non_zero_indices]
            return [self._index_to_goods[idx] for idx in non_zero_indices_tuples if idx in self._index_to_goods]
        
    
    def proximity(self, arr = None, regional_good = None):
            """
            Gives the filtered valuation array not within 'regional_size' distance from a specified regional good in a array.

            Parameters:
            - arr: numpy array of valuations
            - regional_good: The regional good that you want to get the proximity of

            Returns:
            - masked_arr: A numpy array with elements not within 'regional_size' distance from index zeroed out.
            """
            if arr is None: 
                arr = self.valuations
            if regional_good is None: 
                regional_good = self.regional_good
            
            index = self._goods_to_index[regional_good]
            grid = np.ogrid[tuple(slice(0, max_shape) for max_shape in arr.shape)]
            distance = sum(np.abs(g - idx) for g, idx in zip(grid, index))
            masked_arr = np.where(distance <= self._regional_size, arr, 0)
            return masked_arr
    
    @staticmethod
    def _generate_sequence(alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        """
        Generator function to create an alphabet sequence that continues with AA, AB, ... after Z for the alphabet 
        but which works with any set of symbols.
        """
        yield from alphabet 
        size = 2 
        while True:
            for letters in product(alphabet, repeat=size):
                yield ''.join(letters)
            size += 1
        
    @staticmethod
    def _name_goods(shape, alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        """
        Names the goods given a world of given 'shape' using combinations of the given symbols
        """
        alphabet_generator = MyLSVMAgent._generate_sequence(alphabet)
        map_dict = {}
        total_elements = np.prod(shape)
        
        for flat_index in range(total_elements):
            multidimensional_index = np.unravel_index(flat_index, shape)
            letter = next(alphabet_generator)
            map_dict[letter] = multidimensional_index
                        
        return map_dict

    def get_valuation_as_array(self): 
        return self.valuations
    
    def get_valuation(self, good): 
        """
        Given the good as a string returns the valuation you have corresponding to that good.
        """
        return self.valuations[self._goods_to_index[good]]
    
    def get_valuations(self, bundle = None): 
        """
        Given the good as a string returns the valuation you have corresponding to that good.
        """
        if bundle is None: 
            bundle = self.goods
        return {good: self.valuations[self._goods_to_index[good]] for good in bundle}
    
    def get_min_bids_as_array(self): 
        return self.min_bids 
    
    def get_min_bids(self, bundle = None): 
        if bundle is None: 
            bundle = self.goods
        return {good: self.min_bids[self._goods_to_index[good]] for good in bundle if good in self._goods_to_index}

    def is_valid_bid_bundle(self, my_bids):
        """
        Check if my_bids is a valid bid bundle.

        :param my_bids: Dictionary mapping goods to bid values.
        :return: True if the bid bundle is valid, False otherwise.
        """
        
        if not isinstance(my_bids, dict):
            print("NOT VALID: my_bids must be of type Dict[str, float]")
            return False
        
        for good, bid in my_bids.items():
            if bid is None:
                print(f"NOT VALID: bid for good {good} cannot be None")
                return False

            if good not in self._goods_to_index or bid < self.min_bids[self._goods_to_index[good]]:
                print(f"NOT VALID: bid for good {good} cannot be less than the min bid")
                return False

            price_history = self.game_report.game_history['price_history']
            bid_history = self.game_report.game_history['my_bid_history']
            for past_prices, past_bids in zip(price_history, bid_history):
                price_diff = self.current_prices - past_prices
                bid_diff = my_bids - past_bids
                switch_cost = np.dot(price_diff, bid_diff)
                if switch_cost > 0:
                    print(f"NOT VALID: New bids are {switch_cost} relatively more expensive than maintaining the old bids, strategy is insincere")
                    return False  
        return True 
        
    def clip_bids(self, my_bids):
        """ 
        Clips all of your bids to be above the minimum bid
        """
        for good in my_bids: 
            my_bids[good] = max(my_bids[good], self.min_bids[self._goods_to_index[good]])
        return my_bids

    def clip_bid(self, good, bid): 
        """ 
        Clips your bid for `good` to be above the minimum bid
        """
        return max(bid, self.min_bids[self._goods_to_index[good]])
    
    def timeout_handler(self):
        print(f"{self.name} has timed out")
        self.timeout = True

    def handle_postround_data(self, resp):
        self.global_timeout_count = resp['global_timeout_count']
        self.curr_opps = resp['opp_names']
        self.handle_permissions(resp)

    def map_to_ndarray(self, map, object = False): 
        if object: 
            arr = np.empty(self.shape, dtype=object)
        else: 
            arr = np.zeros(self.shape)
        for item in map: 
            arr[self._goods_to_index[item]] = map[item]
        return arr

    def ndarray_to_map(self, arr): 
        return {good: arr[self._goods_to_index[good]] for good in self.get_goods()}
                        
    def get_game_report(self): 
        return self.game_report

    def get_util_history(self):
        return self.game_report.get_util_history()

    def get_last_util(self):
        return self.game_report.get_last_util()
