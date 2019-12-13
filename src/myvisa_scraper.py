import requests
from bs4 import BeautifulSoup
import json

visa_years = [i for i in range(2016, 2020)]
visa_pages = [i for i in range(1, 101)]
visa_years_test = [2019]
visa_pages_test = [i for i in range(1, 101)]


def scrap_by_year_page(year, page):
    print(year, page)
    url = 'https://www.myvisajobs.com/Reports/' + str(year) +'-H1B-Visa-Sponsor.aspx?P=' + str(page)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tbl = soup.find('table', {'class': 'tbl'})

    records = []
    lines = tbl.find_all('tr')
    for i in range(1, len(lines)):
        record = {}
        tds = lines[i].find_all('td')
        if len(tds) < 4:
            # ads line, jump
            continue
        record['rank'] = tds[0].text
        record['sponsor'] = tds[1].text
        record['num_of_LCA'] = tds[2].text
        record['ave_salary'] = tds[3].text
        record['year'] = year
        records.append(record)

    return records


def get_data_from_myvisa(if_test):
    print('scraping data from myvisajobs...')
    if if_test:
        yrs = visa_years_test
        pgs = visa_pages_test
    else:
        yrs = visa_years
        pgs = visa_pages

    visa_records = []
    for year in yrs:
        for p in pgs:
            data = scrap_by_year_page(year, p)
            visa_records.append(data)

    return visa_records

def save_to_json(data, name):
    jsObj = json.dumps(data)

    f = open('data_' + name + '.json', 'w')
    f.write(jsObj)
    f.close()


if __name__ == '__main__':
    # records = get_data_by_year_page(2019, 1)

    for year in visa_years:
        records = []
        for p in visa_pages:
            data = get_data_from_myvisa(year, p)
            records.append(data)
        save_to_json(records, str(year))