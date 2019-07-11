import os
import time
import requests
import json
import pprint
from lxml import html

def main(tried):

    url_dashevo_insight_hash = "https://insight.dashevo.org/insight-api/status?q=getBestBlockHash"
    url_dashevo_insight_height = "https://insight.dashevo.org/insight-api/status?"
    url_blockchair = "https://api.blockchair.com/dash/stats"
    url_blockcypher = "https://api.blockcypher.com/v1/dash/main"
    url_chainz_height = "https://chainz.cryptoid.info/dash/api.dws?q=getblockcount"
    url_chainz_hash = "https://chainz.cryptoid.info/dash/api.dws?q=getblockhash&height="
    url_trezor_prefix = "https://dash"
    url_trezor_suffix = ".trezor.io/blocks"

    block_height = {}
    block_hash = {}

    block_height["dashevo_insight"] = requests.get(url_dashevo_insight_height).json()['info']['blocks']
    block_hash["dashevo_insight"] = requests.get(url_dashevo_insight_hash).json()['bestblockhash']

    blockchair_data = requests.get(url_blockchair).json()
    block_height["blockchair"] = blockchair_data['data']['best_block_height']
    block_hash["blockchair"] = blockchair_data['data']['best_block_hash']

    blockcypher_data = requests.get(url_blockcypher).json()
    block_height["blockcypher"] = blockcypher_data['height']
    block_hash["blockcypher"] = blockcypher_data['hash']

    block_height["chainz"] = requests.get(url_chainz_height).json() + 1
    block_hash["chainz"] = requests.get('{}{}'.format(url_chainz_hash, block_height["chainz"])).json()

    # Get data for trezor servers 1-5
    for i in range(1, 6):
        url_trezor = '{}{}{}'.format(url_trezor_prefix, i, url_trezor_suffix)
        page = requests.get(url_trezor)
        tree = html.fromstring(page.content)
        tr_elements = tree.xpath('//tr')

        # tr_elements[0][x] are the column names
        trezor_name = '{}{}'.format("trezor", i)
        block_height[trezor_name] = int(tr_elements[1][0].text_content())
        block_hash[trezor_name] = tr_elements[1][1].text_content()

    # Sleep this many seconds to attempt to ensure one explorer isn't just behind
    wait_time = 60

    text = ""

    uniqueValuesHeight = set(block_height.values())
    uniqueValuesHash   = set(block_hash.values())

    if len(uniqueValuesHash) > 1:
        if len(uniqueValuesHeight) > 1:
            text = "Possible fork! Explorers reporting different best block hashes and block heights.\n"
        if len(uniqueValuesHeight) == 1:
            text = "POSSIBLE FORK ALERT: Explorers reporting different best block hashes at the same height!!!"

    if len(uniqueValuesHash) > 1:
        new_dict_hash = {}
        for k, v in block_hash.items():
            new_dict_hash.setdefault(v, []).append(k)

        for item in new_dict_hash.items():
            text = text + 'Hash: {} found on Explorer(s): {}\n'.format(item[0], ', '.join(item[1]))

    if len(uniqueValuesHeight) > 1:
        new_dict_height = {}
        for k, v in block_height.items():
            new_dict_height.setdefault(v, []).append(k)

        for item in new_dict_height.items():
            text = text + 'Height: {} found on Explorer(s): {}\n'.format(item[0], ', '.join(item[1]))

    if not text == "":
        if tried>5:
            send_notification(text)
        else: 
            time.sleep(wait_time)
            print("Sleeping...")
            main(tried + 1)

# Sends a slack notification with the webhook being in secret.txt
def send_notification(text):
    secret_file = open("secret.txt", "r")
    if secret_file.mode == 'r':
        secret = secret_file.read()

    os.popen("curl -X POST -H 'Content-type: application/json' --data '{\"text\":\" " + text + " \"}' " + secret)
    print(text)

if __name__ == "__main__":
    main(0)
