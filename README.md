---
this_file: README.md
---

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
>>> jfont.font.glyphs[-1].layers[0].elements[0].component.glyphName
'l'
>>> jfont.font.glyphs[-1].layers[0].elements[0].component.glyphName = 'n'
>>> jfont.font.glyphs[-1].layers[0].elements[0].component.glyphName
'n'
>>> jfont.save('savedfont.vfj')
```

### License

- Copyright (c) 2019, Vassil Kateliev. All rights reserved.
- [BSD 3-Clause License](./LICENSE)


## Development and acceptance

A low-level reader and writer for FontLab JSON (VFJ) files.

`Lib/vfjLib/` contains the package, `Tools/` contains utilities and `Doc/` is reserved for reference material and currently contains only an empty placeholder.

## Checks

The observed source base is `bf87275fba54bc2959b112391b2bca43d7ded621`.
`setup.py` packages `Lib/vfjLib/`. `Tools/` contains utilities and `Doc/` is reserved
for reference material and currently contains only an empty placeholder.
No tracked suite or test wrapper is established.
The pytest metadata in `setup.py` does not supply tests.
Before a writer change, define an owned VFJ fixture and a complete-data
preservation contract. Verify saved and reopened output. Keep unsupported fields
and native compatibility limits explicit. Never use an owner font as a fixture.

Preserve Vassil Kateliev’s authorship and BSD 3-Clause terms in LICENSE.

Read [AGENTS.md](AGENTS.md) for the review and delivery workflow.
Track future work in [PLAN.md](PLAN.md) and [TODO.md](TODO.md).
Issue 123 remains paused. Source, native, installed and release results remain separate.
