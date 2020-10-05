# COVID-19 Project

## Inferring `geonameid` 

### Install

```bash
pip install -r requirements.txt
```

### Get datasets

See the [`data`](data) directory.

### Run

See the [`example.ipynb`](example.ipynb) Jupyter notebook for an example run.

`geoinfer.run()` returns a [`Pandas`](https://pandas.pydata.org) `DataFrame` of the ingested tweets file, with two extra columns:

* `tweet_user_location_copy`: a cleaned up and normalized copy of `tweet_user_location` (can be discarded)
* `geonameid`: the inferred geonameid

### Customize

The [`geoinfer.constants`](geoinfer/constants.py) submodule provides ways to customize inferrance, e.g.:

* `ALT_COUNTRY_NAMES`:  alternate country names (`<geonameid>: [<list of alternates>]`)
* `ALT_ADMIN1_NAMES`: ditto, but for _admin1_ entries
* `LOCATION_DISCARD`: list of location strings to ignore
* `AS_IS_LOCATIONS`: specific locations to set a `geonameid` for; applied after the normal inferrance

