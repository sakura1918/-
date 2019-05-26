class Cartltem():
    def __init__(self,book,amount):
        self.amount = amount
        self.book = book
        #选做
        self.status = 1

class Cart():
    def __init__(self):
        self.save_price=0
        self.total_price=0
        self.cartltem=[]
    #计算购物车中商品节省金额一级总金额
    def sums(self):
        self.total_price=0
        self.save_price=0
        for i in self.cartltem:
            self.total_price += i.book.dangdang_price * i.amount
            self.save_price += (i.book.market_price - i.book.dangdang_price) * i.amount

    #向购物车中添加书籍
    def add_book_toCart(self,bookid):
        for i in self.cartltem:
            if i.book.id == bookid:
                i.amount += 1
                self.sums()
                return
        book = t_book.objects(id = bookid)
        self.cartltem.append(Cartltem(book,1))
        self.sums()

    #修改购物车的商品信息
    def modify_cart(self,bookid,amount):
        for i in self.cartltem:
            if i.book.id == bookid:
                i.amount = amount
        self.sums()

    #删除购物车
    def delete_book(self,bookid):
        for i in self.cartltem:
            if i.book.id == bookid:
                self.cartltem.remove(i)
        self.sums()