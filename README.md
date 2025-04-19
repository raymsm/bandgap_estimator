# Band Gap Estimator(CLI based)
:warning: **Bug present in tauc's module. To be Fixed Soon.**

This is a command-line interface (CLI) tool to estimate the band gap energy of a material from UV-Vis spectroscopy data using the Tauc plot method.
**Platform** : Python
## Installation

1.  Make sure you have Python 3 installed on your system.
2.  Install the required Python libraries:
    ```bash
    pip install numpy pandas matplotlib scipy
    ```
3.  Download the `bandgap_estimator.py` script and the `sample_uvvis.txt` file (or your own UV-Vis data file).

## Usage

Open your terminal or command prompt and navigate to the directory where you saved the `bandgap_estimator.py` file.

**Basic Usage:**

To estimate the band gap from a data file (`your_data.txt`) assuming a direct band gap:

```bash
python bandgap_estimator.py --uvvis your_data.txt
```
To estimate the band gap assuming an indirect band gap:

```bash
python bandgap_estimator.py --uvvis your_data.txt --type indirect
```
**Showing the Tauc Plot:**

To display the Tauc plot:

```bash
python bandgap_estimator.py --uvvis your_data.txt --plot

```
**Saving the Tauc Plot:**

To save the Tauc plot to a file (e.g., tauc_plot.png):

```bash
python bandgap_estimator.py --uvvis your_data.txt --plot --output tauc_plot.png
```
## Help:

For more information on the available options, use the --help flag:

```bash
python bandgap_estimator.py --help
```
Input Data Format
The UV-Vis data file should be a plain text file with at least two columns separated by whitespace:

Wavelength (nm): The wavelength of the incident light in nanometers.
Absorbance: The measured absorbance at the corresponding wavelength.
Lines starting with # are treated as comments and are ignored. The file should not have a header row; the first non-comment line should contain the data.

Tauc Plot Method
The Tauc plot method is used to determine the optical band gap of semiconductor materials from UV-Vis absorbance or reflectance data. The method involves plotting $(αhν)^n$ versus $hν$, where:

$α$ is the absorption coefficient (proportional to absorbance).
$hν$ is the photon energy.
$n$ is a factor that depends on the nature of the electronic transition ($n=2$ for direct allowed transitions and $n=1/2$ for indirect allowed transitions).
By extrapolating the linear portion of the plot near the absorption edge to the energy axis, the band gap energy can be estimated.

## Contributing
[Contact me](ray94msm@gmail.com) for contributions or any questions.
