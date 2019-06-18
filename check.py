import os
import time

def main(tried):
    cmd_dashevo_insight = "curl -s https://insight.dashevo.org/insight-api/status?q=getBestBlockHash | jq .bestblockhash ;"
    cmd_blockchair = "curl -s https://api.blockchair.com/dash/stats | jq '.data.best_block_hash' ;"
    cmd_chainz = "curl -s https://chainz.cryptoid.info/dash/api.dws?q=getblockcount | xargs -I{} echo {}+1 | bc | xargs -I{} curl -s 'https://chainz.cryptoid.info/dash/api.dws?q=getblockhash&height={}' | jq ."
    cmd_blockcypher = "curl -s https://api.blockcypher.com/v1/dash/main | jq .hash"
    cmd_trezor1 = "curl -s https://dash1.trezor.io/blocks | grep -oP '(?<=<td class="ellipsis">).*?(?=</td>)' | head -1 | xargs -I{} echo \"{}\" | jq ."
    cmd_trezor2 = "curl -s https://dash2.trezor.io/blocks | grep -oP '(?<=<td class="ellipsis">).*?(?=</td>)' | head -1 | xargs -I{} echo \"{}\" | jq ."
    cmd_trezor3 = "curl -s https://dash3.trezor.io/blocks | grep -oP '(?<=<td class="ellipsis">).*?(?=</td>)' | head -1 | xargs -I{} echo \"{}\" | jq ."
    cmd_trezor4 = "curl -s https://dash4.trezor.io/blocks | grep -oP '(?<=<td class="ellipsis">).*?(?=</td>)' | head -1 | xargs -I{} echo \"{}\" | jq ."
    cmd_trezor5 = "curl -s https://dash5.trezor.io/blocks | grep -oP '(?<=<td class="ellipsis">).*?(?=</td>)' | head -1 | xargs -I{} echo \"{}\" | jq ."

    dashevo_insight = get_block_hash(cmd_dashevo_insight)
    blockchair = get_block_hash(cmd_blockchair)
    chainz = get_block_hash(cmd_chainz) 
    blockcypher = get_block_hash(cmd_blockcypher) 
    trezor1 = get_block_hash(cmd_trezor1)
    trezor2 = get_block_hash(cmd_trezor2)
    trezor3 = get_block_hash(cmd_trezor3)
    trezor4 = get_block_hash(cmd_trezor4)
    trezor5 = get_block_hash(cmd_trezor5)

    # Sleep this many seconds to attempt to ensure one explorer isn't just behind
    wait_time = 30

    if not dashevo_insight == blockchair:
        if tried:
            send_notification("Dashevo insights latest block hash (" + dashevo_insight + ") does not equal blockchairs latest hash (" + blockchair + ")")
            return
        else: 
            time.sleep(wait_time)
            main(True)
            return
    if not blockchair == chainz:
        if tried:
            send_notification("Blockchairs latest block hash (" + blockchair + ") does not equal Chainzs latest hash (" + chainz + ")")
            return
        else: 
            time.sleep(wait_time)
            main(True)
            return
    if not chainz == blockcypher:
        if tried:
            send_notification("Chainzs latest block hash (" + chainz + ") does not equal blockcyphers latest hash (" + blockcypher + ")")
            return
        else: 
            time.sleep(wait_time)
            main(True)
            return

def get_block_hash(cmd):
    os.popen(cmd).read().rstrip().strip('\"')

# Sends a slack notification with the webhook being in secret.txt
def send_notification(text):
    secret_file = open("secret.txt", "r")
    if secret_file.mode == 'r':
        secret = secret_file.read()

    os.popen("curl -X POST -H 'Content-type: application/json' --data '{\"text\":\" " + text + " \"}' " + secret)
    print(text)

if __name__ == "__main__":
    main(False)
