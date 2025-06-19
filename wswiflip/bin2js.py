'''
Created on 23 sept. 2023

@author: a030466

This utility for creating java file containing uint8arrays of bin files contained in  dir'''

import sys
import os, os.path as path

def usage(progname):
    progshort = path.basename(progname)
    #print(f"usage : python {progshort} input_bin_file start_addr offset_addr")
    print(f"usage : {progshort} input_bin_dir ")


    
if __name__ == '__main__':   
    #print ("Start...")
    try:
        inputdirname=sys.argv[1]
    except:
        usage(sys.argv[0])
        print("...Abort")
        sys.exit()
    
    if not path.isdir(inputdirname):
        print ( inputdirname + "Directory not found... Abort")    
        sys.exit()

    # print("coucou")
    # print(os.listdir(inputdirname))
    # print(inputdirname)
    
    print("gameBin = {")
    for filename in os.listdir(inputdirname):
        if path.isfile(os.path.join(inputdirname, filename)) and filename.lower().endswith(".bin"):
            #print(filename , os.path.join(inputdirname, filename))
            with open(os.path.join(inputdirname, filename), 'rb') as fb: # open in readonly mode
               bn = fb.read()
               #print("{")
               print(f"\"{filename}\": new Uint8Array(")
               bnr = [b for b in bn]
               
               print(bnr)
               #print(type(bn))
               #print("])},")
               print("),")
               fb.close() 
    print("}")
    # with open(inputfilename, "rb") as fb:
    #     bn = fb.read()
    #
    # # print(type(bn))
    # # print(bn)
    # # print([b for b in bn])
    # bnr = bytes([(255-b) for b in reversed(bn) ])
    # #sys.stdout.buffer.write(bytes(reversed(bn)))
    # sys.stdout.buffer.write(bnr)