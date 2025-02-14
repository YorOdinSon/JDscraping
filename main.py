from datetime import date
import requests
import json
import parseAndSend
import time

today = date.today()
day = today.strftime("%B %d, %Y") #not used in this section of the tool, but I like using dates on Python :D

requestURL = "https://crowdstrike.wd5.myworkdayjobs.com/wday/cxs/crowdstrike/crowdstrikecareers/jobs" #I found this in the jobs API within the network tab of the dev tools - the below is what your browser passes to Workday to retrieve the JSON

#fetched the jobs file from Google DevTool, and right clicked on it to "copy as cURL" and used http://curlconverter.com/ to get the headers, cookies, and json_data
cookies = {
    'wd-browser-id': 'b76446ae-4ea6-41c2-90f9-362128c353b3',
    'CALYPSO_CSRF_TOKEN': '5dcf9514-3e5c-4f38-bef3-99da1bf51181',
    'timezoneOffset': '0',
    'enablePrivacyTracking': 'true',
    '_ga': 'GA1.4.1939870210.1735821833',
    'wday_vps_cookie': '2297207818.53810.0000',
    'PLAY_SESSION': '11a903edc434a881c27b5066d1aac7d7a07fccc6-crowdstrike_pSessionId=nivmbka4u70ikpr8c025or273j&instance=vps-prod-y8jw76oq.prod-vps.pr502.cust.pdx.wd',
    '__cf_bm': 'xLKAFfK5YwvM_lXG6349eWZDVqiJQ0lJikPlSkM.yUo-1739281386-1.0.1.1-SPoGHBjdd7Typ0FNc0Zi_FqMnU1HPsaQoFwQ7YSy9yExWGHy610YcnZrnbRPwM.PiEoCxBxOCZ1AcEscWqu8kg',
    '__cflb': '02DiuHJZe28xXz6hQKLf1exjNbMDM5uxfVxS6FeBdRTg8',
    '_cfuvid': '7VhWLziAwnpTACh0y23NJagxu4tBuZBS75Xg9VExMnA-1739281386676-0.0.1.1-604800000',
    '_ga_RQ2CL61L6Z': 'GS1.4.1739281388.5.0.1739281420.0.0.0',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US',
    'content-type': 'application/json',
    # 'cookie': 'wd-browser-id=b76446ae-4ea6-41c2-90f9-362128c353b3; CALYPSO_CSRF_TOKEN=5dcf9514-3e5c-4f38-bef3-99da1bf51181; timezoneOffset=0; enablePrivacyTracking=true; _ga=GA1.4.1939870210.1735821833; wday_vps_cookie=2297207818.53810.0000; PLAY_SESSION=11a903edc434a881c27b5066d1aac7d7a07fccc6-crowdstrike_pSessionId=nivmbka4u70ikpr8c025or273j&instance=vps-prod-y8jw76oq.prod-vps.pr502.cust.pdx.wd; __cf_bm=xLKAFfK5YwvM_lXG6349eWZDVqiJQ0lJikPlSkM.yUo-1739281386-1.0.1.1-SPoGHBjdd7Typ0FNc0Zi_FqMnU1HPsaQoFwQ7YSy9yExWGHy610YcnZrnbRPwM.PiEoCxBxOCZ1AcEscWqu8kg; __cflb=02DiuHJZe28xXz6hQKLf1exjNbMDM5uxfVxS6FeBdRTg8; _cfuvid=7VhWLziAwnpTACh0y23NJagxu4tBuZBS75Xg9VExMnA-1739281386676-0.0.1.1-604800000; _ga_RQ2CL61L6Z=GS1.4.1739281388.5.0.1739281420.0.0.0',
    'origin': 'https://crowdstrike.wd5.myworkdayjobs.com',
    'priority': 'u=1, i',
    'referer': 'https://crowdstrike.wd5.myworkdayjobs.com/crowdstrikecareers',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'x-calypso-csrf-token': '5dcf9514-3e5c-4f38-bef3-99da1bf51181',
}

all_jobs = []
limit = 20
offset = 0
jobIdsCount = set() #tracking the jobIDS in the JSON
apiCallsCount = 0

while True: #looping everything, as in this specific case, Workday allowed me to fetch 20 results for each call.
    json_data = {
        'appliedFacets': {},
        'limit': limit,
        'offset': offset,
        'searchText': '',
    }

    response = requests.post(
        requestURL,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    if response.status_code != 200:
        print(f"❌ Failed to fetch jobs. Status Code: {response.status_code}") #simple error handling to see why it fails
        #print("Response Headers:", response.headers)
        break #breaking the cycle at the very first error I get.
    
    jobs = response.json()
    job_list = jobs.get("jobPostings", [])

    if not job_list:
        print("✅ All jobs retrieved! 😎")
        break

     # Assuming that the last page could have less than 20 results. 

    if len(job_list) < limit:
        print("✅ Reached the last page!")
        break  

    new_jobs = 0

    for job in job_list:
        job_id = job.get("externalPath")  # Use job ID or unique field
        if job_id not in jobIdsCount:
            jobIdsCount.add(job_id)
            all_jobs.append(job)
            new_jobs += 1
    apiCallsCount += 1
    print(f"{apiCallsCount} - 📥 Offset: {offset} | Retrieved {new_jobs} new jobs | Total: {len(all_jobs)}")

    # ✅ If no new jobs were added, stop (API is repeating results)
    if new_jobs == 0:
        print("🚨 STOP! The API might be repeating results or it just reached EOF!.")
        break  

    offset += limit
    time.sleep(1)

    #all_jobs.extend(job_list)
    #print(f"📥 Retrieved {len(all_jobs)} jobs so far...")
    

print(f"✅ Successfully fetched {len(all_jobs)} jobs!") #if this prints, then I'm sure the file is saved!

filename = "fetchedData.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=4)  # Converting Python dict to formatted JSON and in human comprehesible language (indent=4)
print("✅ - Job Done! File created: ", filename)
parseAndSend.parse_and_send(filename)


