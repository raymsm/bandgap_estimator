import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def load_uvvis_data(file_path):
    """Loads UV-Vis data from a text file.

    Args:
        file_path (str): Path to the data file. The file should have two
                         columns: wavelength (nm) and absorbance (arbitrary units),
                         separated by whitespace.

    Returns:
        pandas.DataFrame: DataFrame with 'Wavelength (nm)' and 'Absorbance' columns.
                          Returns None if the file cannot be loaded.
    """
    try:
        df = pd.read_csv(file_path, sep='\s+', comment='#', names=['Wavelength (nm)', 'Absorbance'])
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: Empty data file at {file_path}")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def tauc_plot_method(df, bandgap_type='direct'):
    """Estimates the band gap energy using the Tauc plot method.

    Args:
        df (pandas.DataFrame): DataFrame with 'Wavelength (nm)' and 'Absorbance' columns.
        bandgap_type (str): 'direct' or 'indirect' band gap. Defaults to 'direct'.

    Returns:
        tuple: Estimated band gap energy (eV) and the plot (matplotlib.figure.Figure object).
               Returns (None, None) if the data is invalid or fitting fails.
    """
    wavelength = df['Wavelength (nm)'].values
    absorbance = df['Absorbance'].values

    if len(wavelength) < 2 or len(absorbance) < 2:
        print("Error: Insufficient data for Tauc plot analysis.")
        return None, None

    # Convert wavelength to energy (eV)
    hc = 1240  # Planck's constant * speed of light (eV * nm)
    energy_ev = hc / wavelength

    # Apply the Tauc equation
    if bandgap_type == 'direct':
        tauc_y = (absorbance * energy_ev)**2
        y_label = '(αhν)²'
    elif bandgap_type == 'indirect':
        tauc_y = (absorbance * energy_ev)**(1/2)
        y_label = '(αhν)^(1/2)'
    else:
        print(f"Error: Invalid bandgap type '{bandgap_type}'. Choose 'direct' or 'indirect'.")
        return None, None

    # Linear fit to the absorption edge
    try:
        # Find the region with a significant slope (absorption edge)
        derivative = np.gradient(tauc_y, energy_ev)
        start_index = np.argmax(derivative > 0.01 * np.max(derivative)) # Heuristic for finding the start

        if start_index < 0 or start_index >= len(energy_ev) - 2:
            print("Error: Could not identify a clear absorption edge for linear fitting.")
            return None, None

        fit_energies = energy_ev[start_index:]
        fit_tauc_y = tauc_y[start_index:]

        def linear_func(x, m, c):
            return m * x + c

        popt, pcov = curve_fit(linear_func, fit_energies, fit_tauc_y, p0=[1, 0])
        slope, intercept = popt
        band_gap = -intercept / slope

        # Create the plot
        fig, ax = plt.subplots()
        ax.scatter(energy_ev, tauc_y, label='Data')
        ax.plot(fit_energies, linear_func(fit_energies, *popt), 'r-', label=f'Linear Fit (Eg ≈ {band_gap:.2f} eV)')
        ax.set_xlabel('Energy (eV)')
        ax.set_ylabel(y_label)
        ax.set_title(f'Tauc Plot ({bandgap_type.capitalize()} Band Gap)')
        ax.legend()
        ax.grid(True)

        return band_gap, fig

    except Exception as e:
        print(f"Error during Tauc plot analysis: {e}")
        return None, None

def main():
    parser = argparse.ArgumentParser(description="Estimate band gap energy from UV-Vis spectroscopy data using the Tauc plot method.")
    parser.add_argument("--uvvis", required=True, help="Path to the UV-Vis data file (wavelength vs. absorbance).")
    parser.add_argument("--method", default="tauc", choices=["tauc"], help="Method to use for band gap estimation (currently only 'tauc' is supported).")
    parser.add_argument("--type", default="direct", choices=["direct", "indirect"], help="Type of band gap ('direct' or 'indirect').")
    parser.add_argument("--plot", action="store_true", help="Show the Tauc plot.")
    parser.add_argument("--output", help="Save the plot to a file (e.g., 'tauc_plot.png').")

    args = parser.parse_args()

    if args.method == "tauc":
        df = load_uvvis_data(args.uvvis)
        if df is not None:
            band_gap, fig = tauc_plot_method(df, bandgap_type=args.type)
            if band_gap is not None:
                print(f"Estimated {args.type.capitalize()} band gap energy: {band_gap:.2f} eV")
                if args.plot:
                    plt.show()
                if args.output:
                    plt.savefig(args.output)
                    print(f"Tauc plot saved to {args.output}")
            else:
                print("Band gap estimation failed.")
    else:
        print(f"Error: Method '{args.method}' is not currently supported.")

if __name__ == "__main__":
    main()