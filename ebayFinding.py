from isodate import parse_duration
from datetime import datetime, date
import os
# from webbrowser import open_new_tab


def isWithinPriceRange(itemPrice, itemShippingCost, average, percMultiplier):
    if float(itemPrice) + float(itemShippingCost) <= average * percMultiplier:
        return True
    return False


def convertToNumberOfDays(date):
    return int((datetime.now().date() - date).days)


def fileStuff(dir_name):
    try:
        os.mkdir(f"{dir_name}\\average gpu prices")
    except OSError:
        print("file already exists")

    file = open(f"{dir_name}\\good deals.txt", "w+")
    soldListingsFile = open(f"{dir_name}\\soldGPU's.txt", "w+")
    return file, soldListingsFile


def findMaxAndMinPrices(previousAverage, maxPriceMultiplier, minPriceMutlitiplier):

    if previousAverage is not None:
        maxPrice = float(previousAverage) * maxPriceMultiplier
        minPrice = float(previousAverage) * minPriceMutlitiplier
        return minPrice, maxPrice

    else:
        return 0, 10000


def readPreviousAverage(keyword, dir_name):

    firstTime = open(f"{dir_name}\\average gpu prices\\{keyword} average price.txt", "a+")
    firstTime.close()
    with open(f"{dir_name}\\average gpu prices\\{keyword} average price.txt", "r+") as averagesFile:
        lines = averagesFile.readlines()
        try:
            print(f"previous average: {lines[len(lines) - 1].split()[0]}")
            return lines[len(lines) - 1].split()[0]
        except Exception as e:
            print(f"new text file\n {e}")

        return None


def checkCurrentAveragesDate(keyword, dir_name):

    with open(f"{dir_name}\\average gpu prices\\{keyword} average price.txt", "r+") as averagesFile:
        for line in averagesFile:
            if str(date.today()) in line:
                return False

    return True


def isWithinOneDay(itemTimeRemaining):
    if "days" in str(itemTimeRemaining):
        return False
    return True


def isBlacklisted(blacklist, allBlacklist, itemTitle):

    for word in blacklist:
        if word in itemTitle:
            return False

    for word in allBlacklist:
        if word in itemTitle:
            return False

    return True


def findAverage(api, keywords, blacklist, maxPrice, minPrice, soldListingsFile, allBlacklist, dir_name):

    print(f"sold {keywords[0]}")
    soldListingsFile.write(f"sold {keywords[0]}\n\n\n")

    request = {
        "keywords": keywords,
        "soldItemsOnly": True,
        "categoryId": "27386",
        "itemFilter": [
            {"name": "Condition", "value": ["5000", "4000", "3000", "2500", "2000"]},
            {"name": "LocatedIn", "value": ["GB", "FR", "BE", "DE", "RU", "IT", "ES", "PT", "TR", "PL", "AT", "GR"]},
            {"name": "MinPrice", "value": minPrice},
            {"name": "MaxPrice", "value": maxPrice}
        ],
        "paginationInput": {
            "entriesPerPage": 25,
            "pageNumber": 1
        }
    }

    response = api.execute("findCompletedItems", request)
    total = 0
    x = 0
    # if nothing is found, an error occurs
    try:
        print(response.reply.searchResult.item[0].title)
    except (AttributeError, UnicodeEncodeError) as error:
        if error == AttributeError:
            return -1

    for item in response.reply.searchResult.item:
        if isBlacklisted(blacklist, allBlacklist, item.title):
            soldListingsFile.write(f"Price: £{float(item.sellingStatus.convertedCurrentPrice.value)}, ")
            try:
                print(f"Title: {item.title}")
                soldListingsFile.write(f"Title: {item.title}")
            except (UnicodeEncodeError) as error:
                print(error)
                soldListingsFile.write("weird name")
            print(f"Price: £{float(item.sellingStatus.convertedCurrentPrice.value)}, condition: {item.condition.conditionDisplayName}, URL: {item.viewItemURL}\n")
            soldListingsFile.write(f"condition: {item.condition.conditionDisplayName}, SaleTime: {convertToNumberOfDays(item.listingInfo.endTime.date())} days ago, URL: {item.viewItemURL}\n\n")
            total += float(item.sellingStatus.convertedCurrentPrice.value)
            x += 1

    average = total / x
    saleFrequency = x / (convertToNumberOfDays(response.reply.searchResult.item[x - 1].listingInfo.endTime.date()) + 1)
    soldListingsFile.write(f"\nSales per Day: {saleFrequency}\n\n\n")
    print(f"Average Price of {keywords[0]}: {average}")

    if checkCurrentAveragesDate(keywords[0], dir_name):

        with open(f"{dir_name}\\average gpu prices\\{keywords[0]} average price.txt", "a+") as averagesFile:
            averagesFile.write(f"\n\n{average} - {date.today()}")
    else:
        # overwrite
        with open(f"{dir_name}\\average gpu prices\\{keywords[0]} average price.txt", "r+") as averagesFile:
            lines = averagesFile.readlines()
        with open(f"{dir_name}\\average gpu prices\\{keywords[0]} average price.txt", "w") as averagesFile:
            averagesFile.writelines([item for item in lines[:-1]])
            averagesFile.write(f"{average} - {date.today()}")
    return average


def findItems(api, average, percMultiplier, keywords, blacklist, minPrice, file, allBlacklist):
    itemIdList = []
    print(f"current {keywords[0]}, Max price = {average * percMultiplier}\n\n\n")

    file.write(f"\n\nCurrent {keywords[0]}\'s, Average Price: {average}, Max price = {average * percMultiplier}\n\n\n")

    request = {
        "keywords": keywords,
        "categoryId": "27386",
        "itemFilter": [
            {"name": "Condition", "value": ["5000", "4000", "3000", "2500", "2000", "1750", "1500", "1000"]},
            {"name": "LocatedIn", "value": ["GB", "FR", "BE", "DE", "RU", "IT", "ES", "PT", "TR", "PL", "AT", "GR"]},
            {"name": "MinPrice", "value": minPrice},
            {"name": "MaxPrice", "value": average * percMultiplier}
        ],
        "paginationInput": {
            "entriesPerPage": 100,
            "pageNumber": 1
        },
        "sortOrder": "EndTimeSoonest"
    }

    response = api.execute("findItemsAdvanced", request)

    try:
        for item in response.reply.searchResult.item:
            if isBlacklisted(blacklist, allBlacklist, item.title) & isWithinOneDay({parse_duration(item.sellingStatus.timeLeft)}):
                try:
                    if isWithinPriceRange(item.sellingStatus.convertedCurrentPrice.value, item.shippingInfo.shippingServiceCost.value, average, percMultiplier):
                        print(f"Title: {item.title}, Price: £{float(item.sellingStatus.convertedCurrentPrice.value) + float(item.shippingInfo.shippingServiceCost.value)}, Time Left: {parse_duration(item.sellingStatus.timeLeft)}, sale type: {item.listingInfo.listingType}, URL: {item.viewItemURL}\n\n")
                        file.write(f"Title: {item.title}, Price: £{float(item.sellingStatus.convertedCurrentPrice.value) + float(item.shippingInfo.shippingServiceCost.value)}, Time Left: {parse_duration(item.sellingStatus.timeLeft)}, sale type: {item.listingInfo.listingType}, URL: {item.viewItemURL}\n\n")
                        itemIdList.append(item.itemId)
                except AttributeError:
                    print(f"Title: {item.title}, Time Left: {parse_duration(item.sellingStatus.timeLeft)}, sale type: {item.listingInfo.listingType}, URL: {item.viewItemURL}\n\n")
                    file.write(f"Title: {item.title}, Time Left: {parse_duration(item.sellingStatus.timeLeft)}, sale type: {item.listingInfo.listingType}, URL: {item.viewItemURL}\n\n")
                    itemIdList.append(item.itemId)
                # trading.AddToWatchList(item.itemId)
                # print(item.itemId)
                # open_new_tab(item.viewItemURL)

    except (AttributeError, UnicodeEncodeError) as error:
        print(error)
    return itemIdList
