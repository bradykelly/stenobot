import argparse

progName = "ListBot"

argsString = "   --lbadd some   text"
commands = ["--lbadd", "--lblist", "--lbclear"]

argParts = [s for s in argsString.split(" ") if s.strip() != '']

entryText = None
if argParts[0] == "--lbadd":
    entryText = " ".join(argParts[1:])    


print (entryText)
