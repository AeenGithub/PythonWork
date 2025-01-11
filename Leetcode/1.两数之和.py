#
# @lc app=leetcode.cn id=1 lang=python3
#
# [1] 两数之和
#
class Solution:
    def twoSum(self, nums, target):
        dict_nums = {}
        for x_index, x in enumerate(nums):
            y = target - x
            for key, value in dict_nums.items():
                if y == value:
                    return [key, x_index]
            dict_nums[x_index] = x

