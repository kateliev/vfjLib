# vfjLib

Low-level reader and writer for FontLab JSON (VFJ) source font files

### Installation

```
pip install --user git+https://github.com/kateliev/vfjLib
```

### Usage

```python
>>> import vfjLib
>>> jfont = vfjLib.vfjFont('testfont.vfj')
>>> jfont.dir()
Attributes (Keys) map:
   .version                   <class 'int'>
   .font                      <class 'vfjLib.object.attribdict'>
   .workspace                 <class 'vfjLib.object.attribdict'>
>>> jfont.font
<attribdict: 11>
>>> jfont.font.dir()
Attributes (Keys) map:
   .glyphsCount               <class 'int'>
   .upm                       <class 'int'>
   .glyphs                    <class 'list'>
   .interpolationFlags        <class 'int'>
   .classes                   <class 'list'>
   .openTypeFeatures          <class 'list'>
   .hinting                   <class 'vfjLib.object.attribdict'>
   .info                      <class 'vfjLib.object.attribdict'>
   .meta                      <class 'vfjLib.object.attribdict'>
   .settings                  <class 'vfjLib.object.attribdict'>
   .masters                   <class 'list'>
```

### License

- Copyright (c) 2019, Vassil Kateliev. All rights reserved.
- [BSD 3-Clause License](./LICENSE)
