l1 = [1,2,3,4,5]
l1.sort(reverse=True)
l2 = [3,4,5]
l2.sort(reverse=True)

l1_res = int(''.join(l1))
l2_res = int(''.join(l2))
l3 = str(l1_res + l2_res)
l3_res = l3.split(',')

print(l3_res)