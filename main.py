from fetcher.jobnet_connector import search_ads

if __name__ == "__main__":
    r = search_ads(10, 1, "Java", 10, 1650)
    print(r)
