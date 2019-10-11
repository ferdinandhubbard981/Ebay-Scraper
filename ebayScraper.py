import ebayFinding
import trading
from ebaysdk.finding import Connection
from ebaysdk.trading import Connection as tradeConnect
import os
from webbrowser import open
from time import sleep
from requests.exceptions import ConnectionError
import credentialsconfiguration


def continuationCheck():

    print('Waiting... please press Ctrl-C when you wish to proceed.')
    try:
        for i in range(0, 60):
            sleep(1)
        return True
    except KeyboardInterrupt:
        userInput = input("pls type Q to quit, anything else to keep going")
        if userInput == "Q":
            return False
        else:
            return True


graphicsCards = [
    {"keyword": ["RX 480 PU", "RX 480"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"]},

    {"keyword": ["GTX 1660Ti GPU", "GTX 1660Ti"], "blacklist": ["1050", "1060", "1070"]},
    {"keyword": ["GTX 1070 GPU", "GTX 1070"], "blacklist": ["1050", "1060", "1080", "ti", "Ti", "TI"], "prefix": [{"name": "Asus", "suffix": ["Dual 8G"]}]},
    {"keyword": ["RTX 2060 GPU", "RTX 2060"], "blacklist": ["1050", "1060", "1070", "1080", "2070", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"]},
    {"keyword": ["AMD Radeon RX Vega 56 GPU", "AMD Radeon RX Vega 56"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"]},
    {"keyword": ["GTX 1070Ti GPU", "GTX 1070Ti"], "blacklist": ["1050", "1060", "1080"]},
    {"keyword": ["AMD Radeon RX Vega 64 GPU", "AMD Radeon RX Vega 64"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"]},
    {"keyword": ["GTX 1080 GPU", "GTX 1080"], "blacklist": ["1050", "1060", "1070", "ti", "Ti", "TI"]},
    {"keyword": ["RTX 2070 GPU", "RTX 2070"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"]},
    {"keyword": ["AMD Radeon VII GPU", "AMD Radeon VII"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"]},
    {"keyword": ["RTX 2080 GPU", "RTX 2080"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"]},
    {"keyword": ["GTX 1080Ti GPU", "GTX 1080Ti"], "blacklist": ["1050", "1060", "1070", "2060", "2070", "2080", "RTX", "Rtx", "rtx"]},
    # {"keyword": ["Titan XP GPU", "Titan XP"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080" "GTX", "gtx", "Gtx", "RTX", "Rtx", "rtx", "ti", "Ti", "TI"]},
    # {"keyword": ["Titan V GPU", "Titan V"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080" "GTX", "gtx", "Gtx", "RTX", "Rtx", "rtx", "ti", "Ti", "TI"]},
    {"keyword": ["RTX 2080 Ti GPU", "RTX 2080 Ti"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "GTX", "gtx", "Gtx"]},
    # {"keyword": ["Titan RTX GPU", "Tit  an RTX"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"]}
]
percMultiplier = 0.85
maxPriceMultiplier = 1.6
minPriceMutlitiplier = 0.4
dir_name = os.path.dirname(os.path.realpath(__file__))
credentialsconfiguration.ebay_yaml(dir_name)
api = Connection(config_file="ebay.yaml", debug=False, siteid="EBAY-GB")
tradingApi = tradeConnect(config_file="ebay.yaml", debug=False)

allBlacklist = ["waterblock", "Waterblock", "Bracket/Brace"]
inputCheck = True
while inputCheck:
    itemIdList = []
    file, soldListingsFile = ebayFinding.fileStuff(dir_name)
    for item in graphicsCards:
        previousAverage = ebayFinding.readPreviousAverage(item["keyword"][0], dir_name)
        minPrice, maxPrice = ebayFinding.findMaxAndMinPrices(previousAverage, maxPriceMultiplier, minPriceMutlitiplier)
        print(f"{maxPrice}, {minPrice}")
        while True:
            try:
                average = ebayFinding.findAverage(api, item["keyword"], item["blacklist"], maxPrice, minPrice, soldListingsFile, allBlacklist, dir_name)
                for item in ebayFinding.findItems(api, average, percMultiplier, item["keyword"], item["blacklist"], minPrice, file, allBlacklist):
                    itemIdList.append(item)
            except ConnectionError as disconnected:
                print(disconnected)
                continue
            break
    file.close()
    soldListingsFile.close()
    trading.AddToWatchList(itemIdList, tradingApi)
    inputCheck = continuationCheck()

open(f"{dir_name}\\soldGPU's.txt")
open(f"{dir_name}\\good deals.txt")
