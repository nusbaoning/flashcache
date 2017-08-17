# -*- coding: utf-8 -*-
# author Bao Ning
''' 
input : .req file
function : block is identified by original block id + update times
output : a ranklist of traces, the request lists in time windows of each blocks
# 
'''

import sys
import math
import mts_cache_algorithm
import numpy

LINE_LENGTH=48
IGNORE_CASES=["m", "P", "U", "X", "UT"]
ucln = 1030900
# for 1min fileserver 29486
# for 100min fileserver 568921

# result for 100min fileserver
# ('number of io blocks=', 29986400)
# read/write type 50271 516332 568921
# hit ratio 59123 3631110 0.0162823489236
# write numbers 1.03221769652 0.325566832334

# result for 4G memory 100min fileserver
# ('number of io blocks=', 218169232)
# read/write type 0.0189358812688 0.689398583762 1030900
# hit ratio 32215 1053650 26110062 0.0403541745707
# write numbers 1.04437132321 0.0525101830839


ssdSize = ucln>>5

def parsefile(filename):
    fin = open(filename, 'r')
    fop = open("./filebench_fileserver/text1_shorter2.txt", 'w')
    print "open file"
    i = 0
    nrline = 0
    for line in fin.readlines():            
        items = line.strip().split()
        i+=1
        if(len(items)<7):
            break
        action = items[5]
        rw = items[6]
        if action != "Q":
            continue
        # if "+" not in message:
        #     continue
        
        if i%10000==0:
            print i, 1.0*i/34378018
        fop.write(line)
    fin.close()
    fop.close()

def loadfile(filename):
    fin = open(filename, 'r')
    # fop = open("./filebench_fileserver/test1_copy.txt", 'w')
    i = 0   
    j = 0
    # tmp = 0 
    e2 = 0
    l2 = []
    ssd = mts_cache_algorithm.LRU(size=ssdSize)
    NrSsdHit = 0
    LtCacheUp = []
    rwTypeDict = {}
    # rwset = set([])
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


        j += 1
        # if rw == "N" or action in IGNORE_CASES:
        #     if "+" in message:
        #         e1 += 1
        #         l1.append(i)
        #     continue

        if "+" not in message:
            e2 += 1
            l2.append(i)
            continue

        # rwset.add(rw)

        blocks = message.strip().split()
        b_st = int(blocks[0])
        nrb = int(blocks[2])
        blkey = (b_st, nrb, rw)
        # print(i, nrb, blocks)
        ios = ios + int(nrb)

        # parse 512B block to 4KB page
        # print(b_st, nrb)
        # print(b_st>>3, math.ceil(nrb/8))
        start = b_st>>3
        end = start + int(math.ceil(nrb/8))
        # print(start, end)
        if "W" in rw:
            r = 0
            w = True
        elif "R" in rw:
            r = 1
            w = False
        else:
            print("error", rw)

        for page in range(start,end):
            if page in rwTypeDict:
                (rv,wv) = rwTypeDict[page]
            else:
                rv, wv = (0, 0)
            rwTypeDict[page] = (rv+r, wv+1-r)
            ssd.is_hit(page)
            node = ssd.update_cache(page, w)
            if node is not None:
                if node.hit is True:
                    NrSsdHit += 1
                LtCacheUp.append(node.update)

        
        

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
    print "end", i, j
    print("e2=", e2)
    print("l2=", l2)
    print("number of io blocks=", ios)
    # print(rwset)
    fin.close()
    ro = 0
    wo = 0
    ucln = len(rwTypeDict)
    for key in rwTypeDict.keys():
        rv, wv = rwTypeDict[key]
        total = rv+wv
        if rv/total >= 0.95:
            ro += 1
        elif wv/total >= 0.95:
            wo += 1
    l = ssd.get_top_n(ssdSize)
    for hit,update in l:
        if hit is True:
            NrSsdHit += 1
        LtCacheUp.append(update)
    
    print "read/write type", 1.0*ro/ucln, 1.0*wo/ucln, ucln 
    print "hit ratio", ssdSize, NrSsdHit, ssd.update, float(NrSsdHit)/ssd.update
    # print LtCacheUp
    print "write numbers", numpy.mean(LtCacheUp), numpy.var(LtCacheUp)
    # for key in action_dict.keys():
    #     value = action_dict[key]
    #     if "Q" not in value:
    #         print("key-value error", key, value)

    # fop.close()

loadfile("./filebench_fileserver_4Gmem_100min/test1_short.txt")
# loadfile("./filebench_fileserver/test1_short.txt")
# parsefile("./filebench_fileserver/test1.txt")