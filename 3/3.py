from util.read_input import read_input
from typing import Callable, Dict, List, Union
import sys

# Power = gamma * epsilon
def read_binary_input(f: str) -> List[List[int]]:
    return [[int(x) for x in l] for l in read_input(f)]


def bit_list_to_string(bit_list: List[int]) -> str:
    bit_list_as_strs = [str(x) for x in bit_list]
    return "".join(bit_list_as_strs)


def bit_list_to_int(bit_list: List[int]) -> int:
    return int(bit_list_to_string(bit_list), base=2)


def calc_num_ones_each_position(nums: List[List[int]]) -> Union[List[int], None]:
    if not nums:
        return None
    sums = [0 for _ in nums[0]]
    for bitlist in nums:
        for i, bit in enumerate(bitlist):
            sums[i] += bit
    return sums


def calculate_power(nums: List[List[int]]) -> int:
    sums = calc_num_ones_each_position(nums)
    if sums is None:
        return 0
    gamma_list = [str(int((num / len(nums)) >= 0.5)) for num in sums]
    epsilon_list = [str(int(num) ^ 1) for num in gamma_list]
    gamma, epsilon = [int("".join(lst), base=2) for lst in [gamma_list, epsilon_list]]
    return gamma * epsilon


filter_strategies: Dict[str, Callable[[int, int], int]] = {
    "oxygen": lambda count, num_entries: 1 if count >= num_entries / 2 else 0,
    "co2": lambda count, num_entries: 0 if count >= num_entries / 2 else 1,
}


def calculate_life_support_rating(nums: List[List[int]]) -> int:
    if not nums:
        return 0
    filtered_nums: Dict[str, int] = {}
    for filter_type, filter_func in filter_strategies.items():
        print("Calculating:", filter_type)
        remaining_nums = nums[:]
        for i in range(len(nums[0])):
            sums = calc_num_ones_each_position(remaining_nums)
            if sums is None:
                return 0
            count = sums[i]
            filter_bit = filter_func(count, len(remaining_nums))
            remaining_nums = [num for num in remaining_nums if num[i] == filter_bit]
            if len(remaining_nums) == 1:
                filtered_nums[filter_type] = bit_list_to_int(remaining_nums[0])
                break
            elif len(remaining_nums) == 0:
                print("No more numbers")
    print(filtered_nums)
    return filtered_nums["oxygen"] * filtered_nums["co2"]


if __name__ == "__main__":
    f = sys.argv[1]
    print(calculate_power(read_binary_input(f)))
    print(calculate_life_support_rating(read_binary_input(f)))
