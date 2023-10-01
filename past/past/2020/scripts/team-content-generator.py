import os
os.system(
    "curl \"https://docs.google.com/spreadsheets/d/1tS_AHvttsNA7WVVQjaR8Wv1kEpn-DmuzI5Ld2A0XPQc/export?gid=1088795641&format=tsv\" > team.tsv"
)

readFile = open("team.tsv")
writeFile = open("../team-container-content.html", 'w')

# print >> writeFile, "<h1 class=\"section-title\">Leadership</h1> \n\
#   <p>Click on each profile to read the bio!</p> \n\
#   <div class=\"table-of-contents\"> \n\
#     <a href=\"#directors\" class=\"table-link\">Directors</a> \n\
#     <a href=\"#content\" class=\"table-link\">Content</a> \n\
#     <a href=\"#finance\" class=\"table-link\">Finance</a> \n\
#     <a href=\"#logistics\" class=\"table-link\">Logistics</a> \n\
#     <a href=\"#outreach\" class=\"table-link\">Outreach</a> \n\
#     <a href=\"#communications\" class=\"table-link\">Communications</a> \n\
#     <a href=\"#graphics\" class=\"table-link\">Graphic Design</a> \n\
#     <a href=\"#webmaster\" class=\"table-link\">Webmaster</a> \n\
#     <a href=\"#emeritus\" class=\"table-link\">Emeriti</a> \n\
#     <a href=\"#events\" class=\"table-link\">Event Supervisors</a> \n\
#   </div> \n"
writeFile.write("<h1 class=\"section-title\">Leadership</h1> \n\
  <p>Click on each profile to read the bio!</p> \n\
  <div class=\"table-of-contents\"> \n\
    <a href=\"#directors\" class=\"table-link\">Directors</a> \n\
    <a href=\"#content\" class=\"table-link\">Content</a> \n\
    <a href=\"#finance\" class=\"table-link\">Finance</a> \n\
    <a href=\"#logistics\" class=\"table-link\">Logistics</a> \n\
    <a href=\"#outreach\" class=\"table-link\">Outreach</a> \n\
    <a href=\"#communications\" class=\"table-link\">Communications</a> \n\
    <a href=\"#graphics\" class=\"table-link\">Graphic Design</a> \n\
    <a href=\"#webmaster\" class=\"table-link\">Webmaster</a> \n\
    <a href=\"#emeritus\" class=\"table-link\">Emeriti</a> \n\
    <a href=\"#events\" class=\"table-link\">Event Supervisors</a> \n\
  </div> \n")

# print >> writeFile, "\t<div id=\"profiles\">"
writeFile.write("\t<div id=\"profiles\">")

newSection = True
printDescription = False
printPerson = False
printRow = True  # True = need to print a new Row
printEventSupervisors = False

lines = readFile.readlines()
numLines = len(lines)
print(numLines)
for organizerNum in range(numLines):
    x = lines[organizerNum].split('\t')
    if x[1].strip() == 'events':
        printEventSupervisors = True
    if x[0].strip() == "":
        if not printRow:
            # print >> writeFile, "\t\t</div>"
            writeFile.write("\t\t</div>")
            printRow = True
        # print >> writeFile, ""
        writeFile.write("")
        newSection = True
        printPerson = False
    elif newSection:
        newSection = False
        printDescription = True
        printPerson = True
        # print >> writeFile, "\t\t<h2 class=\"section-subtitle\" id=\"{}\">{} <i class=\"fa fa-angle-up\" id=\"scroll-top\" data-toggle=\"tooltip\" data-placement=\"right\" title=\"Scroll to top\" aria-hidden=\"true\"></i></h2>".format(
        #     x[1], x[0])
        writeFile.write("\t\t<h2 class=\"section-subtitle\" id=\"{}\">{} <i class=\"fa fa-angle-up\" id=\"scroll-top\" data-toggle=\"tooltip\" data-placement=\"right\" title=\"Scroll to top\" aria-hidden=\"true\"></i></h2>".format(
              x[1], x[0]))
    elif printDescription:
        printDescription = False
    #     print >> writeFile, "\t\t<div class=\"col-md-12\"> \n\
    #   <p class=\"section-description\">{}</p> \n\
    # </div>".format(x[0])
        writeFile.write("\t\t<div class=\"col-md-12\"> \n\
      <p class=\"section-description\">{}</p> \n\
    </div>".format(x[0]))

    elif printPerson:
        if printEventSupervisors:
            break
        hasTitle = False
        title = ""
        name = "-".join([temp.strip().lower() for temp in x[0].split(" ")])
        if x[2] != "":
            hasTitle = True
            title = x[2].split(",")
        if printRow:
            # print >> writeFile, "\t\t<div class=\"row\">"
            writeFile.write("\t\t<div class=\"row\">")
        # print >> writeFile, "\t\t\t<div class=\"col-md-6\"> \n\
        #   <ul class=\"list-group\"> \n\
        #     <li class=\"list-group-item\" data-toggle=\"collapse\" href=\"#{}-bio\" aria-expanded=\"false\"> \n\
        #       <div class=\"profile-main\"> \n\
        #         <img src=\"img/bios/{}.jpg\" alt=\"{}\"> \n\
        #         <div class=\"description\"> \n\
        #           <div class=\"profile-name\">{} '{}</div>".format(
        #     name.strip(), name.strip(), x[0].strip(), x[0].strip(),
        #     x[1].strip())
        writeFile.write("\t\t\t<div class=\"col-md-6\"> \n\
          <ul class=\"list-group\"> \n\
            <li class=\"list-group-item\" data-toggle=\"collapse\" href=\"#{}-bio\" aria-expanded=\"false\"> \n\
              <div class=\"profile-main\"> \n\
                <img src=\"img/bios/{}.jpg\" alt=\"{}\"> \n\
                <div class=\"description\"> \n\
                  <div class=\"profile-name\">{} '{}</div>".format(
            name.strip(), name.strip(), x[0].strip(), x[0].strip(),
            x[1].strip()))

        if title != "":
            for tit in title:
                # print >> writeFile, "\t\t\t\t\t\t\t\t\t<div class=\"profile-title\">{}</div>".format(tit.strip())
                writeFile.write("\t\t\t\t\t\t\t\t\t<div class=\"profile-title\">{}</div>".format(tit.strip()))

        # print >> writeFile, "\t\t\t\t\t\t\t\t</div> \n\
        #       </div> \n\
        #       <div class=\"collapse profile-bio\" id=\"{}-bio\"> \n\
        #         {} \n\
        #       </div> \n\
        #     </li> \n\
        #   </ul> \n\
        # </div>".format(name.strip(), x[3].strip())
        writeFile.write("\t\t\t\t\t\t\t\t</div> \n\
              </div> \n\
              <div class=\"collapse profile-bio\" id=\"{}-bio\"> \n\
                {} \n\
              </div> \n\
            </li> \n\
          </ul> \n\
        </div>".format(name.strip(), x[3].strip()))

        if printRow:
            printRow = False
            continue
        if not printRow:
            # print >> writeFile, "\t\t</div>"
            writeFile.write("\t\t</div>")
            printRow = True

if printEventSupervisors:
    for supervisorNum in range(numLines - organizerNum):
        x = lines[organizerNum + supervisorNum].split('\t')
        name, year, event, team = [x[i].strip() for i in range(4)]
        school = '({}) '.format(x[4].strip()) if x[4].strip() else ''
        filename = "-".join([temp.strip().lower() for temp in name.split(" ")])
        
        if supervisorNum % 3 == 0: print >> writeFile, "\t\t<div class=\"row\">"
        
      #   print >> writeFile, '\t\t\t<div class="col-md-4">\n\
      #   <ul class="list-group">\n\
      #       <li class="list-group-item auto-cursor">\n\
      #           <div class="profile-main text-center">\n\
      #               <img src="img/supervisors/{}.jpg" alt="{}">\n\
      #               <div class="description-bottom">\n\
      #               <div class="profile-name">{} {}\'{}</div>\n\
      #               <div class="profile-title">{}</div>\n\
      #               <div class="profile-title">{}</div>\n\
      #               </div>\n\
      #           </div>\n\
      #       </li>\n\
      #   </ul>\n\
      # </div>'.format(filename, name, name, school, year, event, team)
        writeFile.write('\t\t\t<div class="col-md-4">\n\
        <ul class="list-group">\n\
            <li class="list-group-item auto-cursor">\n\
                <div class="profile-main text-center">\n\
                    <img src="img/supervisors/{}.jpg" alt="{}">\n\
                    <div class="description-bottom">\n\
                    <div class="profile-name">{} {}\'{}</div>\n\
                    <div class="profile-title">{}</div>\n\
                    <div class="profile-title">{}</div>\n\
                    </div>\n\
                </div>\n\
            </li>\n\
        </ul>\n\
      </div>'.format(filename, name, name, school, year, event, team))

        # if supervisorNum % 3 == 2: print >> writeFile, "\t\t</div>"
        if supervisorNum % 3 == 2: writeFile.write("\t\t</div>")

    # if supervisorNum % 3 != 2: print >> writeFile, "\t\t</div>"
    if supervisorNum % 3 != 2: writeFile.write("\t\t</div>")

# print >> writeFile, "\t</div>"
writeFile.write("\t</div>")

readFile.close()
writeFile.close()
