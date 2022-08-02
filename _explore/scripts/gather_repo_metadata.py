from scraper.github import queryManager as qm

ghDataDir = "../../explore/github-data"
genDatafile = f"{ghDataDir}/intReposInfo.json"
topicsDatafile = f"{ghDataDir}/intRepos_Topics.json"
writeFile = f"{ghDataDir}/intRepo_Metadata.json"

# initialize data manager and load repo info
genDataCollector = qm.DataManager(genDatafile, True)

# initialize data manager and load repo topics
topicsCollector = qm.DataManager(topicsDatafile, True)

# initialize data manager to write collected info
infoWriter = qm.DataManager(writeFile, False)

print("\nGathering repo metadata...\n")

# iterate through repos
for repo in genDataCollector.data["data"]:

    repoObj = genDataCollector.data["data"][repo]

    repoData = {
        "name": repo,
        "description": repoObj["description"],
        "website": repoObj["homepageUrl"],
    }

    # gather any repo topics
    if repoObj["repositoryTopics"]["totalCount"] > 0:
        topicRepo = topicsCollector.data["data"][repo]
        topics = [
            topicObj["topic"]["name"]
            for topicObj in topicRepo["repositoryTopics"]["nodes"]
        ]

        repoData["topics"] = topics
    else:
        repoData["topics"] = None

    # record info for this repo
    infoWriter.data[repo] = repoData

# write data to file
infoWriter.fileSave(newline="\n")

print("\nDone!\n")
