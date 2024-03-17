'''
Brandon Lee, 2024
This program models a market of mutually exclusive buyers and sellers where:
- their entrances into the market are Poisson arrival processes,
- they leave the market only after engaging in a transaction
- their behavior follows expected utility theory, and
- the utility of the product is nonrandom
'''

# Model specification options:
# - linear EU / risk-averse EU / prospect utility theory
# - rational / real probability weighting
# - exponential / hyperbolic time discounting

import numpy as np
from typing import Callable
import bisect

class Agent:
    product_value: float # monetary value of product

    def __init__(self, product_value: float):
        self.product_value = product_value

class ArrivalMarket:
    def __init__(
            self,
            expected_buyer_arrivals: float,
            expected_seller_arrivals: float,
            generate_buyer: Callable[[], Agent],
            generate_seller: Callable[[], Agent]
        ):
        """
        :param expected_buyer_arrivals: expected number of buyers arriving in one time unit
        :param expected_seller_arrivals: expected number of sellers arriving in one time unit
        :param generate_buyer: function to randomly generate a buyer Agent
        :param generate_seller: function to randomly generate a seller Agent
        """
        self.expected_buyer_arrivals = expected_buyer_arrivals
        self.expected_seller_arrivals = expected_seller_arrivals
        self.generate_buyer = generate_buyer
        self.generate_seller: generate_seller
    
    def run_simulation(self, time_horizon: float):
        """
        :param time_horizon: how many time units the simulation should last
        """
        buyer_pool: list[Agent] = [] # list ordered by buyer offering most to least
        seller_pool: list[Agent] = [] # list ordered by seller accepting least to most
        current_time: float = 0
        next_buyer_arrival_time: float = np.random.exponential(self.expected_buyer_arrivals)
        next_seller_arrival_time: float = np.random.exponential(self.expected_seller_arrivals)
        while True:
            # insert buyer or seller into pool when they arrive
            current_time = np.min(time_horizon, next_buyer_arrival_time, next_seller_arrival_time)
            if current_time == next_buyer_arrival_time:
                bisect.insort(buyer_pool, self.generate_buyer(), key=lambda x: -x.product_value)
                next_buyer_arrival_time = current_time + np.random.exponential(self.expected_buyer_arrivals)
            elif current_time == next_seller_arrival_time:
                bisect.insort(seller_pool, self.generate_seller(), key=lambda x: x.product_value)
                next_seller_arrival_time = current_time + np.random.exponential(self.expected_seller_arrivals)
            else:
                break

            # check pool for possible deals, finalizing them until there are no more deals
            if buyer_pool[0].product_value > seller_pool[0].product_value:
                max_price = np.min(
                    buyer_pool[0].product_value, # buyer will pay no more than their product_value
                    seller_pool[1].product_value # seller can charge no more than the next best seller's product_value
                )
                min_price = np.max(
                    seller_pool[0].product_value, # seller will charge no less than their product_value
                    buyer_pool[1].product_value # buyer can pay no less than the next best buyer's product_value
                )
