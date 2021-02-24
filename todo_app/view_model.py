class ViewModel:
    def __init__(self, cards: list):
        self._cards = cards
    
    def get_cards(self, list_category: str) -> list:
        result_cards = []
        for x in self._cards:
            if x.status == list_category:
                result_cards.append(x)
        return result_cards