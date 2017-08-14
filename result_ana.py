# -*- coding: utf-8 -*-
# author Bao Ning
''' 
input : .req file
function : block is identified by original block id + update times
output : a ranklist of traces, the request lists in time windows of each blocks
# 
'''

import sys

LINE_LENGTH=48
IGNORE_CASES=["m", "P", "U", "X", "UT"]

def loadfile(filename):
    fin = open(filename, 'r')
    # fop = open("./filebench_fileserver/test1_copy.txt", 'w')
    i = 0
    e1 = 0
    l1 = []
    e2 = 0
    l2 = []
    action_dict = {}
    ios = 0
    for line in fin.readlines():
        # fop.write(line)
        i += 1
        # message = line[LINE_LENGTH:]
        # line = line[:LINE_LENGTH]       
        items = line.strip().split()
        # items from 0 to 6 are : 0 major,minor number; 1 #cpu; 2 #sequence;
        # 3 timestamp; 4 pid; 5 action; 6 R/W

        # the end part of the trace
        if(len(items)<7):
            # print("error", line)          
            # print(items)
            # print(i)
            break

        action = items[5]
        rw = items[6]
        message = line[line.find(items[7], LINE_LENGTH):]

        # print("items=", items, "action=", action, "rw=", rw)
        

        if action != "Q":
            continue

        # if rw == "N" or action in IGNORE_CASES:
        #     if "+" in message:
        #         e1 += 1
        #         l1.append(i)
        #     continue

        if "+" not in message:
            e2 += 1
            l2.append(i)
            continue

        blocks = message.strip().split()
        b_st = blocks[0]
        nrb = blocks[2]
        blkey = (b_st, nrb, rw)
        # print(i, nrb, blocks)
        ios = ios + int(nrb)

        # if blkey in action_dict:
        #     blv = action_dict[blkey]
        #     action_dict[blkey] = blv.append(action)
            # print("bstart=", b_st, "nr of b=", nrb)

            
        # if action in IGNORE_CASES:
        #   if "+" in message:
        #       print("+ in m", i, line, message)
        # else:
        #   if "+" not in message:
        #       print("+ not in !m", i, line, message)
        # if i%10000==0:
        #   print(line)         
        #   print(items)

        
        
    #   index = line.find("thresh = ") 
    #   if index < 0:
    #       continue
    #   # print(index)      
    #   lines = line[index:].split(',')
    #   # print(lines)
    #   thresh = int(lines[0][9:])
    #   bg_thresh = int(lines[1][12:])
    #   limit = int(lines[2][8:])
    #   wb_thresh = int(lines[3][12:])
    #   # print(thresh)
    #   # print(wb_thresh)
    #   total += 1
    #   if thresh == wb_thresh:
    #       equal += 1
    #   if bg_thresh == int(thresh/2):
    #       half += 1
    #   if limit > thresh:
    #       limitLarge += 1
    print("end", i)
    print("e1=", e1, "e2=", e2)
    print("l1=", l1)
    print("l2=", l2)
    print("number of io blocks=", ios)
    fin.close()
    # for key in action_dict.keys():
    #     value = action_dict[key]
    #     if "Q" not in value:
    #         print("key-value error", key, value)

    # fop.close()

loadfile("./filebench_fileserver/test1.txt")
