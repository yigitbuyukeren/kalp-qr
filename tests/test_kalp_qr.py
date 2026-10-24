"""Çalıştır: python3 -m unittest discover -s tests"""
import importlib.util, os, tempfile, unittest

spec = importlib.util.spec_from_file_location("kalp_qr", os.path.join(os.path.dirname(__file__), "..", "kalp-qr.py"))
kalp = importlib.util.module_from_spec(spec); spec.loader.exec_module(kalp)

try:
    import cv2, numpy as np
except ImportError:
    cv2 = None

URL = "https://yigitbuyukeren.com/dogum-gunu/"

class KalpQr(unittest.TestCase):
    def test_png_uretir(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "k.png")
            kalp.main([URL, "-o", out, "-t", "Defne için"])
            self.assertGreater(os.path.getsize(out), 1000)

    def test_ayni_girdi_ayni_cikti(self):
        a, _ = kalp.ciz(URL); b, _ = kalp.ciz(URL)
        self.assertEqual(a.tobytes(), b.tobytes())

    def test_renk_ayrisir(self):
        self.assertEqual(kalp.hex_renk("#fff"), (255, 255, 255))
        self.assertEqual(kalp.hex_renk("d6336c"), (214, 51, 108))
        with self.assertRaises(Exception): kalp.hex_renk("#12")

    @unittest.skipIf(cv2 is None, "opencv-python yok")
    def test_telefon_okuyabilir(self):
        img, _ = kalp.ciz(URL)
        arr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        metin, _, _ = cv2.QRCodeDetector().detectAndDecode(arr)
        self.assertEqual(metin, URL)

if __name__ == "__main__":
    unittest.main()
