#
# @lc app=leetcode.cn id=2 lang=python3
#
# [2] 两数相加
#
# https://leetcode-cn.com/problems/add-two-numbers/description/
#
# algorithms
# Medium (35.49%)
# Likes:    2962
# Dislikes: 0
# Total Accepted:    196.2K
# Total Submissions: 552.7K
# Testcase Example:  '[2,4,3]\n[5,6,4]'
#
# 给出两个 非空 的链表用来表示两个非负的整数。其中，它们各自的位数是按照 逆序 的方式存储的，并且它们的每个节点只能存储 一位 数字。
# 
# 如果，我们将这两个数相加起来，则会返回一个新的链表来表示它们的和。
# 
# 您可以假设除了数字 0 之外，这两个数都不会以 0 开头。
# 
# 示例：
# 
# 输入：(2 -> 4 -> 3) + (5 -> 6 -> 4)
# 输出：7 -> 0 -> 8
# 原因：342 + 465 = 807
# 
# 
#
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:

        def str_lst(ll):
            a1 = []
            while(ll):
                a1.append(ll.val)
                ll=ll.next
            ll_reverse = sorted(a1, reverse=True)
            return [str(i) for i in ll_reverse]
        a = int(''.join(str_lst(l1)))
        b = int(''.join(str_lst(l2)))
        c = list(str(a + b))
        # 新建两个空链表
        tmp_node=ListNode(None)
        node=ListNode(None) 
        # 从后往前遍历和字符串，插入链表
        for x in c[::-1]:
            #print(x)
            if not tmp_node.val:
                tmp_node.val=x
                node=tmp_node
                #print(node)
            else:
                tmp_node.next=ListNode(x)
                tmp_node=tmp_node.next
        return node

