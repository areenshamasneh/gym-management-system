class PaginationResponse:
    def __init__(self, items, total_items, current_page, page_size):
        self.items = items
        self.total_items = total_items
        self.current_page = current_page
        self.page_size = page_size
        self.total_pages = self.calculate_total_pages()

    def calculate_total_pages(self):
        return (self.total_items + self.page_size - 1) // self.page_size

    def to_dict(self):
        return {
            "items": self.items,
            "total_items": self.total_items,
            "total_pages": self.total_pages,
            "current_page": self.current_page,
            "page_size": self.page_size,
        }
