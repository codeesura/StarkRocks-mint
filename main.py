try :
    from starknet_py.net.gateway_client import GatewayClient
    from starknet_py.contract import Contract
    from starknet_py.net.networks import TESTNET , MAINNET
    from starknet_py.net.models import StarknetChainId
    from starknet_py.net import AccountClient, KeyPair 
    from starknet_py.net.full_node_client import FullNodeClient
    import asyncio
    from web3 import Web3
except : pass
import threading
import subprocess
import sys
import pkg_resources

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
   for i in installed_packages])
if any("starknet-py" in s for s in installed_packages_list):
    pass
else :
    install("starknet.py")
    try :
        from starknet_py.net.gateway_client import GatewayClient
        from starknet_py.contract import Contract
        from starknet_py.net.networks import TESTNET , MAINNET
        from starknet_py.net.models import StarknetChainId
        from starknet_py.net import AccountClient, KeyPair 
        from starknet_py.net.full_node_client import FullNodeClient
    except : print("Starknet-py yuklenmedi hata ")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

client = GatewayClient(net=MAINNET)
def wallet_adresi(address , private_key):
    if not private_key.startswith("0x"):
        private_key = hex(int(private_key))
    account_client = AccountClient(
        address=address,
        client=client,
        key_pair=KeyPair.from_private_key(int(private_key,16)),
        chain=StarknetChainId.MAINNET,
        supported_tx_version=1
    )
    return account_client

async def mint_fonksiyon(addres, private_key):
    client_account = wallet_adresi(address=addres,private_key=private_key)
    contract = await Contract.from_address(address="0x012f8e318fe04a1fe8bffe005ea4bbd19cb77a656b4f42682aab8a0ed20702f0",client=client_account)
    starkgate_eth_contract = await Contract.from_address(address="0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7",client=client_account)
    calls = [
        starkgate_eth_contract.functions["approve"].prepare(int("0x012f8e318fe04a1fe8bffe005ea4bbd19cb77a656b4f42682aab8a0ed20702f0", 16),Web3.toWei(0.05,'ether')),
        contract.functions["publicMint"].prepare()
    ]
    print(f"{bcolors.OKCYAN}{calls}{bcolors.ENDC}")
    resp = await client_account.execute(calls=calls, max_fee=int(1e16))
    print(f"{bcolors.WARNING}{hex(resp.transaction_hash)}\nIslem kuyrukta!\n{'https://starkscan.co/tx/'+hex(resp.transaction_hash)}{bcolors.ENDC}")
    await client_account.wait_for_tx(resp.transaction_hash)
    print(f"{bcolors.OKBLUE}\nMint tamamlandi{bcolors.ENDC}")

def between_callback(address , private_key):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(mint_fonksiyon(addres=address,private_key=private_key))
    loop.close()

t1 = threading.Thread(target=between_callback, name='t1' , args=("cüzdan adresi",
"private key"))
t1.start()
