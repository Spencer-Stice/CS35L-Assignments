#!/usr/bin/python

"""
Implementation of shuf command in Python 3 with limited functionalities. Written by Spencer Stice.
"""

import random, sys, string, argparse

version_msg = "%prog 2.0"
usage_msg = """shuf [OPTION]... [FILE]
  or:  shuf -e [OPTION]... [ARG]...
  or:  shuf -i LO-HI [OPTION]..."""
description_msg = """Write a random permutation of the input lines to standard output.

                      With no FILE, or when FILE is -, read standard input."""
parser = argparse.ArgumentParser(usage=usage_msg, description=description_msg)

class processfiles:
    def __init__(self, filename):
        try:
            f = open(filename, 'r')
            self.lines = f.readlines()
            f.close()
        except IOError as e:
            errno, strerror = e.args
            parser.error("I/O error({0}): {1}".
                     format(errno, strerror))    

    def chooseline(self, lines):
        return random.choice(lines)

    def getlines(self):
        return len(self.lines)

class processothers:
    def __init__(self):
        pass
    
    def chooseline(self, lines):
        return random.choice(lines)
        

def main():

    parser.add_argument('--echo','-e', dest="echo", nargs="*", action="extend",
                        help='Use command line inputs')
    parser.add_argument('--head-count', '-n', dest="count", type=int, help="Limit the number of results to n")
    parser.add_argument('file', default=sys.stdin, nargs='?', help="Use file as input")
    parser.add_argument('--input-range', '-i', type=str, dest="numrange", help="Output LO-HI permutations")
    parser.add_argument('--repeat','-r', action='store_true', dest="rep", help="Allow repeat lines")
    parser.add_argument('-', required=False, action='store_true', dest="infromstdin", help="Read from stdin")
#    parser.add_argument('', required=False, action='store_true', dest="infromstdin2", help="Read from stdin")
    args, unknown = parser.parse_known_args()

    if(isinstance(args.echo, list) and isinstance(args.numrange, str)):
        sys.exit("Cannot use -e and -i options together\n")
    
    if(isinstance(args.numrange, str)):
        dashtimes = args.numrange.count("-")
        if dashtimes != 1:
            sys.exit("Invalid range")
        numbers = args.numrange.split("-")
        match numbers:
            case [a, b]:
                pass
            case _:
                sys.exit("Invalid range")
        a = int(a)
        b = int(b)
        if a >= b:
            sys.exit("Invalid range")
        if a < 0 or b < 0:
            sys.exit("Invalid range")
        mylist = []
        for i in range(len(numbers)):
            numbers[i] = int(numbers[i])
        for i in range(numbers[0], numbers[1] + 1):
            mylist.append(i)
        generator2 = processothers()
        innumlines = len(mylist)
        if(isinstance(args.count, int)):
           maxlines = args.count - 1
           if args.count < 0:
               sys.exit("Invalid head count")
        else:
            maxlines = innumlines
        if(isinstance(args.count, int) and args.rep == True):
            maxlines = args.count - 1
            i = 0
            while True:
                if i > maxlines:
                    break
                curr_line = generator2.chooseline(mylist)
                sys.stdout.write(str(curr_line))
                sys.stdout.write('\n')
                i = i +1
        elif(args.rep == True):
            while True:
                sys.stdout.write(str(generator2.chooseline(mylist)))
                sys.stdout.write('\n')
        else:
            for i in range(innumlines):
                if i > maxlines:
                    break
                curr_line = generator2.chooseline(mylist)
                sys.stdout.write(str(curr_line))
                sys.stdout.write('\n')
                mylist.remove(curr_line)
            
    elif(isinstance(args.echo, list)):
        ins = args.echo
        generator2 = processothers()
        for i in range(len(unknown)):
            ins.append(unknown[i])
        if len(unknown) > 0 or len(args.echo) == 0:
            ins.append(args.file)
        innumlines = len(args.echo)
        if(isinstance(args.count, int)):
            maxlines = args.count - 1
            if args.count < 0:
               sys.exit("Invalid head count")
        else:
            maxlines = innumlines
        if(isinstance(args.count, int) and args.rep == True):
            index = 0
            while True:
                if index > maxlines:
                    break
                curr_line = generator2.chooseline(ins)
                sys.stdout.write(curr_line)
                sys.stdout.write('\n')
                index = index + 1
        elif(args.rep == True):
            while True:
                sys.stdout.write(generator2.chooseline(ins))
                sys.stdout.write('\n')
        else:
            for index in range(innumlines):
                if index > maxlines:
                    break
                curr_line = generator2.chooseline(ins)
                sys.stdout.write(curr_line)
                sys.stdout.write('\n')
                ins.remove(curr_line)
    elif(isinstance(args.file, str)):
        input_file = args.file
        generator = processfiles(input_file)
        innumlines = generator.getlines()

        if(isinstance(args.count, int)): 
            maxlines   = args.count - 1
            if args.count < 0:
               sys.exit("Invalid head count")
        else:
            maxlines = innumlines
        if(isinstance(args.count, int) and args.rep == True): 
            maxlines = args.count - 1
            index = 0
            while True:
                if index > maxlines:
                    break
                curr_line = generator.chooseline(generator.lines)
                sys.stdout.write(curr_line)
                index = index + 1
        elif(args.rep == True):
            while True:
                curr_line = generator.chooseline(generator.lines)
                sys.stdout.write(curr_line)
        else:
            for index in range(innumlines):
                if index > maxlines:
                    break
                curr_line = generator.chooseline(generator.lines)
                sys.stdout.write(curr_line)
                generator.lines.remove(curr_line)
    elif(args.infromstdin == True or (~isinstance(args.file, str) and ~isinstance(args.numrange, list) and ~
                                      isinstance(args.echo, str))):
        mylines = []
        for line in sys.stdin:
            mylines.append(line)
        generator = processothers()
        innumlines = len(mylines)

        if(isinstance(args.count, int)): 
            maxlines   = args.count - 1
            if args.count < 0:
               sys.exit("Invalid head count")
        else:
            maxlines = innumlines
        if(isinstance(args.count, int) and args.rep == True): 
            maxlines   = args.count - 1
            index = 0
            while True:
                if index > maxlines:
                    break
                curr_line = generator.chooseline(mylines)
                sys.stdout.write(curr_line)
                index = index + 1
        elif(args.rep == True):
            while True:
                curr_line = generator.chooseline(mylines)
                sys.stdout.write(curr_line)
        else:
            for index in range(innumlines):
                if index > maxlines:
                    break
                curr_line = generator.chooseline(mylines)
                sys.stdout.write(curr_line)
                mylines.remove(curr_line)
                
if __name__ == "__main__":
    main()
