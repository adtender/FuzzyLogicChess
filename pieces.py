from tkinter import PhotoImage

def pieces(self):
        self.br = PhotoImage(file="./icons/br.png")
        lbr1, lbr2 = "11", "81"
        self.add_piece(self.br, lbr1)
        self.add_piece(self.br, lbr2)

        self.bkn = PhotoImage(file="./icons/bkn.png")
        lbkn1, lbkn2 = "21", "71"
        self.add_piece(self.bkn, lbkn1)
        self.add_piece(self.bkn, lbkn2)

        self.bb = PhotoImage(file="./icons/bb.png")
        lbb1, lbb2 = "31", "61"
        self.add_piece(self.bb, lbb1)
        self.add_piece(self.bb, lbb2)

        self.bq = PhotoImage(file="./icons/bq.png")
        lbq = "41"
        self.add_piece(self.bq, lbq)

        self.bk = PhotoImage(file="./icons/bk.png")
        lbk = "51"
        self.add_piece(self.bk, lbk)

        
        self.bp = PhotoImage(file="./icons/bp.png")
        lbp1, lbp2, lbp3, lbp4, lbp5, lbp6, lbp7, lbp8 = "12", "22", "32", "42", "52", "62", "72", "82"
        self.add_piece(self.bp, lbp1)
        self.add_piece(self.bp, lbp2)
        self.add_piece(self.bp, lbp3)
        self.add_piece(self.bp, lbp4)
        self.add_piece(self.bp, lbp5)
        self.add_piece(self.bp, lbp6)
        self.add_piece(self.bp, lbp7)
        self.add_piece(self.bp, lbp8)
        
        
        self.wr = PhotoImage(file='./icons/wr.png')
        lwr1, lwr2 = "18", "88"
        self.add_piece(self.wr, lwr1)
        self.add_piece(self.wr, lwr2)

        self.wkn = PhotoImage(file="./icons/wkn.png")
        lwkn1, lwkn2 = "28", "78"
        self.add_piece(self.wkn, lwkn1)
        self.add_piece(self.wkn, lwkn2)

        self.wb = PhotoImage(file="./icons/wb.png")
        lwb1, lwb2 = "38", "68"
        self.add_piece(self.wb, lwb1)
        self.add_piece(self.wb, lwb2)

        self.wq = PhotoImage(file="./icons/wq.png")
        lwq = "48"
        self.add_piece(self.wq, lwq)

        self.wk = PhotoImage(file="./icons/wk.png")
        lwk = "58"
        self.add_piece(self.wk, lwk)

        self.wp = PhotoImage(file="./icons/wp.png")
        lwp1, lwp2, lwp3, lwp4, lwp5, lwp6, lwp7, lwp8 = "17", "27", "37", "47", "57", "67", "77", "87"
        self.add_piece(self.wp, lwp1)
        self.add_piece(self.wp, lwp2)
        self.add_piece(self.wp, lwp3)
        self.add_piece(self.wp, lwp4)
        self.add_piece(self.wp, lwp5)
        self.add_piece(self.wp, lwp6)
        self.add_piece(self.wp, lwp7)
        self.add_piece(self.wp, lwp8)