from datetime import datetime, timedelta, time

# Decorator for get_cards function to slice result by time.
def split_result_by_updated_time(func):
    def wrapper_split_result_by_updated_time(self, list_category, \
        from_threshold = None, to_threshold = None):
        intermediate_list = func(self,list_category)
        final_list = []
        if from_threshold == None and to_threshold == None:
            final_list = intermediate_list 
            return final_list
        elif from_threshold != None and to_threshold == None:
            for x in intermediate_list:
                if x.updated_time >= from_threshold:
                    final_list.append(x)
            return final_list
        elif from_threshold == None and to_threshold != None:
            for x in intermediate_list:
                if x.updated_time < to_threshold:
                    final_list.append(x)
            return final_list
        else:
            for x in intermediate_list:
                if from_threshold <= x.updated_time < to_threshold: 
                    final_list.append(x)
            return final_list
    return wrapper_split_result_by_updated_time

class ViewModel:
    def __init__(self, cards: list):
        self._cards = cards

    @split_result_by_updated_time
    def get_cards(self, list_category = "All"):
        result_cards = []
        if list_category == "All":
            return self._cards
        else:
            for x in self._cards:
                if x.status == list_category:
                    result_cards.append(x)
            return result_cards

    def return_all_done_cards(self, limit_of_cards):
        this_is_midnight = datetime.combine(datetime.now(), time.min)
        all_done_cards = self.get_cards("Done")
        recent_done_cards = self.get_cards("Done", from_threshold = \
            this_is_midnight)
        older_done_cards = self.get_cards("Done", to_threshold = \
            this_is_midnight)
        if len(all_done_cards) > limit_of_cards:
            show_all_done_cards = False
        else:
            show_all_done_cards = True
        return [show_all_done_cards, all_done_cards, recent_done_cards, \
            older_done_cards]
