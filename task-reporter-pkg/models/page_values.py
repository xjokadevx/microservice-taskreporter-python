class PageValue:
    def __init__(self, xpath_query, value, attribute=""):
        self.xpath_query = xpath_query
        self.attribute = attribute
        self.value = value
