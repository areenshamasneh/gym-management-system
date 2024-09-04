class PaginationResponse:
    def __init__(self, items, total_items, total_pages, current_page, page_size):
        self.items = items
        self.total_items = total_items
        self.total_pages = total_pages
        self.current_page = current_page
        self.page_size = page_size

    def to_dict(self):
        return {
            "items": self.items,
            "total_items": self.total_items,
            "total_pages": self.total_pages,
            "current_page": self.current_page,
            "page_size": self.page_size,
        }
