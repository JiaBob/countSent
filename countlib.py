import sys, re, os, chardet

def countBoth_ch(string):
    subsum=0
    phrase=0
    token=0
    for word in string:
        if re.match(r'[\u3002\uff01\uff1f]', word):
            subsum += 1
            token = 1
        elif re.match(r'\n', word)and token==0:
            phrase += 1
            token=0
        else:
            token=0
    return (subsum,phrase//2)

#unfinished
def countBoth_po(string):
    subsum = 0
    phrase = 0
    token = 0
    for word in string:
        if re.match(r'[\u3002\uff01\uff1f]', word):
            subsum += 1
            token = 1
        elif re.match(r'\n', word) and token == 0:
            phrase += 1
            token = 0
        else:
            token = 0
    return (subsum, phrase//2)


