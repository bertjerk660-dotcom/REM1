import unittest,struct
from pathlib import Path
from decode_thug2_ps2_font import decode
ROOT=Path(__file__).resolve().parents[1]
class FontTests(unittest.TestCase):
 def setUp(self):
  self.data=(ROOT/"build/thug2_ui_original/fonts/testtitle.fnt.ps2").read_bytes()
 def test_original_all_fonts(self):
  files=list((ROOT/"build/thug2_ui_original/fonts").glob("*.fnt.ps2"))
  self.assertEqual(len(files),8)
  for f in files:
   im,m=decode(f.read_bytes());self.assertGreater(m["glyph_count"],0)
   self.assertEqual(im.size,(m["width"],m["texture_height"]))
 def test_original_letters_and_numbers(self):
  for name in ("testtitle","newtrickfont"):
   _,m=decode((ROOT/("build/thug2_ui_original/fonts/"+name+".fnt.ps2")).read_bytes())
   codes={c for g in m["glyphs"] for c in g["codes"]}
   self.assertTrue(set(b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ").issubset(codes))
 def test_truncated(self):
  for n in (0,19,20,900,len(self.data)-1):
   with self.assertRaises((ValueError,struct.error)):decode(self.data[:n])
 def test_unknown_version(self):
  b=bytearray(self.data);struct.pack_into("<I",b,4,99)
  with self.assertRaises(ValueError):decode(b)
 def test_count_limit(self):
  b=bytearray(self.data);struct.pack_into("<I",b,8,100000)
  with self.assertRaises(ValueError):decode(b)
 def test_trailing_bytes(self):
  with self.assertRaises(ValueError):decode(self.data+b"x")
 def test_rect_bounds(self):
  b=bytearray(self.data);count=struct.unpack_from("<I",b,8)[0]
  rect_start=len(b)-count*8;struct.pack_into("<H",b,rect_start,65000)
  with self.assertRaises(ValueError):decode(b)
if __name__=="__main__":unittest.main()
