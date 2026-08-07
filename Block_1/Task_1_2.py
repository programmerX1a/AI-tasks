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
        try:
            ticket,code=barcode.split("-")
            sum=int(code)
            for i in range(len(ticket)):
                sum-=ord(ticket[i])*i
            if sum!=0 or ticket not in TicketCode.encoded:
                return "CORRUPTED TICKET"
            return ticket
        except:
            return "CORRUPTED TICKET"
            

        

        








if(__name__=="__main__"):
    ticket1=TicketCode.encode("MIA2026GATE780")
    ticket2=TicketCode.encode("MIA2026GATE7")
    ticket3=TicketCode.encode("MIA2026GATE4")
    print(f"Encoded First Ticket: {ticket1}",end="\n")
    ticket1_decode=TicketCode.decode("MIA2026GATE780-5483")
    ticket2_decode=TicketCode.decode("MIA2026GATE7-4187")
    ticket3_decode=TicketCode.decode("MIA2026GATE4-4154")
    print(f"{ticket1} Decoded: {ticket1_decode}")
    print(f"MI2026GATE780-5483 Decoded: {TicketCode.decode("MI2026GATE780-5483")}")
    print("")
    print(f"Encoded Second Ticket: {ticket2}")
    print(f"{ticket2} Decoded: {ticket2_decode}")
    print(f"MIA2025GATE7-4187 Decoded {TicketCode.decode("MIA2025GATE7-4187")}")
    print("")
    print(f"Encoded Second Ticket: {ticket3}")
    print(f"{ticket3} Decoded: {ticket3_decode}")
    print(f"MIA2025GATE7-4187 Decoded {TicketCode.decode("MIA2026GATE74187")}")


    