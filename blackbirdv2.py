import aiohttp
import asyncio
import requests
from dotenv import load_dotenv
import hashlib
import os
import json

load_dotenv()
listURL = os.getenv("LIST_URL")
listFileName = os.getenv("LIST_FILENAME")
proxy = os.getenv("PROXY") if os.getenv("USE_PROXY") == "TRUE" else None


def doSyncRequest(method, url):
    response = requests.request(method=method, url=url, proxies=proxy, verify=False)
    parsedData = None

    try:
        parsedData = response.json()
    except:
        pass
    return response, parsedData


async def doAsyncRequest(method, url, session):
    print("Sending request...")
    response = await session.request(method, url, proxy=proxy, verify_ssl=False)
    parsedData = None

    try:
        parsedData = await response.json()
    except:
        pass
    return response, parsedData


def readList():
    with open(listFileName, "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


def downloadList():
    response, parsedData = doSyncRequest("GET", listURL)
    with open(listFileName, "w", encoding="UTF-8") as f:
        json.dump(parsedData, f, indent=4, ensure_ascii=False)


def hashJSON(jsonData):
    dumpJson = json.dumps(jsonData, sort_keys=True)
    jsonHash = hashlib.md5(dumpJson.encode("utf-8")).hexdigest()
    return jsonHash


async def fetchResults(username):
    data = readList()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for site in data["sites"]:
            tasks.append(
                doAsyncRequest(
                    method="GET",
                    url=site["uri_check"].replace("{account}", username),
                    session=session,
                )
            )
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


def verifyUsername(username):
    data = asyncio.run(fetchResults(username))
    for item in data:
        print(item)


def checkUpdates():
    if os.path.isfile(listFileName):
        print("[-] Checking for updates...")
        data = readList()
        currentListHash = hashJSON(data)
        response, data = doSyncRequest("GET", listURL)
        remoteListHash = hashJSON(data)
        if currentListHash != remoteListHash:
            print("[!] Updating...")
            downloadList()
        else:
            print("[+] List is up to date")
    else:
        print("[!] Downloading WhatsMyName list")
        downloadList()


if __name__ == "__main__":
    checkUpdates()
    # verifyUsername("p1ngul1n0")
