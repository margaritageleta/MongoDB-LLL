import yaml
from typing import Dict
from urllib.parse import quote_plus

def get_keys(config_file):

    f = open(config_file, 'r')
    try:
        config = yaml.safe_load(f)
    except:
        raise Exception('AAA')

    return {
        'MONGODB_ATLAS_CLUSTER_URI': "mongodb+srv://%s:%s@%s" % (quote_plus(config["db_user"]), quote_plus(config["db_pass"]), config["db_host"]),  
        'OPENAI_API_KEY': config['openai_api_key'],
        'TOGETHER_API_KEY': config['together_api_key']
    }