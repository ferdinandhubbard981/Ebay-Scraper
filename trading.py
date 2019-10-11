from ebaysdk.exception import ConnectionError


def AddToWatchList(ItemID, tradingApi):

    request = {
        "ItemID": ItemID
    }
    try:
        tradingApi.execute("RemoveFromWatchList", {"RemoveAllItems": True})
    except ConnectionError:
        print("Watchlist empty")
    try:
        response = tradingApi.execute("AddToWatchList", request)
        print(int(response.reply.WatchListMaximum) - int(response.reply.WatchListCount))
    except ConnectionError:
        print("Already in watchlist")
