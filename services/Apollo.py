import requests
import json

''' Colors '''
GRAY = PLOAD = '\001\033[38;5;246m\002'
RED = '\001\033[1;31m\002'
ORANGE = '\033[0;38;5;214m\002'
END = '\001\033[0m\002'
MainColor = f'{ORANGE}'
SColor = f'{GRAY}'

LINE = f'{RED}-----------------------------------------:{END}'


class Apollo:
    def __init__(self, config, args):
        self.config = config
        self.domain = args.domain
        self.args = args

    def get_job_postings(self, ORGANIZATION_ID):
        url = "https://api.apollo.io/v1/organizations/{}/job_postings".format(ORGANIZATION_ID)

        querystring = {
            "api_key": self.config['Apollo']['api_key']
        }

        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()["organization_job_postings"]

    def getOrganizations(self):
        url = "https://api.apollo.io/v1/organizations/enrich?api_key={0}&domain={1}".format(
            self.config['Apollo']['api_key'], self.domain)
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()["organization"]

    def getEmployee(self):
        url = "https://api.apollo.io/v1/mixed_people/search"
        payload = json.dumps({
            "api_key": self.config['Apollo']['api_key'],
            "q_organization_domains": self.domain,
            "page": 1,
            "per_page": 200
        })
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()["people"]

    def run(self):
        organizations = self.getOrganizations()
        people = self.getEmployee()
        job_organizations = self.get_job_postings(organizations["id"])
        print(f'{SColor:}--------------Company Information---------------------')
        print(f'{MainColor:}Name: {organizations["name"]}')
        print(f'{MainColor:}website_url: {organizations["website_url"]}')
        print(f'{MainColor:}linkedin_url: {organizations["linkedin_url"]}')
        print(f'{MainColor:}facebook_url: {organizations["facebook_url"]}')
        print(f'{MainColor:}industry: {organizations["industry"]}')
        print(f'{MainColor:}address: {organizations["raw_address"]}')
        print(f'{MainColor:}short_description: {organizations["short_description"]}')
        #        print(f'{MainColor:}total_funding: {organizations["total_funding"]}')
        if self.args.list != "o":
            if self.args.list == "p" or self.args.list == "a":
                print(f'{LINE:}')
                print(f'{SColor:}--------------Employees---------------------')
                if len(people) == 0:
                    print("list empty")
                else:
                    for k in people:
                        print(f'{MainColor:}name: {k["name"]}')
                        print(f'{MainColor:}title: {k["title"]}')
                        print(f'{MainColor:}linkedin_url: {k["linkedin_url"]}')
                        print(f'{MainColor:}email: {k["email"]}')
                        print(f'{MainColor:}photo_url: {k["photo_url"]}')
                        print(f'{LINE:}')

            if self.args.list == "j" or self.args.list == "a":
                print(f'{LINE:}')
                print(f'{SColor:}--------------Company Jobs---------------------')
                if len(job_organizations) == 0:
                    print("list empty")
                else:
                    for k in job_organizations:
                        print(f'{MainColor:}title: {k["title"]}')
                        print(f'{MainColor:}url_job: {k["url"]}')
                        print(f'{MainColor:}state: {k["state"]}')
                        print(f'{MainColor:}city: {k["city"]}')
                        print(f'{MainColor:}last_seen_at: {k["last_seen_at"]}')
                        print(f'{LINE:}')
