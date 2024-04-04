# Google Eearth Engine Fourier Transform
This is a simple example of how to use the Fourier Transform in Google Earth Engine. The Fourier Transform is a mathematical operation that transforms a function of time or space into a function of frequency. In this example, we will use the Fourier Transform to analyze the frequency content of a time series of NDVI values.

## Installation
```bash
pip install geeft
```
or from the source code
```bash
pip install git+https://github.com/Hamilton97/gee-fourier-transform.git
```

## Usage
```python
import ee
import geeft

ee.Initialize()

# create a aoi
aoi = ee.Geometry.Point(-122.08384, 37.425937)

# create a transformation on the NDVI time series
s2_ft = geeft.s2_ft(
    aoi=aoi,
    dependent='NDVI',
    modes=3,
    years=('2018', '2022')
)
```