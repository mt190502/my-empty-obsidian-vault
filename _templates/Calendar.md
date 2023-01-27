
----
tags:  #calendar  #<% moment(moment([tp.file.path(".").split("/").at(3), tp.file.path(".").split("/").at(4)-1, tp.file.path(".").split("/").at(5).split("-").at()])).format("dddd") %>  #<% moment(moment([tp.file.path(".").split("/").at(3), tp.file.path(".").split("/").at(4)-1, tp.file.path(".").split("/").at(5).split("-").at()])).format("DD-MMMM") %>  #<% moment(moment([tp.file.path(".").split("/").at(3), tp.file.path(".").split("/").at(4)-1, tp.file.path(".").split("/").at(5).split("-").at()])).format("MMMM") %>
title: <%tp.file.title%>
links: [[Indexes/DailyNotes]]
----
<span class="leftalign"> <<  [[Notes/DailyNotes/Calendar/<% moment(moment([tp.file.path(".").split("/").at(3), tp.file.path(".").split("/").at(4)-1, tp.file.path(".").split("/").at(5).split("-").at()]).format("x") - 86400000).format("YYYY/MM/DD-MMMM-dddd") %>|<% moment(moment([tp.file.path(".").split("/").at(3), tp.file.path(".").split("/").at(4)-1, tp.file.path(".").split("/").at(5).split("-").at()]).format("x") - 86400000).format("DD-dddd") %>]] <div class="centeralign"> <% moment(parseInt(moment([tp.file.path(".").split("/").at(3), tp.file.path(".").split("/").at(4)-1, tp.file.path(".").split("/").at(5).split("-").at()]).format("x"))).format("DD-dddd") %> <span class="rightalign"> [[Notes/DailyNotes/Calendar/<% moment(parseInt(moment([tp.file.path(".").split("/").at(3), tp.file.path(".").split("/").at(4)-1, tp.file.path(".").split("/").at(5).split("-").at()]).format("x")) + 86400000).format("YYYY/MM/DD-MMMM-dddd") %>|<% moment(parseInt(moment([tp.file.path(".").split("/").at(3), tp.file.path(".").split("/").at(4)-1, tp.file.path(".").split("/").at(5).split("-").at()]).format("x")) + 86400000).format("DD-dddd") %> ]] >>

----

> [!todo] Tasks
> - [ ] 