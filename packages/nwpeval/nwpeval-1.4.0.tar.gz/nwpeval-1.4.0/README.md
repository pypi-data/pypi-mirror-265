# NWPeval

NWPeval is a Python package designed to facilitate the evaluation and analysis of numerical weather prediction (NWP) models. It provides a comprehensive set of metrics and tools to assess the performance of NWP models by comparing their output with observed weather data.

## Features

- Supports a wide range of evaluation metrics, including:
  - Mean Absolute Error (MAE)
  - Root Mean Square Error (RMSE)
  - Anomaly Correlation Coefficient (ACC)
  - Fractions Skill Score (FSS)
  - Equitable Threat Score (ETS)
  - Probability of Detection (POD)
  - False Alarm Ratio (FAR)
  - Critical Success Index (CSI)
  - Brier Skill Score (BSS)
  - Heidke Skill Score (HSS)
  - Peirce Skill Score (PSS)
  - Gilbert Skill Score (GS)
  - Symmetric Extreme Dependency Score (SEDS)
  - Frequency Bias (FB)
  - Gilbert Skill Score (GSS)
  - Hanssen-Kuipers Discriminant (H-KD)
  - Odds Ratio Skill Score (ORSS)
  - Extreme Dependency Score (EDS)
  - Symmetric Extremal Dependence Index (SEDI)
  - Ranked Probability Skill Score (RPSS)
  - Total Squared Error (TSE)
  - Explained Variance Score (EVS)
  - Normalized Mean Squared Error (NMSE)
  - Fractional Variance (FV)
  - Pearson Correlation Coefficient (PCC)
  - Standard Deviation Ratio (SDR)
  - Variance Inflation Factor (VIF)
  - Median Absolute Deviation (MAD)
  - Interquartile Range (IQR)
  - Coefficient of Determination (R^2)
  - Normalized Absolute Error (NAE)
  - Relative Mean Bias (RMB)
  - Mean Absolute Percentage Error (MAPE)
  - Weighted Mean Absolute Error (WMAE)
  - Absolute Skill Score (ASS)
  - Relative Skill Score (RSS)
  - Quadratic Skill Score (QSS)
  - Normalized Root Mean Squared Error (NRMSE)
  - Logarithmic Mean Bias Error (LMBE)
  - Scaled Mean Squared Error (SMSE)
  - Mean Bias Deviation (MBD)
  - Geometric Mean Bias (GMB)
  - Symmetric Brier Score (SBS)
  - Adjusted Explained Variance (AEV)
  - Cosine Similarity
  - F1 Score
  - Matthews Correlation Coefficient (MCC)
  - Balanced Accuracy (BA)
  - Negative Predictive Value (NPV)
  - Jaccard Similarity Coefficient
  - Gain
  - Lift
  - Mean Kullback-Leibler Divergence (MKLDIV)
  - Jensen-Shannon Divergence (JSDIV)
  - Hellinger Distance
  - Wasserstein Distance
  - Total Variation Distance
  - Chi-Square Distance
  - Intersection
  - Bhattacharyya Distance
  - Harmonic Mean
  - Geometric Mean
  - Lehmer Mean
  - Chernoff Distance
  - Rényi Divergence
  - Tsallis Divergence

- Flexible computation of metrics along specified dimensions or over the entire dataset.
- Support for threshold-based metrics with customizable threshold values.
- Integration with xarray and NumPy for efficient computation and data handling.
- Compatibility with both time series and spatial data, supporting 2D, 3D, and 4D datasets.
- Easy-to-use API for computing individual metrics or multiple metrics simultaneously.
- Detailed documentation and examples to guide users in utilizing the package effectively.

## Installation

You can install NWPeval using pip:

```shell
pip install nwpeval
```

## Usage

Here's a basic example of how to use NWPeval to compute evaluation metrics:

```python
import xarray as xr
from nwpeval import NWPeval

# Load the observed and modeled data
obs_data = xr.open_dataset('observed_data.nc')
model_data = xr.open_dataset('model_data.nc')

# Create an instance of NWPeval
evaluator = NWPeval(obs_data, model_data)

# Compute individual metrics
mae = evaluator.compute_mae()
rmse = evaluator.compute_rmse()
acc = evaluator.compute_acc()

# Compute multiple metrics simultaneously
metrics = ['FSS', 'ETS', 'POD', 'FAR']
thresholds = {'FSS': 0.5, 'ETS': 0.7, 'POD': 0.6, 'FAR': 0.3}
results = evaluator.compute_metrics(metrics, dim=['lat', 'lon'], thresholds=thresholds)
```

For more detailed usage instructions and examples, please refer to the examples 

## Contributing

Contributions to NWPeval are welcome! If you encounter any issues, have suggestions for improvements, or would like to contribute new features, please open an issue or submit a pull request on the GitHub repository.

## License

NWPeval is licensed under the [MIT License](LICENSE).

## Acknowledgments

We would like to express our gratitude to the developers and contributors of the libraries and tools used in building NWPeval, including NumPy, xarray, and SciPy.

## Contact

For any questions, feedback, or inquiries, please contact the maintainer:

- Name: Debasish Mahapatra
- Email: debasish.atmos@gmail.com | Debasish.mahapatra@ugent.be
- GitHub: [Your GitHub Username]

We hope you find NWPeval useful in evaluating and analyzing your numerical weather prediction models!
```

