# Google Earth Engine Fourier Transform

from math import pi
from typing import Callable
import ee

if not ee.data._credentials:
    ee.Initialize()


class S2Dataset(ee.ImageCollection):
    """
    A class representing a Sentinel-2 dataset in Google Earth Engine.

    This class extends the `ee.ImageCollection` class and provides additional methods
    for processing Sentinel-2 imagery.

    Attributes:
        None
    """

    def __init__(self):
        super().__init__("COPERNICUS/S2_HARMONIZED")

    def add_ndvi(self):
        self.map(
            lambda x: x.addBands(x.normalizedDifference(["B8", "B4"])).rename("NDVI")
        )
        return self

    def apply_cloud_mask(self):
        self.map(self.cloud_mask)
        return self

    @staticmethod
    def cloud_mask(image: ee.Image):
        qa = image.select("QA60")
        # Bits 10 and 11 are clouds and cirrus, respectively.
        cloud_bit_mask = 1 << 10
        cirrus_bit_mask = 1 << 11
        # Both flags should be set to zero, indicating clear conditions.
        mask = (
            qa.bitwiseAnd(cloud_bit_mask)
            .eq(0)
            .And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
        )

        return image.updateMask(mask)


def get_names(prefix: str, frequencies: list[int]) -> list[str]:
    return [f"{prefix}_{freq}" for freq in frequencies]


def add_constant(image) -> ee.Image:
    return image.addBands(ee.Image(1))


def add_time(image: ee.Image) -> ee.Image:
    date = image.date()
    years = date.difference(ee.Date("1970-01-01"), "year")
    time_radians = ee.Image(years.multiply(2 * pi))
    return image.addBands(time_radians.rename("t").float())


def add_harmonics(
    freqs: list[int], cos_names: list[str], sin_names: list[str]
) -> Callable:
    def wrapper(image: ee.Image):
        frequencies = ee.Image.constant(freqs)
        time = ee.Image(image).select("t")
        cosine = time.multiply(frequencies).cos().rename(cos_names)
        sines = time.multiply(frequencies).sin().rename(sin_names)
        return image.addBands(cosine).addBands(sines)

    return wrapper


def compute_phase(cos: str, sin: str):
    name = f'phase_{cos.split("_")[-1]}'

    def wrapper(image: ee.Image) -> ee.Image:
        return image.addBands(
            image.select(cos).atan2(image.select(sin)).unitScale(-pi, pi).rename(name)
        )

    return wrapper


def compute_amplitude(cos: str, sin: str):
    name = f'amplitude_{cos.split("_")[-1]}'

    def wrapper(image: ee.Image):
        return image.addBands(image.select(cos).hypot(image.select(sin)).rename(name))

    return wrapper


def compute_fourier_transform(
    dataset: ee.ImageCollection, dependent: str, modes: int = 3
) -> ee.Image:
    """
    Computes the Fourier transform of an image collection.

    Args:
        dataset (ee.ImageCollection): The input image collection.
        dependent (str): The dependent variable to be used in the regression.
        modes (int, optional): The number of Fourier modes to include. Defaults to 3.

    Returns:
        ee.Image: The Fourier transformed image.

    Raises:
        None

    Examples:
        # Compute Fourier transform with 3 modes
        result = compute_fourier_transform(dataset, "dependent_variable", 3)
    """

    frequencies = list(range(1, modes + 1))
    cos_names = get_names("cos", frequencies)
    sin_names = get_names("sin", frequencies)

    independents = ["t", "constant"] + cos_names + sin_names

    dataset = (
        dataset.map(add_constant)
        .map(add_time)
        .map(add_harmonics(frequencies, cos_names, sin_names))
    )

    trend: ee.Image = dataset.select(independents + [dependent]).reduce(
        ee.Reducer.linearRegression(len(independents), 1)
    )
    coefficients = (
        trend.select("coefficients").arrayProject([0]).arrayFlatten([independents])
    )

    # add coefficients to each image in the dataset
    dataset = dataset.select(dependent).map(lambda x: x.addBands(coefficients))

    for cos, sin in zip(cos_names, sin_names):
        dataset = dataset.map(compute_phase(cos, sin)).map(compute_amplitude(cos, sin))

    # transform and return
    return dataset.median().unitScale(-1, 1)


def s2_ft(
    aoi: str, dependent: str = None, modes: int = 3, years: tuple[str] = None
) -> ee.Image:
    """
    Computes the Fourier transform of Sentinel-2 data.

    Args:
        aoi (str): The area of interest.
        dependent (str, optional): The dependent variable. Defaults to NDVI.
        modes (int, optional): The number of Fourier modes to compute. Defaults to 3.
        years (tuple[str], optional): The years to filter the data. Defaults to ("2018", "2022").

    Returns:
        ee.Image: The Fourier transform result.
    """
    years = years or ("2018", "2022")
    dependent = dependent or "NDVI"

    dataset = (
        S2Dataset().filterBounds(aoi).filterDate(*years).apply_cloud_mask().add_ndvi()
    )
    return compute_fourier_transform(dataset=dataset, dependent=dependent, modes=modes)
