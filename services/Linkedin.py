import re
import time
import urllib

import requests
from playwright.sync_api import sync_playwright


class Linkedin:
    def __init__(self, config, name):
        self.config = config
        self.name = name

        def log_request(intercepted_request):
            print("a request was made:", intercepted_request)

        def cookies(context):
            data = {}

            cookies = context.cookies()
            for f in cookies:
                if "JSESSIONID" in f["name"]:
                    JSESSIONID = f["value"]
                    data["JSESSIONID"] = \
                        re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", JSESSIONID)[
                            0]
            cookies = ';'.join([f'{eh["name"]}={eh["value"]}' for eh in cookies])

            data["cookies"] = cookies
            return data

        def getcookie(self):
            data = {}
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(channel="chrome", headless=False, )
                context = browser.new_context()
                page = context.new_page()
                page.once("load", log_request)
                page.goto("https://www.linkedin.com/")
                page.click("[placeholder=\" \"]")
                page.fill("[placeholder=\" \"]", self.config['data']['email'])
                page.click("text=Password Show >> [placeholder=\" \"]")
                page.fill("text=Password Show >> [placeholder=\" \"]", config['data']['password'])
                time.sleep(5)
                page.click("button:has-text(\"Sign in\")")
                print("")
                if page.url.startswith("https://www.linkedin.com/checkpoint/challenge"):
                    page.wait_for_timeout(70000)
                    return cookies(context)
                else:
                    return cookies(context)

            def getCompanyID(name, cookies):
                query = urllib.parse.quote(name.encode('utf8'))
                print(query)
                url = "https://www.linkedin.com/voyager/api/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-174&origin=GLOBAL_SEARCH_HEADER&q=all&query=(keywords:{},flagshipSearchIntent:SEARCH_SRP,queryParameters:(resultType:List(COMPANIES)),includeFiltersInResponse:false)&start=0".format(
                    query)
                print(url)
                payload = {}
                headers = {
                    'authority': 'www.linkedin.com',
                    'accept': 'application/vnd.linkedin.normalized+json+2.1',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'cookie': '{}'.format(cookies["cookies"]),
                    'csrf-token': 'ajax:{}'.format(cookies["JSESSIONID"]),
                    'pragma': 'no-cache',
                    'referer': 'https://www.linkedin.com/search/results/companies/?keywords=sympl&origin=GLOBAL_SEARCH_HEADER&sid=i~U',
                    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
                    'x-li-lang': 'en_US',
                    'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_companies;yQgLL+oZQ/WMABZFwpvKQA==',
                    'x-li-track': '{"clientVersion":"1.11.5856","mpVersion":"1.11.5856","osName":"web","timezoneOffset":2,"timezone":"Africa/Cairo","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1.25,"displayWidth":1920,"displayHeight":1080}',
                    'x-restli-protocol-version': '2.0.0'
                }
                print(headers)

                response = requests.request("GET", url, headers=headers, data=payload)
                json_data = response.json()
                CompanyID = json_data["data"]["elements"][1]
                return CompanyID

            def profileContactInfo(publicIdentifier, cookies):
                url = "https://www.linkedin.com/voyager/api/identity/profiles/{}/profileContactInfo".format(
                    publicIdentifier)
                payload = {}
                headers = {
                    'authority': 'www.linkedin.com',
                    'accept': 'application/vnd.linkedin.normalized+json+2.1',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'cookie': '{}'.format(cookies["cookies"]),
                    'csrf-token': 'ajax:{}'.format(cookies["JSESSIONID"]),
                    'pragma': 'no-cache',
                    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
                    'x-li-lang': 'en_US',
                    'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_companies;yQgLL+oZQ/WMABZFwpvKQA==',
                    'x-restli-protocol-version': '2.0.0'
                }

                response = requests.request("GET", url, headers=headers, data=payload)
                return response.json()

            def profileInfo(publicIdentifier, cookies):
                url = "https://www.linkedin.com/voyager/api/identity/profiles/{}".format(publicIdentifier)
                payload = ""
                headers = {
                    'authority': 'www.linkedin.com',
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'content-type': 'text/plain;charset=UTF-8',
                    'cookie': '{}'.format(cookies["cookies"]),
                    'csrf-token': 'ajax:{}'.format(cookies["JSESSIONID"]),
                    'origin': 'https://www.linkedin.com',
                    'pragma': 'no-cache',
                    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
                    'x-li-query-accept': 'application/graphql',
                    'x-restli-protocol-version': '2.0.0'
                }

                response = requests.request("GET", url, headers=headers, data=payload)

                print(response.text)

                return response.json()

            # locationName

            def get_employees(name, cookies):
                global JobTitleText, emailAddress, phoneNumbers
                data = {}
                rr = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",
                                getCompanyID(name, cookies)["items"][0]["itemUnion"]["*entityResult"])
                url = "https://www.linkedin.com/voyager/api/search/hits?count=50&facetCurrentCompany=List({})&keywords=List()&origin=organization&q=people&start=0".format(
                    rr[0])
                payload = {}
                headers = {
                    'authority': 'www.linkedin.com',
                    'accept': 'application/vnd.linkedin.normalized+json+2.1',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'cookie': '{}'.format(cookies["cookies"]),
                    'csrf-token': 'ajax:{}'.format(cookies["JSESSIONID"]),
                    'pragma': 'no-cache',
                    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
                    'x-li-lang': 'en_US',
                    'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_companies;yQgLL+oZQ/WMABZFwpvKQA==',
                    'x-li-track': '{"clientVersion":"1.11.5856","mpVersion":"1.11.5856","osName":"web","timezoneOffset":2,"timezone":"Africa/Cairo","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1.25,"displayWidth":1920,"displayHeight":1080}',
                    'x-restli-protocol-version': '2.0.0'
                }

                response = requests.request("GET", url, headers=headers, data=payload)
                json_data = response.json()
                elements = json_data["data"]["elements"]
                included = json_data["included"]
                for k in elements:
                    hitInfo = k["hitInfo"]
                    for i in included:
                        if "lastName" in i:
                            entityUrn = i["entityUrn"].split(":")[3]
                            if "id" in hitInfo:
                                if entityUrn == hitInfo["id"]:
                                    full_Name = i["firstName"] + " " + i["lastName"]
                                    data["full_Name"] = full_Name
                                    publicIdentifier = i["publicIdentifier"]
                                    profiles = profileContactInfo(publicIdentifier, cookies)
                                    miniProfile = profileInfo(publicIdentifier, cookies)["miniProfile"]
                                    print(miniProfile)
                                    if "emailAddress" in profiles:
                                        emailAddress = profiles["emailAddress"]
                                    else:
                                        emailAddress = "Empty"
                                    if "phoneNumbers" in profiles:
                                        phoneNumbers = profiles["phoneNumbers"]
                                    else:
                                        phoneNumbers = "Empty"
                                    if "address" in profiles:
                                        address = profiles["address"]
                                    else:
                                        address = "Empty"
                                    if "snippets" in hitInfo:
                                        Job_Title = hitInfo["snippets"][0]
                                        if "heading" in Job_Title:
                                            JobTitleText = hitInfo["snippets"][0]["heading"]["text"]
                                        else:
                                            JobTitleText = "Empty"
                                    else:
                                        JobTitleText = "Empty"
