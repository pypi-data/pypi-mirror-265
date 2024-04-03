# mendotapy

A Python 3.6+ package for analysis-ready [Lake Mendota ice phenology](https://climatology.nelson.wisc.edu/first-order-station-climate-data/madison-climate/lake-ice/history-of-ice-freezing-and-thawing-on-lake-mendota/) data

Installing
----------

### PyPi
```sh
pip install mendotapy==1.0.0
```

### GitHub
```sh
pip install -e git+https://github.com/lgloege/mendotapy.git#egg=mendotapy
```

Using the Package
----------
**Read data into a dataframe**
```python
import mendotapy
df = mendotapy.load()
```