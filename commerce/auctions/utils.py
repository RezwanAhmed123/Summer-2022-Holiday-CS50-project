def is_current_user(request, query_user, context):
    if request.user == query_user:
        is_current_user = True
        context["is_current_user"] = True
    return context

def get_number_of_unique_bidders(bidder_list):
    unique_bidders = []
    for bidder in bidder_list:
        if bidder not in unique_bidders:
            unique_bidders.append(bidder)
    return len(unique_bidders)

def get_unique_bidders(bidder_list):
    unique_bidders = []
    for bidder in bidder_list:
        if bidder not in unique_bidders:
            unique_bidders.append(bidder.id)
    return unique_bidders

def update_past_bidders(item, bid_list):
    if item.past_bidders:
        item.past_bidders.set([])
        for bid in bid_list:
            bidder = bid.bidder
            item.past_bidders.add(bidder)
    else:
        item.past_bidders.set([])

def get_items_in_category(item_list, category):
    items = []
    for item in item_list:
        if category in item.category.all():
            items.append(item)
    return items
    