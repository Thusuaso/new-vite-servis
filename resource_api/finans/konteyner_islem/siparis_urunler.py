from helpers import SqlConnect


class SiparisUrunler:

    def __init__(self,yil):

        data = SqlConnect().data

        self.dtUrunler = data.getStoreList(
            """
            select
            u.SatisToplam,
            u.SiparisNo
            from SiparisUrunTB u
            where u.SiparisNo in 
            (
                 Select
                s.SiparisNo from SiparislerTB s,MusterilerTB m
                where s.SiparisNo=u.SiparisNo and
                m.ID = s.MusteriID and
                Year(s.YuklemeTarihi)=? and s.SiparisDurumID in (1,2,3)
                and m.Mt_No=2
                and m.ID not in (6,34) 
            )
            """,(yil)
        )

        self.dtEskiUrunler = data.getStoreList(
            """
            select
            u.SatisToplam,
            u.SiparisNo
            from SiparisUrunTB u
            where u.SiparisNo in 
            (
                Select
                s.SiparisNo from SiparislerTB s,MusterilerTB m
                where s.SiparisNo=u.SiparisNo and
                m.ID = s.MusteriID and
                Year(s.YuklemeTarihi)<? and s.SiparisDurumID=3
                and m.Mt_No=2
                and m.ID not in (6,34)
            )
            """,(yil)
        )

        self.urunlist = list()
        self.eski_urunlist = list()

        self.__urunListOlustur()
        self.__urunListOlustur_Eski()

    def __urunListOlustur(self):

        for item in self.dtUrunler:

            data = {

                'siparisNo' : item.SiparisNo,
                'satisToplam' : float(item.SatisToplam)
            }

            self.urunlist.append(data)

    def __urunListOlustur_Eski(self):

        

        for item in self.dtEskiUrunler:

            data = {

                'siparisNo' : item.SiparisNo,
                'satisToplam' : float(item.SatisToplam)
            }

            self.eski_urunlist.append(data)


class SiparisUrunlerNew:
    def __init__(self,yil):

        data = SqlConnect().data

        self.dtUrunler = data.getStoreList(
            """
            select
            u.SatisToplam,
            u.SiparisNo
            from SiparisUrunTB u
            where u.SiparisNo in 
            (
                 Select
                s.SiparisNo from SiparislerTB s,MusterilerTB m
                where s.SiparisNo=u.SiparisNo and
                m.ID = s.MusteriID and
                Year(s.SiparisTarihi)=? and s.SiparisDurumID in (1,2,3)
                and m.Mt_No=2
                and m.ID not in (6,34) 
            )
            """,(yil)
        )

        self.dtEskiUrunler = data.getStoreList(
            """
            select
            u.SatisToplam,
            u.SiparisNo
            from SiparisUrunTB u
            where u.SiparisNo in 
            (
                Select
                s.SiparisNo from SiparislerTB s,MusterilerTB m
                where s.SiparisNo=u.SiparisNo and
                m.ID = s.MusteriID and
                Year(s.SiparisTarihi)<? and s.SiparisDurumID in (1,2,3)
                and m.Mt_No=2
                and m.ID not in (6,34)
            )
            """,(yil)
        )

        self.urunlist = list()
        self.eski_urunlist = list()

        self.__urunListOlustur()
        self.__urunListOlustur_Eski()

    def __urunListOlustur(self):

        for item in self.dtUrunler:

            data = {

                'siparisNo' : item.SiparisNo,
                'satisToplam' : float(item.SatisToplam)
            }

            self.urunlist.append(data)

    def __urunListOlustur_Eski(self):

        

        for item in self.dtEskiUrunler:

            data = {

                'siparisNo' : item.SiparisNo,
                'satisToplam' : float(item.SatisToplam)
            }

            self.eski_urunlist.append(data)


    

