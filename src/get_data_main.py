import argparse
import pandas as pd

from myvisa_scraper import get_data_from_myvisa, visa_pages, visa_years
from api_crawler import pull_adzuna_jobs, pull_github_jobs
from glassdoor_scraper import start
from mysql_db import create_tables, conn, cur, refresh_jobs

IF_TEST = False

def grab_data_by_scraping_and_api_requests(if_test):
    company_data = []
    visa_records = []

    visa_records = get_data_from_myvisa(if_test)
    github_jobs = pull_github_jobs(if_test)
    adzuna_jobs = pull_adzuna_jobs(if_test)

    # # Manual options for the company, num pages to scrape, and URL
    pages = 1
    companyName = "microsoft"
    companyURL = "https://www.glassdoor.com/Interview/Microsoft-Software-Development-Engineer-Interview-Questions-EI_IE1651.0,9_KO10,39.htm"
    company_data = start(companyName, companyURL, pages)

    return visa_records, {'github_jobs': github_jobs, 'adzuna_jobs': adzuna_jobs}, company_data


def grab_data_from_local_files():
    companies = pd.read_csv('../data/us_companies.csv')
    print(companies.head())

    cmp = pd.read_csv('../data/companies/microsoft.csv')
    print(cmp.head())

    cur.execute("select * from positions limit 10")
    result = cur.fetchall()
    print(result)

    cur.execute("select * from visa_records limit 10")
    result = cur.fetchall()
    print(result)


def clean_save_job(data):
    github_jobs = data['github_jobs']
    adzuna_jobs = data['adzuna_jobs']
    jobs = [] # company, title, location, description, created, url
    for item in github_jobs:
        jobs.append({
            'company': item['company'],
            'title': item['title'],
            'location': item['location'],
            'description': item['description'],
            'created': item['created_at'],
            'url': item['company_url']
        })

    for item in adzuna_jobs:
        jobs.append({
            'company': item['company']['display_name'],
            'title': item['title'],
            'location': item['location']['display_name'],
            'description': item['description'],
            'created': item['created'],
            'url': item['redirect_url']
        })


    for item in jobs:
        item['company'] = item['company'].replace("'", "\\'")
        item['description'] = item['description'].replace("'", "\\'")
        sql = 'INSERT INTO positions (company, title, location, created, url, description) VALUES \
                ("{}", "{}", "{}", "{}", "{}", "{}")'.format(item['company'], item['title'],
                                                  item['location'],
                                                  item['created'], item['url'], item['description'])
        # sql = 'INSERT INTO positions (company, title, location, created, url) VALUES \
        #         ("{}\", '{}', '{}', '{}', '{}')""".format(item['company'], item['title'],
        #                                           item['location'],
        #                                           item['created'], item['url'])
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            print(sql)
            continue

    conn.commit()

def clean_save_visa(data):
    for i in range(len(data)):
        line = data[i]
        for item in line:
            sql = "INSERT INTO visa_records (rank, sponsor, num_of_LCA, ave_salary, ryear) VALUES "

            sql += "({}, '{}', {}, '{}', '{}')".format(item['rank'], item['sponsor'],
                                                    int(item['num_of_LCA'].replace(',', '')),
                                                    item['ave_salary'], item['year'])
            try:
                cur.execute(sql)
            except Exception as e:
                # print(e)
                # print(sql)
                continue

    cur.execute(sql)
    conn.commit()


def clean_save_company(data):
    print(data)
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-source", choices=["local", "remote", "test"], nargs=1, help="where data should be gotten from")
    args = parser.parse_args()

    location = args.source[0]

    if location == "local":
        grab_data_from_local_files()

    elif location == "remote":
        IF_TEST = False
        visa_data, job_data, company_data = grab_data_by_scraping_and_api_requests(IF_TEST)
        print(visa_data)
        print(job_data)

        # create_tables()
        clean_save_job(job_data)
        clean_save_visa(visa_data)
        clean_save_company(company_data)

    elif location == "test":
        IF_TEST = True
        create_tables()
        visa_data, job_data, company_data = grab_data_by_scraping_and_api_requests(IF_TEST)

        clean_save_job(job_data)
        clean_save_visa(visa_data)
        clean_save_company(company_data)

    else:
        print('invalid param!')
        exit(0)


if __name__ == "__main__":
    IF_TEST = False
    # create_tables()

    # visa single
    # visa_records = get_data_from_myvisa(IF_TEST)
    # clean_save_visa(visa_records)

    #positions
    refresh_jobs()
    github_jobs = pull_github_jobs(IF_TEST)
    adzuna_jobs = pull_adzuna_jobs(IF_TEST)
    data = {'github_jobs': github_jobs, 'adzuna_jobs': adzuna_jobs}
    clean_save_job(data)


