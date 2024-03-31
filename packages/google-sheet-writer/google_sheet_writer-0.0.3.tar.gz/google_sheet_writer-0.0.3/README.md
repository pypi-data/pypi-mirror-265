# google_sheet_writer

**google_sheet_writer** is an object-oriented wrapper around (amazing!) [gspread](https://github.com/burnash/gspread) and [gspread_formatting](https://github.com/robin900/gspread-formatting) that allows to programmatically create Google Sheets tables in an easy way.

On top of being convenient, it strives to minimize the amount of requests to save API quota.

Install in development mode: `pip install -e .`

See examples in `examples` folder.

The examples assume `United Kingdom` spreadsheet locale (can be changed in `File → Settings` **prior to launching generation script**). Other locales (e.g. `Russia`) might not work.
