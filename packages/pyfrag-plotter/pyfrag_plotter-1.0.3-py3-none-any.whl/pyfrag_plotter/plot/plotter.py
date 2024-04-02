import logging
import os
import time
from os.path import join as opj
from typing import List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
from attrs import define, field

from pyfrag_plotter import config
from pyfrag_plotter.plot.plot_details import set_axes_details, set_figure_details
from pyfrag_plotter.pyfrag_object import PyFragResultsObject


def plot_logger(log_level=logging.INFO):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logging.log(log_level, f"Plotting with {func.__name__}. Time taken: {end_time - start_time:.2f} seconds.")
            return result

        return wrapper

    return decorator


@define
class PlotInfo:
    """Class to hold information about the plot to be generated.

    Attributes:
        irc_coord (str): The IRC coordinate to plot on the x-axis.
        irc_coord_label (str): The label for the x-axis.
        colours (List[str]): The list of colours to use for the plot.
        line_styles (List[str]): The list of line styles to use for the plot.
        peak_type (Optional[str]): The type of peak to plot, if any.

    """

    irc_coord: str
    irc_coord_label: str
    colours: List[str] = field(factory=lambda: config.get("SHARED", "colours"))
    line_styles: List[str] = field(factory=lambda: config.get("SHARED", "line_styles"))
    peak_type: Optional[str] = field(factory=lambda: config.get("SHARED", "stat_point_type") if config.get("SHARED", "stat_point_type") != "none" else None)


class Plotter:
    """
    This class provides methods for plotting the results of the PyFrag calculations. It supports plotting of activation
    strain model terms, energy decomposition terms, and extra strain terms. The plots are saved to a specified directory.

    Additionally, the "standard_plot_routine" method can be used to plot any key (or a combination of) in the PyFragResultsObject and the user may create specicifed functions using this method.

    Attributes:
        name (str): The name of the plotter object.
        objects (Sequence[PyFragResultsObject]): A list of PyFragResultsObject objects that contain the data to be plotted.
        path (str): The directory to save the plots to.
        plot_info (PlotInfo): An instance of the PlotInfo class that contains information about the plot, such as the
                            line styles and colors.

    Note: The plotter object can be used with a "with" statement to ensure that the plot directory is removed if it's empty.
    """

    def __init__(self, name: str, plot_dir: str, pyfrag_objects: Sequence[PyFragResultsObject], irc_coord: Sequence[str]):
        """
        Initializes the Plotter object.

        Args:
            name (str): The name of the plotter object.
            plot_dir (str): The directory to save the plots to.
            pyfrag_objects (Sequence[PyFragResultsObject]): A list of PyFragResultsObject objects that contain the data to be plotted.
            irc_coord (Sequence[str]): A sequence of two strings that specify the IRC coordinate and its label.
        """
        self.name = name
        self.objects = pyfrag_objects
        self.path = opj(plot_dir, name)
        self.plot_info = PlotInfo(irc_coord=irc_coord[0], irc_coord_label=irc_coord[1])

    def __enter__(self):
        """
        Prepares the plotter object for use with a "with" statement.

        This method checks if the specified directory exists for making plots. If not, it creates it (and any parent directories).
        """
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Cleans up the plotter object after use with a "with" statement.

        This method makes sure to close the plotter object and remove the plot directory if it's empty.
        """
        for root, dirs, files in os.walk(self.path, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if len(os.listdir(dir_path)) == 0:
                    os.rmdir(dir_path)

    # ------------------------------------------------------------------------------------------------------------- #
    # ------------------------------ ASM, EDA and ASM extra strain plotting routines ------------------------------ #
    # ------------------------------------------------------------------------------------------------------------- #

    def standard_plot_routine(self, keys: Sequence[str], ax: Optional[plt.Axes] = None, markers: Optional[Sequence[str]] = None):
        """
        The standard plot routine for the EDA, ASM and extra strain plots.

        This method plots the specified keys for each PyFragResultsObject in the plotter. It supports plotting of multiple keys
        on the same axes, and allows for customization of the line styles and markers.

        Args:
            keys (Sequence[str]): The keys to plot. These should match the keys in the corresponding dictionary type (asm, eda or extra_strain).
            ax (Optional[plt.Axes], optional): The axes to plot on. If None, the current axes is used. Defaults to None.
            markers (Optional[Sequence[str]], optional): The markers to use for the lines. If None, no markers are used. Defaults to None.
        """
        ax = plt.gca() if ax is None else ax
        markers = [""] * len(self.objects) if markers is None else markers

        x_axes = [obj.get_x_axis(self.plot_info.irc_coord) for obj in self.objects]
        for i, (line_style, term) in enumerate(zip(self.plot_info.line_styles, keys)):
            for x_axis, colour, obj, line_marker in zip(x_axes, self.plot_info.colours, self.objects, markers):
                term_data = obj.get_data_of_key(term)  # eda, asm or extra_strain

                # Plot the data. If it's the first object, associate a label with the line
                if i == 0:
                    ax.plot(x_axis, term_data, label=obj.name, color=colour, linestyle=line_style, marker=line_marker, zorder=1)
                else:
                    # Otherwise, just plot the data
                    ax.plot(x_axis, term_data, color=colour, linestyle=line_style, marker=line_marker, zorder=1)

                # If a peak type is specified, plot the peak
                if i == 0 and self.plot_info.peak_type is not None:
                    peak_index = obj.get_peak_index(peak=self.plot_info.peak_type)
                    ax.scatter(x_axis[peak_index], term_data[peak_index], color=colour, s=90, zorder=2)

    @plot_logger()
    def plot_asm(self, keys: Optional[List[str]] = None, **kwargs) -> Tuple[plt.Figure, plt.Axes]:
        """
        Plots the activation strain model terms.

        This method plots the specified ASM terms for each PyFragResultsObject in the plotter. If no terms are specified, all terms are plotted.

        Args:
            keys (Optional[List[str]], optional): The ASM terms to plot. If None, all terms are plotted. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the `set_axes_details` and `set_figure_details` functions.

        Returns:
            fig (plt.Figure): The figure object.
            ax (plt.Axes): The axes object.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Get the keys to plot. If none are specified, plot all of them
        if keys is None:
            asm_keys: List[str] = config.get("ASM", "asm_keys")
        else:
            asm_keys = keys

        # Plot the keys
        self.standard_plot_routine(asm_keys, ax)

        # Since the same keys are plotted for all objects, we can just use the first object to get the labels
        labels = self.objects[0].get_plot_labels(asm_keys)

        # Set the key-specific plot details
        set_axes_details(ax=ax, x_label=self.plot_info.irc_coord_label, line_style_labels=labels, **kwargs)
        set_figure_details(fig=fig, title=f"ASM_{'_'.join(asm_keys)}", savefig=opj(self.path, f"ASM_{'_'.join(asm_keys)}.png"), line_style_labels=labels, **kwargs)
        return fig, ax

    @plot_logger()
    def plot_eda(self, keys: Optional[List[str]] = None, **kwargs) -> Tuple[plt.Figure, plt.Axes]:
        """
        Plots the energy decomposition terms.

        This method plots the specified EDA terms for each PyFragResultsObject in the plotter. If no terms are specified, all terms are plotted.

        Args:
            keys (Optional[List[str]], optional): The EDA terms to plot. If None, all terms are plotted. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the `set_axes_details` and `set_figure_details` functions.

        Returns:
            fig (plt.Figure): The figure object.
            ax (plt.Axes): The axes object.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Get the keys to plot. If none are specified, plot all of them
        if keys is None:
            eda_keys: List[str] = config.get("EDA", "eda_keys")
        else:
            eda_keys = keys

        self.standard_plot_routine(eda_keys, ax)

        # Since the same keys are plotted for all objects, we can just use the first object to get the labels
        labels = self.objects[0].get_plot_labels(eda_keys)

        # Set the key-specific plot details
        set_axes_details(ax=ax, x_label=self.plot_info.irc_coord_label, line_style_labels=labels, **kwargs)
        set_figure_details(fig=fig, title=f"EDA_{'_'.join(eda_keys)}", savefig=opj(self.path, f"EDA_{'_'.join(eda_keys)}.png"), **kwargs)
        return fig, ax

    @plot_logger()
    def plot_extra_strain(self, keys: Optional[List[str]] = None, **kwargs) -> Tuple[plt.Figure, plt.Axes]:
        """
        Plots the extra strain terms.

        This method plots the specified extra strain terms for each PyFragResultsObject in the plotter. If no terms are specified,
        all terms are plotted. The plot is saved to the plot directory with a filename that includes the plotted terms.

        Args:
            keys (Optional[List[str]], optional): The extra strain terms to plot. If None, all terms are plotted. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the `set_axes_details` and `set_figure_details` functions.

        Returns:
            fig (plt.Figure): The figure object.
            ax (plt.Axes): The axes object.

        Raises:
            ValueError: If any of the specified keys do not exist in the extra strain dictionary.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Get the keys to plot. If none are specified, plot all of them
        if keys is None:
            extra_strain_keys: List[str] = config.get("ASM", "asm_strain_keys")
        else:
            extra_strain_keys = keys

        self.standard_plot_routine(extra_strain_keys, ax)

        # Since the same keys are plotted for all objects, we can just use the first object to get the labels
        labels = self.objects[0].get_plot_labels(extra_strain_keys)

        # Set the key-specific plot details
        set_axes_details(ax=ax, x_label=self.plot_info.irc_coord_label, line_style_labels=labels, **kwargs)
        set_figure_details(fig=fig, title=f"Strain_{'_'.join(extra_strain_keys)}", savefig=opj(self.path, f"ASM_{'_'.join(extra_strain_keys)}.png"), **kwargs)
        return fig, ax

    # ------------------------------------------------------------------------------------------------------------- #
    # ------------------------------ Population and Orbital Energy plotting routines ------------------------------ #
    # ------------------------------------------------------------------------------------------------------------- #

    @plot_logger()
    def plot_population(self, keys: Optional[Tuple[List[str]]] = None):
        """Plots the population of the orbitals.

        Args:
            keys (Optional[Tuple[List[str]]], optional): The keys to plot. Defaults to None.

        Raises:
            NotImplementedError: This function is not implemented yet.

        """
        raise NotImplementedError("This function is not implemented yet")

        # Plots the keys by doing the folowwing: if no keys are specified, it plots all of them in pairs of two
        # Otherwise, it plots the specified keys in the format: [list_of_first_object[specified indices], list_of_second_object[specified indices], ...]

        # # Get the keys to plot. If none are specified, plot all of them in pairs of two
        # if keys is None:
        #     keys = [(self.objects[i].population.keys(), self.objects[i+1].population.keys()) for i in range(0, len(self.objects), 2)]
        # else:
        #     keys = [tuple(self.objects[i].population.keys() if j in indices else [] for i in range(len(self.objects))) for j, indices in enumerate(keys)]

        # # Plot the keys
        # for key_pair in keys:
        #     x_axes = [obj.get_x_axis(self.plot_info.irc_coord) for obj in self.objects]
        #     for i, (line_style, term) in enumerate(zip(self.plot_info.line_styles, key_pair)):
        #         for x_axis, colour, obj in zip(x_axes, self.plot_info.colours, self.objects):
        #             term_data = obj.population[term]
        #             # Plot the data
        #             if i == 0:
        #                 plt.plot(x_axis, term_data, label=obj.name, color=colour, linestyle=line_style)
        #             else:
        #                 plt.plot(x_axis, term_data, color=colour, linestyle=line_style)

        # # Set the plot details
        # set_plot_details(savefig=opj(self.path, "population.png"),
        #                 title="Population",
        #                 x_label=self.plot_info.irc_coord_label)

    @plot_logger()
    def plot_arbitrary_keys(self, title: str, keys: List[str], **kwargs) -> Tuple[plt.Figure, plt.Axes]:
        """
        Arbitrary plotting function for plotting any key (or a combination of) in the PyFragResultsObject object.

        This method plots the specified keys for each PyFragResultsObject in the plotter. The plot is saved to the plot directory
        with a filename that includes the plotted keys. The plot title and other figure and axes details can be customized.

        Args:
            title (str): The title of the plot.
            keys (List[str]): The keys to plot. These should match the keys in the corresponding dictionary type (asm, eda or extra_strain).
            **kwargs: Additional keyword arguments to pass to the `set_axes_details` and `set_figure_details` functions.

        Returns:
            fig (plt.Figure): The figure object.
            ax (plt.Axes): The axes object.

        Raises:
            ValueError: If any of the specified keys do not exist in the dictionaries of the PyFragResultsObject objects.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)

        self.standard_plot_routine(keys, ax)

        labels = self.objects[0].get_plot_labels(keys)

        # Set the key-specific plot details
        set_axes_details(ax=ax, x_label=self.plot_info.irc_coord_label, line_style_labels=labels, **kwargs)
        set_figure_details(fig=fig, title=title, savefig=opj(self.path, f"{'_'.join(keys)}.png"), **kwargs)
        return fig, ax
