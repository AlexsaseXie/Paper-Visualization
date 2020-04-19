import json


def paper_to_new_paper(paper, year):
    new_paper = {'id': year * 1000 + paper['id'],
                 'year': year,
                 'title': paper['title'],
                 'authors': paper['authors'],
                 'cited_count': paper['citation']['total'],
                 # 'abstract': paper['abstract'],
                 # 'link': paper['ieee_link'],
                 # 'keywords': []
                 }

    # keywords_set = set()
    # for words in paper['keywords'].values():
    #     keywords_set.update(words)
    # new_paper['keywords'] = list(keywords_set)

    new_paper['cited_by'] = []
    for info in paper['cited_by']:
        new_paper['cited_by'].append(int(info['year']) * 1000 + info['id'])

    new_paper['references'] = []
    for info in paper['reference_list']:
        new_paper['references'].append(int(info['year']) * 1000 + info['id'])

    return new_paper


paper_infos = {}
id_map = {}
new_paper_infos = {}

for year in range(2001, 2019, 2):
    with open(f'iccv/organized/iccv{year}_paper_infos.json', 'r') as f:
        paper_infos[year] = json.load(f)

for year in paper_infos:
    papers = paper_infos[year]
    new_paper_infos[year] = []
    for paper in papers:
        if len(paper) == 0:
            continue
        # 删除无引用文章
        if year > 2005 and len(paper['reference_list']) + len(paper['cited_by']) == 0:
            continue
        new_paper_infos[year].append(paper_to_new_paper(paper, year))

with open(f'iccv/paper_info.json', 'w') as f:
    json.dump(new_paper_infos, f, indent=4)
