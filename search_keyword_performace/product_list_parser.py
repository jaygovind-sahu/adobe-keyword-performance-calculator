class ProductListParser:
    def __init__(self, product_list_string):
        parts = product_list_string.split(';')
        self.category = parts[0]
        self.product_name = parts[1]
        self.item_count = float(parts[2])
        try:
            self.total_revenue = int(parts[3])
        except ValueError:
            self.total_revenue = 0
