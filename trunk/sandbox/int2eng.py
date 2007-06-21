#!/usr/bin/python
# http://www.itasoftware.com/careers/puzzles07.html


unique = {
           1: "one",
           2: "two",
           3: "tree",
           4: "four",
           5: "five",
           6: "six",
           7: "seven",
           8: "eight",
           9: "nine",
          10: "ten",
          11: "eleven",
          12: "twelve",
          13: "thirteen",
          15: "fifteen",
          20: "twenty",
          30: "thirty",
          40: "forty",
          50: "fifty",
          60: "sixty",
          70: "seventy",
          80: "eighty",
          90: "ninety",
         }

tenpower_postfixes = {1: "teen", 2: "hundred", 3: "thousand",
                      6: "million", 9: "billion"}

def factorize(value, base=10):
    while value != 0:
        rem = value % base
        value = (value - rem) // base
        yield rem

def defactorize(values, base=10, bigendian=True):
    if not bigendian:
        values.reverse()
    res = 0
    for e, i in enumerate(values):
        res += i * base ** e
    return res

def int2str0(value):
    if value < 10 and value in unique:
        return unique[value]
    else:
        return ""

def int2str1(value):
    if int2str0(value):
        return int2str0(value)
    elif 10 <= value < 20:
        if value in unique:
            return unique[value]
        else:
            return unique[value % 10] + tenpower_postfixes[1]
    else:
        return ""

def int2str2(value):
    if int2str1(value):
        return int2str1(value)
    elif 20 <= value < 100:
        if value in unique:
            return unique[value]
        else:
            return unique[value - value % 10] + unique[value % 10]
    else:
        return ""

def int2str3(value):
    if int2str2(value):
        return int2str2(value)
    elif 10**2 <= value < 10**3:
        return int2str2(value // 10**2) + tenpower_postfixes[2] + int2str2(value % 10**2)
    else:
        return ""

def int2str4(value):
    if int2str3(value):
        return int2str3(value)
    elif 10**3 <= value < 10**6:
        return int2str3(value // 10**3) + tenpower_postfixes[3] + int2str3(value % 10**3)
    else:
        return ""

def int2str6(value):
    if int2str4(value):
        return int2str4(value)
    elif 10**6 <= value < 10**9:
        return int2str4(value // 10**6) + tenpower_postfixes[6] + int2str4(value % 10**6)
    else:
        return ""

def int2str(value):
    res = int2str6(value)
    if res:
        return res
    else:
        return "Converter missing!"
        

if __name__ == "__main__":
    print list(factorize(123)), defactorize(factorize(123))
    mean = 3.0
    c = 0
    for i in xrange(1,999999999,110881):
        c += 1
        print i, mean
        mean = (mean * (c-1) + len(int2str(i))) / c
    print "Media primi %s numeri: %s" % (c, mean)
