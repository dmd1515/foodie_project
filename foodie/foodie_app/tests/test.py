from django.test import TestCase, Client
from django.urls import reverse
import json
from myapp.models import Zinute  # Tarkime, kad turite Zinute modelį

class ZinuciuVienetiniaiTestai(TestCase):
    """Vienetiniai testai žinučių validacijai ir apdorojimui"""
    def setUp(self):
        self.client = Client()
        self.nuoroda = reverse('siusti_zinute')
        self.galima_zinute = "Tai yra tinkama žinutė"
        self.per_ilga_zinute = "a" * 301
        self.tuscia_zinute = ""
        self.specialiu_simboliu_zinute = "!@#$%^&*()_+{}|:\"<>?~`-=[]\\;',./"
        self.maksimalaus_ilgio_zinute = "a" * 300

    def test_siusti_galima_zinute(self):
        """Vienetinis testas: tinkamos žinutės siuntimas"""
        atsakas = self.client.post(
            self.nuoroda,
            {'zinute': self.galima_zinute},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(atsakas.status_code, 200)
        duomenys = json.loads(atsakas.content)
        self.assertEqual(duomenys['pavyko'], 'Žinutė išsiųsta!')

    def test_siusti_tuscia_zinute(self):
        """Vienetinis testas: tuščios žinutės siuntimas"""
        atsakas = self.client.post(
            self.nuoroda,
            {'zinute': self.tuscia_zinute},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(atsakas.status_code, 400)
        duomenys = json.loads(atsakas.content)
        self.assertEqual(duomenys['klaida'], 'Žinutė negali būti tuščia.')


class ZinuciuIntegraciniaiTestai(TestCase):
    """Integraciniai testai tarp komponentų"""
    def setUp(self):
        self.client = Client()
        self.siuntimo_nuoroda = reverse('siusti_zinute')
        self.saraso_nuoroda = reverse('zinuciu_sarasas')
        self.testine_zinute = "Integracinio testo žinutė"
    
    def test_zinutes_keliavimas_nuo_kliento_iki_duomenu_bazes(self):
        """Integracinis testas: visas kelias nuo kliento iki duomenų bazės"""
        # Siunčiame žinutę per API
        atsakas = self.client.post(
            self.siuntimo_nuoroda,
            {'zinute': self.testine_zinute},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(atsakas.status_code, 200)
        
        # Tikriname, ar žinutė išsaugota duomenų bazėje
        zinute = Zinute.objects.first()
        self.assertIsNotNone(zinute)
        self.assertEqual(zinute.turinys, self.testine_zinute)
        
        # Tikriname, ar žinutė rodoma sąrašo API
        saraso_atsakas = self.client.get(self.saraso_nuoroda)
        self.assertEqual(saraso_atsakas.status_code, 200)
        self.assertContains(saraso_atsakas, self.testine_zinute)

    def test_zinuciu_validavimas_tarp_lygiu(self):
        """Integracinis testas: validacija tarp kliento ir serverio"""
        # Testuojame per ilgą žinutę
        per_ilga_zinute = "a" * 301
        atsakas = self.client.post(
            self.siuntimo_nuoroda,
            {'zinute': per_ilga_zinute},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(atsakas.status_code, 400)
        
        # Tikriname, kad žinutė nebuvo išsaugota
        self.assertEqual(Zinute.objects.count(), 0)
        
        # Testuojame tinkamą žinutę
        galima_zinute = "Tinkama žinutė"
        atsakas = self.client.post(
            self.siuntimo_nuoroda,
            {'zinute': galima_zinute},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(atsakas.status_code, 200)
        self.assertEqual(Zinute.objects.count(), 1)

    def test_zinutes_apdorojimo_grandine(self):
        """Integracinis testas: žinutės apdorojimas per kelis komponentus"""
        # Siunčiame žinutę
        testine_zinute = "Testinė žinutė"
        atsakas = self.client.post(
            self.siuntimo_nuoroda,
            {'zinute': testine_zinute},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(atsakas.status_code, 200)
        
        # Tikriname duomenų bazę
        zinute = Zinute.objects.first()
        self.assertEqual(zinute.turinys, testine_zinute)
        self.assertIsNotNone(zinute.laiko_zymė)
        
        # Tikriname, ar žinutė buvo apdorota (jei taip numatyta)
        self.assertTrue(zinute.apdorota)
        
        # Tikriname, ar buvo sukurta pranešimą (jei taip numatyta)
        # self.assertEqual(Pranesimas.objects.count(), 1)


class ZinuciuAPIKomponenciuTestai(TestCase):
    """Testai tarp skirtingų API komponentų"""
    def setUp(self):
        self.client = Client()
        self.siuntimo_nuoroda = reverse('siusti_zinute')
        self.statistika_nuoroda = reverse('zinuciu_statistika')
    
    def test_zinuciu_statistiku_integracija(self):
        """Integracinis testas tarp žinučių ir statistikos komponentų"""
        # Siunčiame kelias žinutes
        zinutes = ["Testas 1", "Testas 2", "Testas 3"]
        for zinute in zinutes:
            atsakas = self.client.post(
                self.siuntimo_nuoroda,
                {'zinute': zinute},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            self.assertEqual(atsakas.status_code, 200)
        
        # Tikriname statistiką
        statistikos_atsakas = self.client.get(self.statistika_nuoroda)
        self.assertEqual(statistikos_atsakas.status_code, 200)
        statistikos_duomenys = json.loads(statistikos_atsakas.content)
        
        self.assertEqual(statistikos_duomenys['viso_zinuciu'], 3)
        self.assertEqual(statistikos_duomenys['vidutinis_ilgis'], 6.0)
        
    def test_zinutes_ir_vartotojo_integracija(self):
        """Integracinis testas tarp žinučių ir vartotojų komponentų"""
        # Sukuriame testinį vartotoją
        vartotojo_duomenys = {
            'vartotojo_vardas': 'testuotojas',
            'slaptazodis': 'testuotojoSlaptazodis123'
        }
        self.client.post(reverse('registruoti'), vartotojo_duomenys)
        
        # Prisijungiame
        self.client.login(username='testuotojas', password='testuotojoSlaptazodis123')
        
        # Siunčiame žinutę kaip prisijungęs vartotojas
        atsakas = self.client.post(
            self.siuntimo_nuoroda,
            {'zinute': "Vartotojo žinutė"},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(atsakas.status_code, 200)
        
        # Tikriname vartotojo asociaciją
        zinute = Zinute.objects.first()
        self.assertEqual(zinute.vartotojas.vartotojo_vardas, 'testuotojas')