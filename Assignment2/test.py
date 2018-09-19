"""
My TESTING SCRIPT
"""
import os

j = 1
# test series I: 7 tests on incorrect input file samples
print("\nTEST SERIES I: Incorrect files\n")
print("test {} starts".format(j))
for i in range(1, 7 + 1):
    print("$ python3 polygons.py -print --file incorrect_{}.txt".format(i))
    os.system("python3 polygons.py -print --file incorrect_{}.txt".format(i))
print("test {} ends\n".format(j))
j += 1

# test series II: 8 tests on wrong input file samples
print("\nTEST SERIES II: Wrong files\n")
print("test {} starts".format(j))
for i in range(1, 8 + 1):
    print("$ python3 polygons.py -print --file wrong_{}.txt".format(i))
    os.system("python3 polygons.py -print --file wrong_{}.txt".format(i))
print("test {} ends\n".format(j))
j += 1

# test series III: 14 tests on wrong input file samples
print("\nTEST SERIES III: Valid polygons files\n")
print("test {} starts".format(j))
for i in range(1,14 + 1):
    print("$ python3 polygons.py --file polys_{}.txt".format(i))
    os.system("python3 polygons.py --file polys_{}.txt".format(i))
    #os.system("python3 polygons_.py --file polys_{}.txt".format(i))

print("test {} ends\n".format(j))
j += 1

# valid polygons diff test:
# if passed no info will show here
print("~~~~~~~ diff test output ~~~~~~~\n")
for i in range(1, 14+1):
    r = os.popen("diff polys_{}_output.txt polys_{}_output_.txt".format(i, i))  # 执行该命令
    info = r.readlines()  # 读取命令行的输出到一个list
    for line in info:  # 按行遍历
        line = line.strip("\r\n")
        print(line)
print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

print("\n\n==== actual marks on CSE ====\n")
# show marks: this is gen on cse machine, download it and review
with open("5137858.results.txt") as f:
    print(f.read())
