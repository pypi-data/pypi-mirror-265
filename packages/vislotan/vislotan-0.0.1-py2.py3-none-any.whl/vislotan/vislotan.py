import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

class VisLotan:
    def plt_plot(self, df, events, plot_by='index', figsize=(16, 10)):
        fig, axs = plt.subplots(len(events),figsize=figsize)
        
        if plot_by=='index':
            x=df.index
        else:
            x=df[plot_by]
        
        for i, event_group in enumerate(events):
            for event in event_group:
                axs[i].plot(x, df[event], label=event)
                #axs[i].set_title(event)
                #axs[i].legend()
                axs[i].legend(loc='lower right')
                
    def plotly_plot(self, df, events, plot_by='index', mode='lines'):
        fig = make_subplots(rows=len(events), cols=1, shared_xaxes=True, vertical_spacing=0.05)

        if plot_by=='index':
            x=df.index
        else:
            x=df[plot_by]
        
        for i, event_group in enumerate(events):
            for event in event_group:
                fig.add_trace(go.Scatter(x=x, y=df[event], name=event,
                                    mode=mode,#'lines+markers',
                        marker=dict( size=6,line=dict(width=2))),
                                                            row=i+1, col=1, secondary_y=False ,)
    #                        color='rgba(135, 206, 250, 0.05)',
                                                            
                            
            
                fig.add_annotation(
                        text="text",
                        xref="paper", yref="paper",
                        x=1.2, y=0.6,
                        showarrow=False,
                        align='left',
                    )

        fig.update_layout(showlegend=True, height=800, width=1600)
        
        return fig
                                                            
                
    def plotly_plot_2df(self, df1, df2, events, plot_by='index',label1='1st', label2='2nd', title=""):
        fig = make_subplots(rows=len(events), cols=1, shared_xaxes=True, vertical_spacing=0.05)

        if plot_by=='index':
            x1=df1.index
            x2=df2.index
        else:
            x1=df1[plot_by]
            x2=df2[plot_by]
        
        for i, event_group in enumerate(events):
            for event in event_group:
                fig.add_trace(go.Scatter(x=x1, y=df1[event], name=f"{label1} {event}",
                                    mode='lines',#'lines+markers',
                        marker=dict( size=6,line=dict(width=2))),
                                                            row=i+1, col=1, secondary_y=False ,)
                fig.add_trace(go.Scatter(x=x2, y=df2[event], name=f"{label2} {event}",
                                    mode='markers',#'lines+markers',
                        marker=dict( size=6,line=dict(width=2))),
                                                            row=i+1, col=1, secondary_y=False ,)
    #                        color='rgba(135, 206, 250, 0.05)',
                                                            
                            
            
                fig.add_annotation(
                        text="text",
                        xref="paper", yref="paper",
                        x=1.2, y=0.6,
                        showarrow=False,
                        align='left',
                    )

        fig.update_layout(showlegend=True, height=800, width=1600, title=title)
        
        return fig
                                                            
                                                            
