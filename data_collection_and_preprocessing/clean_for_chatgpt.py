import pandas as pd
import json
import re

def clean_for_evaluation():
    try:
        with open('../data/post_history.json', 'r') as f: 
            post_history = json.load(f)
            print('JSON loaded')

        for channel in post_history.keys():
            post_history[channel] = list(filter(None, post_history[channel]))
            post_history[channel] = [re.sub(r'[([]?https:\S*', '', post) for post in post_history[channel]]  # delete links
            post_history[channel] = [re.sub(r'\*', '', post) for post in post_history[channel]]  # delete markdown symbols
            post_history[channel] = [re.sub(r'_{2,}', '', post) for post in post_history[channel]]  # delete multiple underscore

        post_history = pd.DataFrame.from_dict(post_history, orient='index')
        post_history = post_history.reset_index()
        post_history_long = pd.melt(post_history, id_vars='index', value_name='post')
        post_history_long = (
            post_history_long
            .drop('variable', axis=1)
            .rename(columns={'index': 'channel'})
            .dropna(inplace=False)
            .reset_index(drop=True)
        )
        # Uncomment if necessary: post_history_long = post_history_long[~post_history_long['post'].duplicated()]
        print('Cleaned and outputted')
        return post_history_long
    except Exception as e:
        print(f'An error occurred: {e}')
        return {}
