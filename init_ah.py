class AuctionFrame:
    def __init__(self, name, pos_search, pos_handwerkswaren):
        self.Name = name
        self.Pos_Search = pos_search
        self.Pos_Handwerkswaren = pos_handwerkswaren


def open_auction_frame():

    return

def init_auction_frame(category):
    # Koordinaten des Screenshots müssen auf die Koordinates des echten Fensters übertragen werden
    # Check if auction-house window is in the foreground
    # Simply crop the captured screenshot, since the AH-window is always at the same position (requiring a non-changing resolution of the client window)
    # Klick auf "Rücksetzen", Klick auf die gewünschte Kategorie, Klick auf "Suchen" (alles mit festgesetzten Koordinaten programmieren, später dann mit Template-matching)

    # Find all relevant templates, such as Buttons, Rollbars etc


    print("Auctionhouse window prepared.")
    return