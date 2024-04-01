import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from IPython.display import display, HTML


class VisLotan:
    @staticmethod
    def plt_plot(df, events, plot_by='index', figsize=(16, 10)):
        """
        Generates line plots for the specified events in the dataframe using matplotlib.

        Parameters:
        - df (DataFrame): The Pandas DataFrame containing the data.
        - events (list of list): A list of event group lists. Each event group will be plotted in a separate subplot.
        - plot_by (str): Column name to use for the x-axis. If 'index', the DataFrame's index will be used.
        - figsize (tuple): The size of the figure (width, height) in inches.

        Returns:
        None. Displays the plot inline.
        """
        fig, axs = plt.subplots(len(events), figsize=figsize)

        x = df.index if plot_by == 'index' else df[plot_by]

        for i, event_group in enumerate(events):
            for event in event_group:
                axs[i].plot(x, df[event], label=event)
                axs[i].legend(loc='lower right')

    @staticmethod
    def plotly_plot(df, events, plot_by='index', mode='lines', height=800, width=1600):
        """
        Generates interactive line plots for the specified events in the dataframe using Plotly.

        Parameters:
        - df (DataFrame): The Pandas DataFrame containing the data.
        - events (list of list): A list of event group lists. Each event group will be plotted in a separate subplot.
        - plot_by (str): Column name to use for the x-axis. If 'index', the DataFrame's index will be used.
        - mode (str): The drawing mode for the plot ('lines', 'markers', 'lines+markers', etc.).

        Returns:
        fig (Figure): A Plotly Figure object that can be displayed or further customized.
        """
        fig = make_subplots(rows=len(events), cols=1, shared_xaxes=True, vertical_spacing=0.05)

        x = df.index if plot_by == 'index' else df[plot_by]

        for i, event_group in enumerate(events):
            for event in event_group:
                fig.add_trace(
                    go.Scatter(
                        x=x, y=df[event], name=event, mode=mode,
                        marker=dict(size=6, line=dict(width=2))
                    ),
                    row=i + 1, col=1, secondary_y=False
                )

                # Annotation example, can be customized or removed
                fig.add_annotation(
                    text="text",
                    xref="paper", yref="paper",
                    x=1.2, y=0.6,
                    showarrow=False,
                    align='left'
                )

        fig.update_layout(showlegend=True, height=height, width=width)

        return fig

    @staticmethod
    def plotly_plot_2df(df1, df2, events, plot_by='index', label1='1st', label2='2nd',
                        mode1='lines', mode2= 'markers', title="", height=800, width=1600):
        """
        Generates interactive line plots for the specified events, comparing two dataframes using Plotly.

        Parameters:
        - df1, df2 (DataFrame): The Pandas DataFrames containing the data to compare.
        - events (list of list): A list of event group lists. Each event group will be plotted in a separate subplot.
        - plot_by (str): Column name to use for the x-axis. If 'index', the DataFrame's index will be used.
        - label1, label2 (str): Labels for the data series from df1 and df2 respectively.
        - title (str): The title of the plot.

        Returns:
        fig (Figure): A Plotly Figure object that can be displayed or further customized.
        """
        fig = make_subplots(rows=len(events), cols=1, shared_xaxes=True, vertical_spacing=0.05)

        x1 = df1.index if plot_by == 'index' else df1[plot_by]
        x2 = df2.index if plot_by == 'index' else df2[plot_by]

        for i, event_group in enumerate(events):
            for event in event_group:
                fig.add_trace(
                    go.Scatter(
                        x=x1, y=df1[event], name=f"{label1} {event}",
                        mode=mode1, marker=dict(size=6, line=dict(width=2))
                    ),
                    row=i + 1, col=1, secondary_y=False
                )
                fig.add_trace(
                    go.Scatter(
                        x=x2, y=df2[event], name=f"{label2} {event}",
                        mode=mode2, marker=dict(size=6, line=dict(width=2))
                    ),
                    row=i + 1, col=1, secondary_y=False
                )

                # Annotation example, can be customized or removed
                fig.add_annotation(
                    text="text",
                    xref="paper", yref="paper",
                    x=1.2, y=0.6,
                    showarrow=False,
                    align='left'
                )

        fig.update_layout(showlegend=True, height=height, width=width, title=title)

        return fig

    @staticmethod
    def set_width(size):
        """
        Sets the width of the Jupyter Notebook container and the maximum number of displayed rows.

        Parameters:
        - size (int): The desired width percentage of the container and the maximum number of rows to display.

        Returns:
        None. Adjusts the notebook display settings.
        """
        display(HTML(f"<style>.container {{ width:{size}% !important; }}</style>"))
        pd.set_option('display.max_rows', size)
