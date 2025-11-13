from datetime import datetime



def test_create_dict():
    print(__file__)
    from ad_model.job_ad import JobAd
    job_ad_1 = JobAd("Sweden",
                      19000,
                      "Göteborg",
                      "Izzted",
                      "Coder",
                      "123",
                      "http:localhost",
                      "NoWhere",
                      800000,
                      "Hacker",
                      "Lorem Ipsum",
                      datetime.now(),
                      "some status",
                      datetime.now())
    print(job_ad_1)
    print(job_ad_1.__dict__)
    json_str = job_ad_1.to_json()
    print(json_str)
    job_ad_1_dict = JobAd.from_json(json_str)
    print(job_ad_1_dict)


if __name__ == "__main__":
    test_create_dict()