class TicketCode:
    encoded=[]
    @staticmethod
    def add_code(code):
        TicketCode.encoded.append(code)
    @classmethod
    def encode(self,ticket_id):
        sum=0
        for i in range(len(ticket_id)):
            sum+=ord(ticket_id[i])*i
        TicketCode.add_code(ticket_id)
        return ticket_id+"-"+str(sum)
    @classmethod
    def decode(self,barcode):
        ticket,code=barcode.split("-")
    
        sum=int(code)
        for i in range(len(ticket)):
            sum-=ord(ticket[i])*i
        if sum!=0 or ticket not in TicketCode.encoded:
            return "CORRUPTED TICKET"
        return ticket
            

        

        








if(__name__=="__main__"):
    ticket=TicketCode.encode("MIA2026GATE78")
    ticket=TicketCode.decode("MIA2026GATE780-4859")
    print(ticket)