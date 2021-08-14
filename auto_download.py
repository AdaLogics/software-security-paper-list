import os
import sys
import requests
from pathlib import Path

def download_list(listname):


    namecount = 0
    failcount = 0
    out_dir = os.path.join("out", listname)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    print("Downloading papers from list %s"%(listname))

    # Get the markdown
    list_readme = "README.md"

    failname = []
    namelist = []

    if listname == "All":
        grab_all = True
        should_grab = True
    else:
        grab_all = False
        should_grab = False

    # Open the list and go through each bullet
    with open(list_readme, "r", encoding='UTF-8') as lrf:

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
                        name = line[start+1:end].replace(" ","_").replace(",", "_").replace(':', '_')
                        print("Name: %s"%(name))
                        namelist.append(name)
                        namecount +=1

                        # Now get the URL
                        start = line.find("(")
                        end = line.find(")")
                        URL = line[start+1:end]
                        print("URL: %s"%(URL))

                        response=requests.get(URL)
                        filetowrite=Path(os.path.join(out_dir, "%s.pdf"%(name)))
                        filetowrite.write_bytes(response.content)
                    except:
                        failname.append(name)
                        failcount +=1
                        continue
            else:
                #print("Skipping %s"%(line))
                pass
        
        

        p = Path(out_dir)
        fail_flag = False
        sucess_pdfs = sorted(p.glob('*.pdf'))
        sucess_name = [pdf.stem for pdf in sucess_pdfs ]
        for child in p.iterdir():
            if child in sucess_pdfs:
                continue
            else:
                fail_flag = True
                failcount +=1
                child.unlink()

        if fail_flag:
            print('\n\nThe following files failed to download, please download manually\n')
            for name in namelist:
                if name in sucess_name:
                    continue
                else:
                    print(name)

        print("Total papers count :", namecount)
        print("Failure count :", failcount)
        print('Sucess count :', namecount - failcount)
        print('\n\n')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ./auto_download.py TOPIC_NAME")
    download_list(sys.argv[1])
