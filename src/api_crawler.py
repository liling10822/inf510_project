import requests
import json

def get_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.text)
    else:
        data = []

    return data

def post_url(url, params):
    r = requests.post(url, data=json.dumps(params))
    if r.status_code == 200:
        data = json.loads(r.text)
    else:
        data = []

    return data

def pull_github_jobs(if_test):
    print('pulling data from github jobs...')

    if if_test:
        max_page = 2
    else:
        max_page = 10

    data = []
    for page in range(max_page):
        url = "https://jobs.github.com/positions.json?page=" + str(page)
        p_data = get_url(url)
        data.extend(p_data)
        if len(p_data) == 0:
            break
    print('get github jobs: ', len(data))

    return data

def pull_adzuna_jobs(if_test):
    print('pulling data from adzuna...')

    if if_test:
        max_page = 11
    else:
        max_page = 101

    param = {
        'app_id': '45b909db',
        'app_key': '7c9cdae6fe05c8644755936ec94100a7',
        'category': 'it-jobs'
    }
    data = []
    print('getting data from adzuna...')
    for page in range(1, max_page):
        print('page ', page)
        url = 'https://api.adzuna.com/v1/api/jobs/us/search/' + str(page) + '?' \
              'app_id='+param['app_id'] + '&app_key=' + param['app_key'] + '&category=' + param['category']
        p_data = get_url(url)
        if 'results' in p_data:
            data.extend(p_data['results'])

    print('get adzuna jobs: ', len(data))
    return data

if __name__ == "__main__":
    # pull_github_jobs()
    pull_adzuna_jobs()