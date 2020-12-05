import sys
import os
import requests
from pathlib import Path

def download_list(listname):

    out_dir = os.path.join("out", listname)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    print("Downloading papers from list %s"%(listname))

    # Get the markdown
    list_readme = "README.md"

    if listname == "All":
        grab_all = True
        should_grab = True
    else:
        should_grab = False

    # Open the list and go through each bullet
    with open(list_readme, "r") as lrf:

        for line in lrf:
            # If we have defined a listname then we should only get the papers from this list.
            if grab_all == False and listname != None:
                if should_grab == False:
                    if "##" in line and listname in line:
                        should_grab = True
                        continue
                if should_grab and "##" in line:
                    should_grab = False

            if should_grab:
                print("Trying %s"%(line))
                if (    "-" in line and 
                        "[" in line and 
                        "]" in line and 
                        "(" in line and 
                        ")" in line and 
                        ".pdf" in line):
                    # we assume this is a line with a link to a paper, so we proceed to download it
                    #print("Will try to extract paper %s"%(line))

                    try:
                        start = line.find("[")
                        end = line.find("]")
                        name = line[start+1:end].replace(" ","_").replace(",", "_")
                        print("Name: %s"%(name))

                        # Now get the URL
                        start = line.find("(")
                        end = line.find(")")
                        URL = line[start+1:end]
                        print("URL: %s"%(URL))

                        response=requests.get(URL)
                        filetowrite=Path(os.path.join(out_dir, "%s.pdf"%(name)))
                        filetowrite.write_bytes(response.content)
                    except:
                        continue
            else:
                print("Skipping %s"%(line))

download_list("All")
