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