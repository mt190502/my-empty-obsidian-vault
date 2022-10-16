#!/bin/bash

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
# - lineindexname     #
# - listcount         #
# - newnotebutton     #
# - reverse           #
# - sorted            #
# - targetfile        #
# - wikilinktags      #
#######################
# Example: <%tp.user.autoindex({lineindex: "true", excludedir: "bin", indexdir: "path/", lineindexname: "INDEX1", newnotebutton: "false", sorted: "true", reverse: "true", targetfile: "index.md", wikilinktags: "name"})%>


# ~> clear last characters to avoid conflicts
excludedir=${excludedir%/}
indexdir=${indexdir%/}
targetfile=${targetfile%.md}



# ~> checkvars
checkvars() {
    count=0
    findercmd="find \"$indexdir\" -type f | grep -v \"\.touch\.md\" "

    [[ ! -n $indexdir        ]] && echo "\$indexdir not defined"    && credit=$(($credit + 1))
    [[ ! -n $targetfile      ]] && echo "\$targetfile not defined"  && credit=$(($credit + 1))
    [[ -n $excludedir        ]] && findercmd+="${excludedir:+| grep -vEi \"$excludedir}\""
    [[ -n $includedir        ]] && findercmd+="${includedir:+| grep -Ei \"$includedir}\""
    [[ $sorted == "true"     ]] && findercmd+="${sorted:+ | sort ${reverse:+-Vr}}"
    [[ -n $listcount         ]] && findercmd+="${listcount:+ | head -n $listcount}"
    [[ ! -n $wikilinktags    ]] && wikilinktags="name"
    [[ ! -n $newnotebutton   ]] && newnotebutton="true"
    [[ $credit -ge 1         ]] && exit
}



# ~> generate index
generateindex() {
    _tags=$(cat "$targetfile.md" | grep tags | head -n 1 | cut -d ' ' -f2-)
    _links=$(cat "$targetfile.md" | grep links | head -n 1 | cut -d ' ' -f2-)
    _indexname=$(cat "$targetfile.md" | grep -Po '(?<=~>\s)[\d\w\s]+(?=\s<~)' | head -n 1)
    _scriptopt=$(cat "$targetfile.md" | grep 'tp.user.autoindex')

    OLDIFS=$IFS
    IFS=$(echo -en "\n\b")
    indexlist=

    for a in $(bash -c "$findercmd"); do
        if [[ -n "$wikilinktags" ]]; then
            if [[ "$(echo $wikilinktags | cut -d ':' -f1)" == "name" ]]; then
                tmp=$(echo ${a%.md} | awk -F '/' '{print $NF}')
                indexlist+="$(echo - [[${a}\|${tmp}]])\n"
            elif [[ "$(echo $wikilinktags | cut -d ':' -f1)" == "regex" ]]; then
                tmp=$(cat "${a%.md}.md" | grep -Po "$(echo $wikilinktags | cut -d ':' -f2-)")
                indexlist+="$(echo - [[${a}\|${tmp}]])\n"
            fi
        else
            indexlist+="$(echo - [[${a}/${a%.md}]])\n"
        fi
    done

    lastfilename=$(echo -e $indexlist | tail -n 2 | grep -Po "(?<=\/).*(?=\|)" | awk -F '/' '{print $NF}' | sed 's/\.md//g' | awk '{print $1}')
    newfilenumber=$(( $(echo -e $indexlist | tail -n 2 | grep -Po "(?<=\/).*(?=\|)" | awk -F '/' '{print $NF}' | sed 's/\.md//g' | awk '{print $2}') + 1))
    [[ ! -n $lastfilename ]] && lastfilename="Note"
    newnotename="$lastfilename $newfilenumber"
    [[ $newnotebutton == "true" ]] && indexlist+="- [[${indexdir%/}/${newnotename}.md| + New Note + ]]\n"

    IFS=$OLDIFS
}



saveindexfromscratch() {
        _newcontent="""
----\n\
tags: ${_tags}\n\
links: ${_links}\n\
----\n\
<p align=\"center\" style=\"font-size: 25; font-weight: bold;\"> ~> ${_indexname} <~ </p>\n\n\
----\n\
\n\
$indexlist\
\n\
\n\
${_scriptopt}
"""
    echo -e $_newcontent > "$targetfile.md"
}



saveindexinline() {
    if [[ $(cat "$targetfile.md" | grep -o "<!--$lineindexname-->" | wc -l) != "2" ]]; then
        echo "<!--$lineindexname--> is not found in $targetfile"
        exit
    else
        scriptopt=$(cat "$targetfile.md" | sed -n "/<!--$lineindexname-->/,/<!--$lineindexname-->/p" | grep "tp\.user\.autoindex")
        sed -i "/<!--$lineindexname-->/,/<!--$lineindexname-->/c<!--$lineindexname-->\n$indexlist\n$scriptopt\n<!--$lineindexname-->" "$targetfile.md"
    fi
}



if [[ $lineindex == "true" ]]; then
    checkvars
    generateindex
    saveindexinline
elif [[ $fullyindex == "true" ]]; then
    checkvars
    generateindex
    saveindexfromscratch
else
    echo No method selected "lineindex" or "fullyindex"
fi
