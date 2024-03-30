from requests.exceptions import HTTPError

class RequiredError(Exception): ...
class BadAuthentication(Exception): ...
class NeedsBrowser(Exception): ...
class Error(Exception): ...

class Pyre:
    def __init__(self, item):
        self.item = item

    def val(self):
        return self.item[1]

    def key(self):
        return self.item[0]


def raise_detailed_error(request_object):
    try:
        request_object.raise_for_status()
    except HTTPError as e:
        # raise detailed error message
        # TODO: Check if we get a { "error" : "Permission denied." } and handle automatically
        raise HTTPError(e, request_object.text)
    
def convert_to_pyre(items):
    pyre_list = []
    for item in items:
        pyre_list.append(Pyre(item))
    return pyre_list

def convert_list_to_pyre(items):
    pyre_list = []
    for item in items:
        pyre_list.append(Pyre([items.index(item), item]))
    return pyre_list