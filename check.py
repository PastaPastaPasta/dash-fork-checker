import os
import time

def main(tried):
    cmd_dashevo_insight = "curl -s https://insight.dashevo.org/insight-api/status?q=getBestBlockHash | jq .bestblockhash ;"
    cmd_blockchair = "curl -s https://api.blockchair.com/dash/stats | jq '.data.best_block_hash' ;"
    cmd_chainz = "curl -s https://chainz.cryptoid.info/dash/api.dws?q=getblockcount | xargs -I{} echo {}+1 | bc | xargs -I{} curl -s 'https://chainz.cryptoid.info/dash/api.dws?q=getblockhash&height={}' | jq ."
    cmd_blockcypher = "curl -s https://api.blockcypher.com/v1/dash/main | jq .hash"

    dashevo_insight = os.popen(cmd_dashevo_insight).read().rstrip().strip('\"')
    blockchair = os.popen(cmd_blockchair).read().rstrip().strip('\"')
    chainz = os.popen(cmd_chainz).read().rstrip().strip('\"') 
    blockcypher = os.popen(cmd_blockcypher).read().rstrip().strip('\"') 

    if not dashevo_insight == blockchair:
        if tried:
            send_notification("Dashevo insights latest block hash (" + dashevo_insight + ") does not equal blockchairs latest hash (" + blockchair + ")")
        else: 
            time.sleep(20)
            main(True)
    if not blockchair == chainz:
        if tried:
            send_notification("Blockchairs latest block hash (" + blockchair + ") does not equal Chainzs latest hash (" + chainz + ")")
        else: 
            time.sleep(20)
            main(True)
#    if not chainz == blockcypher:
#        if tried:
#            send_notification("Chainzs latest block hash (" + chainz + ") does not equal blockcyphers latest hash (" + blockcypher + ")")
#        else: 
#            time.sleep(20)
#            main(True)

# Sends a slack notification with the webhook being in secret.txt
def send_notification(text):
    secret_file = open("secret.txt", "r")
    if secret_file.mode == 'r':
        secret = secret_file.read()

    print("curl -X POST -H 'Content-type: application/json' --data '{\"text\":\" " + text + " \"}' " + secret)
    os.popen("curl -X POST -H 'Content-type: application/json' --data '{\"text\":\" " + text + " \"}' " + secret)

if __name__ == "__main__":
    main(False)