import numpy as np
import pandas as pd

# for a clearing price to be found, each buyer/seller must have a unique product_value
def find_clearing_price(buyer_product_values, seller_product_values):
    # make sure there are not no buyers or sellers
    if len(buyer_product_values) == 0 or len(seller_product_values) == 0: return None

    # create an array of significant values that could serve as the bounds of the clearing price interval
    significant_values = np.sort(np.concatenate([buyer_product_values, seller_product_values]))
    epsilon = np.max(significant_values[1:] - significant_values[:significant_values.size-1])/10
    minus_one = significant_values-epsilon
    plus_one = significant_values+epsilon
    significant_values = np.sort(np.concatenate([significant_values, minus_one, plus_one]))
    
    clearing_max_index = significant_values.size-1
    # lower clearing_max while quantity demanded < quantity supplied
    while ((np.sum(buyer_product_values >= significant_values[clearing_max_index])
           != np.sum(seller_product_values <= significant_values[clearing_max_index]))
           and clearing_max_index > 0):
        clearing_max_index -= 1
    
    clearing_min_index = 0
    # increase clearing_min while quantity demanded > quantity supplied
    while ((np.sum(buyer_product_values >= significant_values[clearing_min_index])
           != np.sum(seller_product_values <= significant_values[clearing_min_index]))
           and clearing_min_index < significant_values.size-1):
        clearing_min_index += 1

    # return solution interval
    if clearing_max_index < clearing_min_index: return None
    min_bound = significant_values[clearing_min_index]
    max_bound = significant_values[clearing_max_index]
    return [min_bound, max_bound]

def find_median_clearing_price(buyer_product_values, seller_product_values):
    price = find_clearing_price(buyer_product_values, seller_product_values)
    if price: return np.mean(price)
    else: return None

def run_example(rand_seed=int(np.random.random()*1000)):
    np.random.seed(rand_seed)

    # the max prices buyers are willing to pay, sorted from strong to weak
    buyer_product_values = np.sort(np.random.random(size=np.random.randint(1,5)))[::-1]
    # the min prices sellers are willing to accept, sorted from strong to weak
    seller_product_values = np.sort(np.random.random(size=np.random.randint(1,5)))[::-1]

    print("seed:", rand_seed)
    print("buyer_product_values:")
    print(buyer_product_values)
    print("seller_product_values:")
    print(seller_product_values)
    print("clearing price interval:")
    print(find_clearing_price(buyer_product_values, seller_product_values))
    print("median clearing price:")
    print(find_median_clearing_price(buyer_product_values, seller_product_values))