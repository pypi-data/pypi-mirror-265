import configparser as cp
import logging
import os
from typing import Optional

from pyfrag_plotter.config.config_handler import Config

# Global variable that contains the config file. It is first empty, but will be filled in the |init| function
config: Config = Config(cp.ConfigParser())


def initialize_pyfrag_plotter(user_config_file: Optional[str] = None) -> None:
    """
    Initializes the PyFrag plotter configuration.

    This function reads the standard configuration file provided in the module and sets the config as a global variable
    that is read throughout the program. The standard configuration can be overwritten by providing a custom configuration file.

    Args:
        user_config_file (Optional[str]): The path to a custom configuration file. If provided, the settings in this file
        will overwrite the standard configuration. Defaults to None.

    Returns:
        None

    Raises:
        ValueError: If the log level specified in the configuration is invalid.
    """
    global config

    # Get the absolute path of the directory one level above the current directory
    current_dir = os.path.abspath(os.path.dirname(__file__))

    # Construct the path to the configuration file
    config_file = os.path.join(current_dir, "config", "config.ini")

    # Read the default config file
    config_parser = cp.ConfigParser()
    config_parser.read(config_file)

    # Read the user config file if provided and overwrite the config file
    if user_config_file is not None:
        config_parser.read(user_config_file)

    # Finally, check if all config keys are valid
    # This it to make it easier for providing user-friendly error messages
    config.overwrite_config(config_parser)

    try:
        logging.basicConfig(level=config.get("SHARED", "log_level"), format="%(levelname)s - %(message)s")
    except ValueError:
        logging.basicConfig(level="DEBUG", format="%(levelname)s - %(message)s")
        logging.log(logging.WARNING, f"Invalid log level '{config.get('SHARED', 'log_level')}'. Using 'DEBUG' level for finding (input) mistakes.")

    config.validate_config()
    logging.log(logging.INFO, "The config file is valid")

    # Initialize the log level and plot parameters
    _initialize_plot_parameters()
    logging.log(logging.INFO, "Initialized PyFrag plotter Succesfully")


def _initialize_plot_parameters() -> None:
    """
    Applies plot-specific parameters to matplotlib.

    This function is called by `initialize_pyfrag_plotter` and sets various parameters for matplotlib, such as the figure size,
    font family, and font size. It also tries to use the interactive backend for matplotlib, and falls back to the non-interactive
    backend if the interactive backend is not available.

    Returns:
        None
    """
    import matplotlib as mpl

    # In some occations matplotlib cannot use the interactive backend, so we try to use the non-interactive backend
    try:
        mpl.use("TkAgg")
        import matplotlib.pyplot as plt
    except ImportError:
        mpl.use("Agg")
        import matplotlib.pyplot as plt

    # Get a list of available fonts of matplotlib
    # import matplotlib.font_manager
    # flist = matplotlib.font_manager.get_fontconfig_fonts()
    # names = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in flist]
    # print(names)

    # mp.font_manager._rebuild()
    # font = fp.FontProperties(fname=r"C:\\Windows\\Fonts\\Helvetica Regulier.ttf")
    # print(font.get_name())

    # Figure size
    plt.rcParams["figure.figsize"] = config.get("MATPLOTLIB", "fig_size")

    # Font family
    plt.rcParams["font.family"] = config.get("MATPLOTLIB", "font")

    # Takes care of ticks starting at the edge of the screen
    # plt.rcParams["axes.autolimit_mode"] = "round_numbers"
    plt.rcParams["axes.xmargin"] = 0.00
    plt.rcParams["axes.ymargin"] = 0.00

    # Font size for the text in the plot including the title, xticks, and yticks
    font_size = config.get("MATPLOTLIB", "font_size")

    # Label font size for x and y axiss
    label_font_size = config.get("MATPLOTLIB", "label_size")

    # Legend font size for within the plot
    legend_font_size = config.get("MATPLOTLIB", "legend_size")

    plt.rc("font", size=font_size)  # controls default text sizes
    plt.rc("xtick", labelsize=font_size - 2)  # fontsize of the tick labels
    plt.rc("ytick", labelsize=font_size - 2)  # fontsize of the tick labels
    plt.rc("figure", titlesize=font_size + 2)  # fontsize of the figure title
    plt.rc("axes", titlesize=label_font_size)  # fontsize of the axes title
    plt.rc("axes", labelsize=label_font_size)  # fontsize of the x and y labels
    plt.rc("legend", fontsize=legend_font_size)  # legend fontsize
