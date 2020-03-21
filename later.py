def setPercentChanges(self):
    for stock in self.stocks:
        json = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" +
                            stock + "&apikey=" + self.KEY).json()
        print(json)
        json = json["Global Quote"]

        previousClose = float(json["08. previous close"])
        open = float(json["02. open"])

        percentChange = (open - previousClose) / previousClose

        self.percentChanges.update({stock: percentChange})

# Uses alphavantage, might come back to later