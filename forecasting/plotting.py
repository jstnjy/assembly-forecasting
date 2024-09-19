import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional
import plotly.express as px


def datetime_line_plot(data: pd.DataFrame,
                       column_name: str,
                       freq: Optional[str] = None,
                       agg_operation: str = 'mean',
                       *,
                       plot_title_name="",
                       plot_xlabel_name="",
                       plot_ylabel_name="",
                       make_interactive=False) -> None | bool:
    """
        A convenient function that creates a lineplot if an index is a DateTime
        for numerical column only
    """

    if freq is None:
        if make_interactive:
            fig = px.line(data, x=data.index, y=column_name,
                          title=plot_title_name, labels={data.index.name: plot_ylabel_name,
                                                         column_name: plot_xlabel_name}
                          )
            fig.show()
        else:
            data[column_name].plot()
            plt.title(plot_title_name)
            plt.xlabel(plot_xlabel_name)
            plt.ylabel(plot_ylabel_name)
            plt.show()
        return

    resampled_data = data.resample(freq).agg({column_name: agg_operation})

    if make_interactive:
        fig = px.line(resampled_data, x=resampled_data.index, y=column_name,
                      title=plot_title_name, labels={data.index.name: plot_xlabel_name,
                                                     column_name: plot_ylabel_name}

                      )
        fig.show()

    else:
        resampled_data[column_name].plot()
        plt.title(plot_title_name)
        plt.xlabel(plot_xlabel_name)
        plt.ylabel(plot_ylabel_name)
        plt.show()


def count_comparison_bar_plot(df1: pd.DataFrame,
                              df2: pd.DataFrame,
                              *,
                              make_ratio: bool = False,
                              num_to_compare: int = 10,
                              column_name: str,
                              df1_name: str = "",
                              df2_name: str = "",
                              plot_title_name: str = "",
                              plot_xlabel_name: str = "",
                              plot_ylabel_name: str = "") -> None:
    """
        A bar plot that ranks and comparese the count of two different columns
        with similar length and name
    """

    # create a new df that ranks the df1 and df2
    compare_df = pd.concat([
        df1[column_name].value_counts(normalize=make_ratio).head(
            num_to_compare).to_frame().reset_index().assign(day=df1_name),
        df2[column_name].value_counts(normalize=make_ratio).head(
            num_to_compare).to_frame().reset_index().assign(day=df2_name)
    ])

    if make_ratio:
        orig_y_name = 'proportion'
    else:
        orig_y_name = 'count'

    # plot the compare_df
    fig = px.bar(compare_df, x=compare_df.index + 1, y=orig_y_name, color='day',
                 barmode='group', hover_data=column_name, text=column_name,
                 title=plot_title_name,
                 labels={orig_y_name: plot_ylabel_name,
                         'x': plot_xlabel_name},
                 )

    # show all rank values
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            tick0=1,
            dtick=1
        )
    )
    fig.show()


def comparison_line_plot(df1: pd.DataFrame,
                         df2: pd.DataFrame,
                         *,
                         column_name: str,
                         df1_name: str = "",
                         df2_name: str = "",
                         plot_title_name: str = "",
                         plot_xlabel_name: str = "",
                         plot_ylabel_name: str = "") -> None:
    """
        A line plot that plots two line plots for comparison
    """

    # create a new df that ranks the df1 and df2
    compare_df = pd.concat([
        df1.assign(indicator=df1_name),
        df2.assign(indicator=df2_name)
    ])

    # plot the compare_df
    fig = px.line(compare_df, x=compare_df.index, y="forecast", color='indicator',
                  hover_data=column_name,
                  title=plot_title_name,
                  labels={"forecast": plot_ylabel_name,
                          'x': plot_xlabel_name},
                  )

    fig.show()
