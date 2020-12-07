lines = []
lines_without_duplicates = []

with open ("README.md", "r") as rm:
    for line in rm:
        lines.append(line)


dups = set()
for l_1 in lines:
    if "- [" not in l_1:
        lines_without_duplicates.append(l_1)
        continue
    occurrences = 0
    for l_2 in lines:
        if l_1.lower()[0:25] == l_2.lower()[0:25]:
            occurrences += 1

    if occurrences > 1:
        print("Double line detected %d times: %s"%(occurrences, l_1.replace("\n", "")))

        # Only add if it is not in the dict
        set_entry = l_1[0:25].lower()
        if set_entry not in dups:
            dups.add(set_entry)
            lines_without_duplicates.append(l_1)
    else:
        lines_without_duplicates.append(l_1)


newfile = "".join(lines_without_duplicates)
with open("README2.md", "w+") as rm2:
    rm2.write(newfile)
