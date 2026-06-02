import requests

def fetch_usajobs(keyword, location="", results_per_page=15):
        headers = {
            "Host": "data.usajobs.gov",
            "User-Agent": "div.jose90@gmail.com",
            "Authorization-Key": "pC3TWVlOb/72+E3B04gkVu05y/zIsp5zZiS9vu8PKSw=",
        }

        params = {
            "Keyword": keyword,
            "LocationName": location,
            "ResultsPerPage": results_per_page,
        }

        url = "https://data.usajobs.gov/api/search"
        queryParam = f"?Keyword={keyword}&LocationName={location}"

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            result = response.json()["SearchResult"]
            print(f"SearchResultCount: {result['SearchResultCount']}")
            return result["SearchResultItems"]
        else:
            print(f"Request failed: {response.status_code}")
            return []

if __name__ == "__main__":
    jobs = fetch_usajobs("software")
    for job in jobs:
        title = job['MatchedObjectDescriptor']['PositionTitle']
        agency = job['MatchedObjectDescriptor']['OrganizationName']
        print(f"{title} at {agency}")