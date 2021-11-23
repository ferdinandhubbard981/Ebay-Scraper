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

    print('Waiting... Press Ctrl-C to skip wait.')
    try:
        for i in range(0, 60):
            sleep(1)
        return True
    except KeyboardInterrupt:
        userInput = input("type Q to quit, anything else to keep going")
        if userInput == "Q":
            return False
        else:
            return True


graphicsCards = [
    #{"keyword": ["Casio FX-CG50", "FX-CG50"], "blacklist": ["reeeeeeeeeeeeeeeeeeeeeeeeee"], "categoryID": "9972", "averageOverride" : 150},
    {"keyword": ["RX 480 GPU", "RX 480"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"], "categoryID": "27386"},
    #{"keyword": ["GTX 1660Ti GPU", "GTX 1660Ti"], "blacklist": ["1050", "1060", "1070"], "categoryID": "27386"},
    #{"keyword": ["GTX 1070 GPU", "GTX 1070"], "blacklist": ["1050", "1060", "1080", "ti", "Ti", "TI"], "prefix": [{"name": "Asus", "suffix": ["Dual 8G"]}], "categoryID": "27386"},
    #{"keyword": ["RTX 2060 GPU", "RTX 2060"], "blacklist": ["1050", "1060", "1070", "1080", "2070", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"], "categoryID": "27386"},
    #{"keyword": ["AMD Radeon RX Vega 56 GPU", "AMD Radeon RX Vega 56"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"], "categoryID": "27386"},
    #{"keyword": ["GTX 1070Ti GPU", "GTX 1070Ti"], "blacklist": ["1050", "1060", "1080"], "categoryID": "27386"},
    #{"keyword": ["AMD Radeon RX Vega 64 GPU", "AMD Radeon RX Vega 64"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"], "categoryID": "27386"},
    #{"keyword": ["GTX 1080 GPU", "GTX 1080"], "blacklist": ["1050", "1060", "1070", "ti", "Ti", "TI"], "categoryID": "27386"},
    #{"keyword": ["RTX 2070 GPU", "RTX 2070"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"], "categoryID": "27386"},
    #{"keyword": ["AMD Radeon VII GPU", "AMD Radeon VII"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"], "categoryID": "27386"},
    #{"keyword": ["RTX 2080 GPU", "RTX 2080"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"], "categoryID": "27386"},
    #{"keyword": ["GTX 1080Ti GPU", "GTX 1080Ti"], "blacklist": ["1050", "1060", "1070", "2060", "2070", "2080", "RTX", "Rtx", "rtx"], "categoryID": "27386"},
    # {"keyword": ["Titan XP GPU", "Titan XP"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080" "GTX", "gtx", "Gtx", "RTX", "Rtx", "rtx", "ti", "Ti", "TI"], "categoryID": "27386"},
    # {"keyword": ["Titan V GPU", "Titan V"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080" "GTX", "gtx", "Gtx", "RTX", "Rtx", "rtx", "ti", "Ti", "TI"], "categoryID": "27386"},
    #{"keyword": ["RTX 2080 Ti GPU", "RTX 2080 Ti"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "GTX", "gtx", "Gtx"], "categoryID": "27386"},
    # {"keyword": ["Titan RTX GPU", "Tit  an RTX"], "blacklist": ["1050", "1060", "1070", "1080", "2060", "2070", "2080", "GTX", "gtx", "Gtx", "ti", "Ti", "TI"], "categoryID": "27386"}
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
                average = ebayFinding.findAverage(api, item["keyword"], item["blacklist"], maxPrice, minPrice, soldListingsFile, allBlacklist, dir_name, item["categoryID"])
                try:
                    average = item["averageOverride"]
                except Exception as e:
                    print()

                for item in ebayFinding.findItems(api, average, percMultiplier, item["keyword"], item["blacklist"], minPrice, file, allBlacklist, item["categoryID"]):
                    itemIdList.append(item)
            except ConnectionError as disconnected:
                print(str(disconnected))
                continue
            break
    file.close()
    soldListingsFile.close()
    trading.AddToWatchList(itemIdList, tradingApi)
    inputCheck = continuationCheck()

open(f"{dir_name}\\soldGPU's.txt")
open(f"{dir_name}\\good deals.txt")
