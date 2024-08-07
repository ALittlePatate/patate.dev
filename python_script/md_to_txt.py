# Script used to convert t/prog manifesto from md to txt

import sys
import re

if len(sys.argv) != 2 :
    print(f"Usage: python {sys.argv[0]} file.md")

def keep_bracket_content(text):
    pattern = r'\[(.*?)\]\(.*?\)'
    new_text = re.sub(pattern, r'\1', text)
    return new_text
    
with open(sys.argv[1], "r") as f :
    with open("out.txt", "w") as o :
        for l in f.readlines() :
            l = l.replace("**", "")
            i = 0
            for i in range(len(l)) :
                if l[i] != '#' and l[i] != ' ':
                    break
            l = l[i:]
            l = keep_bracket_content(l)
            o.write(l)