import os
import time


def main(tried):
    cmd_dashevo_insight = "curl -s https://insight.dashevo.org/insight-api/status?q=getBestBlockHash | jq .bestblockhash ;"
    cmd_blockchair = "curl -s https://api.blockchair.com/dash/stats | jq '.data.best_block_hash' ;"
    cmd_chainz = "curl -s https://chainz.cryptoid.info/dash/api.dws?q=getblockcount | xargs -I{} echo {}+1 | bc | xargs -I{} curl -s 'https://chainz.cryptoid.info/dash/api.dws?q=getblockhash&height={}' | jq ."
    cmd_blockcypher = "curl -s https://api.blockcypher.com/v1/dash/main | jq .hash"
    cmd_trezor1 = "curl -s https://dash1.trezor.io/blocks | grep -oP '(?<=<td class=\"ellipsis\">).*?(?=</td>)' | head -1 | xargs -I{} echo \\\"{}\\\" | jq . ;"
    cmd_trezor2 = "curl -s https://dash2.trezor.io/blocks | grep -oP '(?<=<td class=\"ellipsis\">).*?(?=</td>)' | head -1 | xargs -I{} echo \\\"{}\\\" | jq . ;"
    cmd_trezor3 = "curl -s https://dash3.trezor.io/blocks | grep -oP '(?<=<td class=\"ellipsis\">).*?(?=</td>)' | head -1 | xargs -I{} echo \\\"{}\\\" | jq . ;"
    cmd_trezor4 = "curl -s https://dash4.trezor.io/blocks | grep -oP '(?<=<td class=\"ellipsis\">).*?(?=</td>)' | head -1 | xargs -I{} echo \\\"{}\\\" | jq . ;"
    cmd_trezor5 = "curl -s https://dash5.trezor.io/blocks | grep -oP '(?<=<td class=\"ellipsis\">).*?(?=</td>)' | head -1 | xargs -I{} echo \\\"{}\\\" | jq . ;"

    data = {}
    data["dashevo_insight"] = get_block_hash(cmd_dashevo_insight)
    data["blockchair"] = get_block_hash(cmd_blockchair)
    data["chainz"] = get_block_hash(cmd_chainz)
#    data["blockcypher"] = get_block_hash(cmd_blockcypher)
    blockcypher = get_block_hash(cmd_blockcypher)
    data["trezor1"] = get_block_hash(cmd_trezor1)
    data["trezor2"] = get_block_hash(cmd_trezor2)
    data["trezor3"] = get_block_hash(cmd_trezor3)
    data["trezor4"] = get_block_hash(cmd_trezor4)
    data["trezor5"] = get_block_hash(cmd_trezor5)

    # Sleep this many seconds to attempt to ensure one explorer isn't just behind
    wait_time = 10

    text = ""

    uniqueValues = set(data.values())
    
    if len(uniqueValues) > 1:
        text = "Possible fork! Explorers reporting different best block hashes.\n"
        new_dict = {}
        for k, v in data.items():
            new_dict.setdefault(v, []).append(k)

        for item in new_dict.items():
            text = text + 'Hash: {} found on Explorer(s): {}\n'.format(item[0], ', '.join(item[1]))

    if blockcypher == data["dashevo_insight"]:
        text = text + 'Blockcypher (' + blockcypher + ')  appears up to date with dashevo (' + data["dashevo_insight"] + ')'

    if not text == "":
        if tried:
            send_notification(text)
        else: 
            time.sleep(wait_time)
            main(True)

def get_block_hash(cmd):
    return os.popen(cmd).read().rstrip().strip('\"')

# Sends a slack notification with the webhook being in secret.txt
def send_notification(text):
    secret_file = open("secret.txt", "r")
    if secret_file.mode == 'r':
        secret = secret_file.read()

    os.popen("curl -X POST -H 'Content-type: application/json' --data '{\"text\":\" " + text + " \"}' " + secret)
    print(text)

if __name__ == "__main__":
    main(False)
