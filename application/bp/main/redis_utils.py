#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import current_app, g
import requests
from json import loads, dumps


def get_reddit_content():
    subreddit_dict = g.redis_store.get('home_page_subreddit_dict')
    current_app.logger.debug('here is our subreddit dict from redis: {}'.format(subreddit_dict))

    if subreddit_dict:
        current_app.logger.info('Reddit data is cached, returning')
        subreddit_dict = loads(subreddit_dict)
    else:
        current_app.logger.info('Unable to find subreddit dict in cache, pulling fresh')
        headers = {"User-Agent": "UCS v0.1"}
        subreddit_list = current_app.config.get('SUBREDDIT_LIST', [])
        subreddit_dict = {}
        for subreddit in subreddit_list:
            post_list = []
            json_url = 'https://www.reddit.com/r/' + subreddit + '/hot.json'
            response = requests.get(json_url, headers=headers)
            data = response.json()
            for i in xrange(current_app.config.get('MAX_REDDIT_POSTS', 1)):
                post = data['data']['children'][i]['data']
                title = post['title']
                url = post['url']
                perma_link = 'https://www.reddit.com' + post['permalink']

                if subreddit == 'programmerhumor':
                    preview_src = post['url']
                else:
                    preview_src = post['thumbnail']
                if preview_src in ['self', '', None]:
                    preview_src = ''

                post_list.append({'title': title, 'url': url, 'perma_link': perma_link, 'preview_src': preview_src})
            subreddit_dict[subreddit] = post_list
        current_app.logger.debug('Our subreddit dict: {}'.format(subreddit_dict))
        g.redis_store.setex(name='home_page_subreddit_dict', value=dumps(subreddit_dict),
                            time=current_app.config.get('REDDIT_CACHE_TTL', 3600))

    return subreddit_dict
