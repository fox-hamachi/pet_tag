# Stamp Jig

Version 1.0.0

A customizable 3D-printed guide for hand-stamping a round metal tag with letter punches. Letters stay on an even pitch along each row, rows on an even pitch down the tag.

On [Cults3D](https://cults3d.com/en/3d-model/home/customizable-stamp-jig-for-round-metal-tags) and [GitHub](https://github.com/fox-hamachi/stamp-jig).

## Hardware

- **Stamps:** [OWDEN Professional 36-piece steel metal stamping set](https://www.amazon.com/dp/B07ZFB5J15), 3mm (1/8") characters, 5.95mm square shanks. Not great.. some characters are slightly different size or tilted
- **Tag:** [Framendino 10-pack round anodized aluminum pet ID tag blanks](https://www.amazon.com/dp/B08P3Z64W4), 25mm x 0.85mm, 3mm hole 3.5mm from the edge
- A steel bench block and a hammer

## Parts

- **Base:** rail with the punch slot. Clicks the sled from row to row.
- **Carriage:** holds the punch. Clicks along the rail one letter at a time.
- **Sled:** holds the tag on the bench block, pinned through the tag hole.

## Printing

| | |
|---|---|
| Material | PLA |
| Nozzle / layer | 0.4mm / 0.2mm |
| Walls / infill | 3 walls, 20% infill |
| Orientation | As exported. Carriage and sled are upside down on purpose. |
| Supports | Base only, under the tunnel. Clear the tunnel fully so the sled slides. |

Clearances were tuned on a Creality K1. If parts are tight or loose on your printer, adjust the clearances in the config and rebuild.

## Use

- Front of the base (marked FRONT) and the sled handle toward you.
- Turn the carriage so the word facing you matches the row: **ODD** for an odd number of letters, **EVEN** for an even number. For odd rows the middle letter is on the rail tick; for even rows the two middle letters sit half a letter either side of it.
- Hole row: the last sled notch puts the tag hole under the slot, for one letter each side of the hole (**EVEN**, second click each side).

## Customizing/Script Use

Change the parameters in `3mm_punch_25mm_tag.yaml` (Python) or at the top of `stamp_jig.scad` (OpenSCAD Customizer).

```
python3 -m pip install -r requirements.txt
python3 stamp_jig.py [out_dir] [config.yaml] [name=value ...]
```

- A config yaml only needs the values that differ from the defaults, e.g. `python3 stamp_jig.py my_8mm_punch.yaml`.
- `name=value` overrides single values, e.g. `python3 stamp_jig.py punch_width=8 letter_pitch=3.2`.
- Writes the three STLs to `out_dir` (default: current folder) and prints the rows and letters that fit.
- `hole_letters: false` gives a plain pin tab and no hole row.

## Files

| File | |
|---|---|
| `stamp_jig_{base,carriage,sled}.stl` | Print-ready parts |
| `stamp_jig.scad` | OpenSCAD model |
| `stamp_jig.py`, `3mm_punch_25mm_tag.yaml` | Python generator and its default config |
| `examples/` | Example tag and punch, assembly (3MF), render, photo |

## Changelog

See [Releases](https://github.com/fox-hamachi/stamp-jig/releases).

## Credit

Remix of [Guide for 8mm letter/number stamps](https://www.printables.com/model/761518) by JinPrints. Remixed by [foxhamachi](https://github.com/fox-hamachi/stamp-jig). AI-assisted design.

## License

CC BY 4.0, see `LICENSE`.
