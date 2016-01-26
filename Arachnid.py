import operator, os, time, tkMessageBox
from Tkinter import *

def main(): # RUNS MAIN METHOD
    output["text"] = "" # CLEAR output
    if len(keyNpt.get()) > 0:
        results = processResults(searchTree(str(dirNpt.get()), parseStrList(str(keyNpt.get()))))
        if len(results) > 0:
            output["text"] = "[ Search complete. ]"
            tkMessageBox.showinfo("Results", results) # UPDATE OUTPUT WITH SEARCH RESULTS
        else: output["text"] = "[ No matches found. ]" # IF AN ERROR OCCURRED
    else: output["text"] = "Please fill out all fields."
    return

def parseStrList(string): # PARSE string INPUT TO keys
    items = []
    while string.find(",") > -1:
        c = string.find(",")
        items.append(string[:c].strip()) # ADD PARSED KEY
        string = string[c + 1:].strip()
    items.append(string)
    return items

def processResults(queries): # SORT AND TABULATE queries
    data, queries, results = "", sorted(queries.items(), key=operator.itemgetter(1)), ""
    for n in range(1, len(queries) + 1): results += "\n[ %s : %s ]" % (queries[-n][1], queries[-n][0]) # SHOW MATCHES FIRST
    return results

def searchFile(path, keys): # return matches FOUND IN FILE AT path
    data, matches = "", 0
    if not (lambda path: os.access(path, os.R_OK))(path): return matches # QUIT IF FILE AT path IS UNREADABLE
    with open(path, "r") as f:
        for l in f.readlines(): data += l # GET ALL LINES IN f
    for k in keys:
        while data.find(k) > -1: data, matches = data[data.find(k) + 1:], matches + 1 # UPDATE VALUES
    return matches

def searchTree(dirPath, keys): # return queries
    queries = {}
    if len(dirPath) == 0: dirPath = "./" # SETS DEFAULT dirPath VALUE
    for root, directories, filenames in os.walk(dirPath):
        for f in filenames:
            if f == "Arachnid.py": continue
            path = os.path.join(root,f)
            matches = searchFile(path, keys)
            if matches > 0: queries[str(path)] = matches # ONLY SHOW PATHS WITH HITS
    return queries

#WINDOW
window = Tk()
window.wm_title("Arachnid")

#FRAMES
top, space1, mid,space2, bottom = Frame(window), Frame(window, height=4), Frame(window), Frame(window, height=4), Frame(window)

#WIDGETS
keyLbl, keyNpt = Label(top, text="Keywords (separate w/ commas): "), Entry(top, bg="white", width=20)
dirLbl, dirNpt, go = Label(mid, text="Directory: "), Entry(mid, bg="white", width=20), Button(mid, command=main, text="Go")
outputLbl, output = Label(bottom, text="Output: "), Label(bottom, text="[ Waiting for initial launch.... ]")

#WIDGET PACKING
keyLbl.pack(side = LEFT)
keyNpt.pack(side = RIGHT)

dirLbl.pack(side = LEFT)
go.pack(side = RIGHT)
dirNpt.pack()

outputLbl.pack(side = LEFT)
output.pack(side = RIGHT)

#FRAME PACKING
top.pack()
space1.pack()
mid.pack()
space2.pack()
bottom.pack()

#REST
window.mainloop()
