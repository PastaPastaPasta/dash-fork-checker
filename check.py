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

    data = []
    data.append(["dashevo_insight", get_block_hash(cmd_dashevo_insight)])
    data.append(["blockchair", get_block_hash(cmd_blockchair)])
    data.append(["chainz", get_block_hash(cmd_chainz)]) 
    data.append(["blockcypher", get_block_hash(cmd_blockcypher)]) 
    data.append(["trezor1", get_block_hash(cmd_trezor1)])
    data.append(["trezor2", get_block_hash(cmd_trezor2)])
    data.append(["trezor3", get_block_hash(cmd_trezor3)])
    data.append(["trezor4", get_block_hash(cmd_trezor4)])
    data.append(["trezor5", get_block_hash(cmd_trezor5)])

    # Sleep this many seconds to attempt to ensure one explorer isn't just behind
    wait_time = 10

    text = ""
    for index in range(0, len(data) - 1):

        if not data[index][1] == data[index+1][1]:
            text = text + data[index][0] + " (" + data[index][1] + ") does not equal " + data[index+1][0] + " (" + data[index+1][1] + ") \n"

    if not text == "":
        send_notification(text)
 
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
