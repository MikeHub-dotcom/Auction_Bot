class AuctionItem(object):

    def __init__(self, name, amount, seller, bid_price, buyout_price, rarity):
        self.Name = name
        self.Amount = amount
        self.Seller = seller
        self.Bid_Price = bid_price
        self.Buyout_Price = buyout_price
        self.Rarity = rarity
        self.PricePerItem = buyout_price/amount
