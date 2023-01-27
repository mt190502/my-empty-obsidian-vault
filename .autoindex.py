import os, re, datetime
#######################
#  AVAILABLE OPTIONS  #
#######################
# - fullyindex        #
# - lineindex         #
#######################
#   AVAILABLE VARS    #
#######################
# - excludedir        #
# - indexdir          #
# - indexname         #
# - listcount         #
# - newnotebutton     #
# - reverse           #
# - targetfile        #
# - wikilinktags      #
#######################

class AutoIndex:
    def __init__(self, **kwargs):
        for a in kwargs:
            setattr(self, a, kwargs.get(a))

        # ~> clear last characters to avoid conflicts and check vars
        if self.excludedir_env != None: self.excludedir_env = self.excludedir_env.replace(chr(92), '/').rstrip("/")

        if self.indexdir_env != None: self.indexdir_env = self.indexdir_env.replace(chr(92), '/').rstrip("/")
        else: print("indexdir not defined, aborting..."); exit(0)

        if self.targetfile_env != None: self.targetfile_env = self.targetfile_env.replace(chr(92), '/').split(".md")[0]
        else: print("targetfile not defined, aborting..."); exit(0)


        # ~> script handler
        if self.fullyindex_env == self.lineindex_env: print("You must select a option: fullyindex or lineindex"); exit(0)

        # ~> generate index and apply a method
        generatedindex = self.generateindex(self.indexdir_env, self.excludedir_env, self.listcount_env, self.newnotebutton_env, self.reverse_env, self.wikilinktags_env)

        if self.fullyindex_env.lower() == "true":
            self.savefullyindex(generatedindex,self.targetfile_env)
        elif self.lineindex_env.lower() == "true":
            if self.indexname_env == None: print("indexname not defined, aborting..."); exit(0)
            self.savelineindex(generatedindex, self.indexname_env, self.targetfile_env)


    # ~> index generator
    def generateindex(self, indexdir, excludedir, listcount, newnotebutton, reverse, wikilinktags):
        # ~> get filelist
        tmp = list()
        for a in os.walk(indexdir):
            for b in a[2]:
                tmp.append(f"{a[0].replace(chr(92), '/')}/{b}")

        # ~> exclude requested dirs and files
        out = []
        for c in [a for a in tmp if not re.match(f"(.*)(.touch.md|{excludedir})(.*)", a)]:
            out.append(c)

        # ~> generate index
        indexlist = []
        for c in out:
            if c.endswith(".md"):
                with open(c, "r") as f:
                    if wikilinktags.split(":")[0] == "name":
                        indexlist.append(f"- [[{c}|{c.split('/')[-1].split('.md')[0]}]]\n")
                    elif wikilinktags.split(":")[0] == "regex":
                        try:
                            regex = re.findall(f"{wikilinktags.split(':')[1:][0]}", f.read())[0]
                        except IndexError:
                            print("indextitle not found in targetfile, use wikilinktags: \"name\" ")
                            exit()
                        else:
                            indexlist.append(f"- [[{c}|{regex}]]\n")

        indexlist.sort(key=self.naturalsortkey)

        if reverse.lower() == "true":
            tmp = indexlist[::-1]
        else:
            tmp = indexlist

        if listcount != None:
            del tmp[int(listcount):]

        if "true" in newnotebutton.split(":")[0].lower():
            try:
                tag = newnotebutton.split(':')[1]
            except:
                tag = "Note"

            if os.path.exists(f"{indexdir}/.count"):
                with open(f"{indexdir}/.count", "r+") as f:
                    tmp1 = f.read()
                    tmp2 = []
                    try:
                        for a in os.walk(f"{indexdir}"):
                            for b in a[2]:
                                if b.startswith(f"{tag} "):
                                    tmp2 += re.findall(f"{tag} (.*).md", b)
                        tmp2.sort(key=self.naturalsortkey)

                        if int(tmp1) > int(tmp2[-1]):
                            x = int(tmp2[-1]) + 1
                        elif int(tmp1) == int(tmp2[-1]):
                            x = int(tmp1) + 1
                        else:
                            x = int(tmp2[-1]) + 1
                    except IndexError:
                        x = 1

                with open(f"{indexdir}/.count", "w") as f:
                    f.write(str(x))
            else:
                with open(f"{indexdir}/.count", "w") as f:
                    f.write('1')
                    x = 1

            if "-daily" in newnotebutton.split(":")[0].lower():
                value1 = datetime.datetime.now().strftime(f'%Y/%m/{tag}')
                #value2 = datetime.datetime.now().strftime(tag)
                value2 = "-> TODAY <-"
                tmp.append(f"- [[{indexdir}/{value1}.md|{value2}]]\n")
            else:
                tmp.append(f"- [[{indexdir}/{tag} {x}.md|+ New Note +]]\n")
        return tmp



    # ~> save line based index
    def savelineindex(self, generatedindex, indexname, targetfile):
        with open(f"{targetfile}.md", "r") as f:
            g = f.readlines()

            # ~> check indexname
            if indexname == None:
                print("indexname is not defined")
                exit(0)

            # ~> get index line numbers from targetfile
            index = [x for x in range(len(g)) if g[x].strip('\n') == f'<!--{indexname}-->']
            if len(index) != 2:
                print("Wrong indexname")
                exit(0)

            # ~> find line index starter rule
            for a in g[index[0]:index[1]+1]:
                scriptopt = None
                if re.match("<%\+?tp.user.autoindex", a):
                    scriptopt = a

                if scriptopt != None:
                    del g[index[0]:index[1]+1]
                    generatedindex.insert(0, f'<!--{indexname}-->\n')
                    generatedindex.append(f"\n{scriptopt}")
                    generatedindex.append(f'<!--{indexname}-->\n')

                    for a in range(index[0], index[0] + len(generatedindex)):
                        g.insert(a, generatedindex[a-index[0]])
            f.close()

        with open(f"{targetfile}.md", "w") as f:
            f.writelines(g)
            f.close()

    def naturalsortkey(self, s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split(re.compile('([0-9]+)'), s)]

    # ~> save index from scratch
    def savefullyindex(self, generatedindex, targetfile):
        with open(f"{targetfile}.md", "r") as f:
            g = f.read()
            tags = re.findall("tags: (#.*)", g)[0]
            links = re.findall("links: (.*)", g)[0]
            title = re.findall("title: (.*)", g)[0]
            scriptopt = re.findall(".*tp.user.autoindex.*", g)
            if len(scriptopt) > 1:
                print("Wrong file configuration")
                exit(0)
            joinedlist = "".join(generatedindex).strip('\n')
            newcontent = f"""
----\n\
tags: {tags}\n\
title: {title}\n\
links: {links}\n\
----\n\
\n\
{joinedlist}\
\n\
\n\
{scriptopt[0]}
"""
            with open(f"{targetfile}.md", "w") as f:
                f.writelines(newcontent)
                f.close()


session = AutoIndex(fullyindex_env=os.environ.get("fullyindex", "false"),
            lineindex_env=os.environ.get("lineindex", "false"),
            excludedir_env=os.environ.get("excludedir", None),
            indexdir_env=os.environ.get("indexdir", None),
            indexname_env=os.environ.get("indexname", None),
            listcount_env=os.environ.get("listcount", None),
            newnotebutton_env=os.environ.get("newnotebutton", "false"),
            reverse_env=os.environ.get("reverse", "false"),
            targetfile_env=os.environ.get("targetfile", None),
            wikilinktags_env=os.environ.get("wikilinktags", "name"))