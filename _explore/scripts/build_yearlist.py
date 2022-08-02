from scraper.github import queryManager as qm
from os import environ as env
import os.path

ghDataDir = env.get("GITHUB_DATA", "../github-data")
yearDict = {}

# Gather all file name data
print("Checking GitHub data file names with year stamps...")
if not os.path.exists(ghDataDir):
    raise FileNotFoundError("Directory path '%s' does not exist." % (ghDataDir))
for file in os.listdir(ghDataDir):
    if file.endswith(".json"):
        nameSplit = file.split(".")
        # Must have format "somePrefix.0000.json"
        if nameSplit[0] != "YEARS" and nameSplit[1].isdigit():
            prefix = nameSplit[0]
            yearX = int(nameSplit[1])
            if prefix not in yearDict:
                yearDict[prefix] = []
            yearDict[prefix].append(yearX)

print("Sorting year data...")
# Remove duplicate years (though shouldn't be possible) and sort list
for prefix, yearList in yearDict.items():
    yearList = sorted(set(yearList))
    yearDict[prefix] = yearList

yearData = qm.DataManager(f"{ghDataDir}/YEARS.json", False)
yearData.fileSave(newline="\n")

print("Done!\n")
