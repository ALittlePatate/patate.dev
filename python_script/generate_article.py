"""
~foldername~template~foldername~
~titre~Test article~titre~
~date~ Jan 25, 2022~date~
~section~Test~section~
~data~data~data~
~link~[https://www.google.com]link to google~link~
~list~Test~list~
~endlist~
~image~serverlist.png~image~
"""
#TODO : 
# - add code snippet


import os
from os import listdir
from os.path import isfile, join
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def write_file(text) :
    with open("out.html", "a") as o :
        o.write(text)

def generate_base(title) :
    base = """
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>"""+title+"""</title>
    <link rel="stylesheet" type="text/css" href="../css/styles.css"/>
</head>
<body>
    <div class="header">
        <a href="/">
            <a href="../index.html"><img alt="Spike" src="../images/spike.jpg" id="spike"></a>
        </a>
        <div class="menu">
            <a> </a>
            <a href="blog.html">the blog</a>
			<a href="//github.com/ALittlePatate">github</a>
            <a href="../pgp/key.txt">pgp key</a>
        </div>
    </div>

  <article aria-label="Content" itemscope itemtype="http://schema.org/BlogPosting">
    <h1 itemprop="name headline">"""+title+"""</h1>    
"""
    write_file(base)

def generate_date(date) :
    base = """
<time class="mono"> """+date+"""</time>

<main itemprop="articleBody" style="position: relative">
"""

    write_file(base)

def generate_paragraph(p) :
    base = "<p>"+p+"</p>"
    write_file(base)

def generate_section(s) :
    s_2 = s.replace(" ","-")
    base = '''
<h2 id="'''+s_2+'''">
    <a href="#'''+s_2+'''">'''+s+'''</a>
</h2>
'''
    write_file(base)

def generate_end_file() :
    base = '''
    <p></p></main></article>
    <footer id="foot">
		<a href="//gnu.org"><img alt="GNU/Linux" src="../images/footer/gnu_linux.png" /></a>
		<img alt="" src="../images/footer/internet-privacy.gif" />
		<a href="//torproject.org"><img alt="Tor" src="../images/footer/tor.gif" /></a>
		<a href="."><img alt="patate.dev" src="../images/footer/patate_dev.png" /></a>
	</footer>
    </html>'''
    
    write_file(base)

def generate_image(path) :
    base = '''
<p>
    <img class="center_image" src="'''+path+'''" alt="" />
</p>
'''
    write_file(base)

def set_foldername(name) :
    os.mkdir("../images/"+name)
    onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]
    for f in onlyfiles :
        if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png") or f.endswith(".ico") or f.endswith(".gif") :
            shutil.move(f, "../images/"+name+"/"+f)

def main() :
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

    name = ""
    titre = ""
    date = ""
    was_list = False
    with open(filename, "r") as a :
        for line in a.readlines() :
            
            if line.startswith("~foldername~") :
                final_line = line.replace("~foldername~","").strip()
                name = final_line
                set_foldername(final_line)

            elif line.startswith("~titre~") :
                final_line = line.replace("~titre~","").strip()
                titre = final_line
                generate_base(final_line)

            elif line.startswith("~date~") :
                final_line = line.replace("~date~","").strip()
                date = " " + final_line
                generate_date(final_line)

            elif line.startswith("~section~") :
                final_line = line.replace("~section~","").strip()
                generate_section(final_line)
            
            elif line.startswith("~image~") :
                final_line = line.replace("~image~","").strip()
                final_line = "../images/"+name+"/" + final_line
                generate_image(final_line)

            else :
                if line.startswith("~endlist~"):
                    was_list = False
                    write_file("</ul>")
                    continue

                if line.startswith("~list~") :
                    l = line.split("~list~")
                    res = ""

                    if not was_list :
                        res += "<ul>"

                    for w in l :
                        if not w == " " and not w == "" and not w == "\n":
                            res += "<li>"+w+"</li>"
                    
                    was_list = True
                    line = res

                if "~data~" in line :
                    l = line.split("~data~")
                    res = ""
                    for w in l :
                        if not w.startswith(" ") and not w.endswith(" ") and not "<li" in w :
                            res += '<code class="language-plaintext highlighter-rouge">'+w+'</code>'
                        else :
                            res += w
                    line = res

                if "~link~" in line :
                    l = line.split("~link~")
                    res = ""
                    for w in l :
                        if not w.startswith(" ") and not w.endswith(" ") and not w == "":
                            link = w.split("]")
                            if len(link) < 2 :
                                continue

                            res += '<a href="'+link[0][1:]+'" target="_blank">'+link[1]+'</a>'
                        else :
                            res += w
                    line = res

                if not was_list :
                    write_file("<p>" + line.strip() + "</p>")
                else :
                    write_file(line.strip())
    
    generate_end_file()
    shutil.move("out.html", "../pages/"+name+".html")

    base = '''\n\t\t<li><a href="'''+name+'''.html" class="article">'''+titre+'''</a></li>\n'''
    with open("../pages/blog.html", "r+") as f :
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "<!--Articles-->" in line :
                lines[i+1] = lines[i+1].strip() + base
                
        f.seek(0)
        for line in lines:
            f.write(line)

if __name__ == "__main__" :
    main()
