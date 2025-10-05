from kaggle.api.kaggle_api_extended import KaggleApi

def search_kaggle(query):
    api = KaggleApi()
    api.authenticate()
    datasets = api.dataset_list(search=query)
    return [
        {
            "ref": d.ref,
            "title": d.title,
            "subtitle": d.subtitle,
            "url": d.url
        }
        for d in datasets
    ]
