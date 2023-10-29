# OGNtoXC

Small utility to pull all FLARM IDs from OGN Device DB, filter aircraft of interest, and output a file in XCSoar compatible format.

This is useful as XCSoar supports a max of 200 FLARM Identifications.

## Sample usage:
Eg. filter from a list of competition IDs pulled from Soaring Spot for a contest. Also filter registrations for a given country to avoid duplicates.

```python
python -m venv env
source env/bin/activate
pip install -r requirements.txt

python OGNtoXC.py "LV-" "SE,4,C1,JA"
```