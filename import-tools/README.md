# Excel SOURCE-only conversion
Download the entire Drive folder as a ZIP. On a computer with Python installed:

```
pip install openpyxl
python convert_source.py /path/to/drive_chords.zip
```

Check `songs.json` and `review.csv` before importing via Admin. Excel layouts vary; this extracts chord cells from columns A:S and deliberately ignores the right-side TRANSPOSED area. Some files may use different layouts. The original application only supports chord grids; lyrics are not represented in its data schema. Do not assume the converter preserves lyrics, visual alignment, or all formatting. It does not write to Firebase.
