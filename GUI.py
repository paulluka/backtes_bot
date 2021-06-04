import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


vert = '#599673'
rouge = '#e95142'

def couleur(df):
    if df['Close'].iloc[-2]-df['Close'].iloc[-1] < 0 :
        return vert
    else : return rouge


def gui(df, name, fenetre):

	buy_df = df[df["signal"] == 1]
	sell_df = df[df["signal"] == -1]
		#Indicateurd à afficher
	m_a_5d = st.checkbox('Moyenne mobile 5 jours')
	m_a_9d = st.checkbox('Moyenne mobile 9 jours')

	fig = make_subplots(rows=1, cols=2,
	                    specs=[[{'type': 'xy'},{'type':'indicator'}]],
	                    column_widths=[0.85, 0.05],
	                    shared_xaxes=True,
	                    subplot_titles=[name, ''])


	# courbes #####################
	fig.add_trace(go.Scatter(
	    y = df['Close'],
	    x = df['Date'],
	    line=dict(color="grey", width=1),
	    name="",
	    hovertemplate=
	    "Date: %{x}<br>" +
	    "Close: %{y}<br>"+
	    "Volume: %{text}<br>",
	    text = df.Volume,
	), row=1, col=1)


	# Tracer les moyennes mobiles
	if m_a_5d:
	  fig.add_trace(go.Scatter(
	      y = df["m_a_5d"],
	      x = df['Date'],
	      line=dict(color="blue", width=1),
	      name="",
	  ), row=1, col=1)

	if m_a_9d:
	  fig.add_trace(go.Scatter(
	      y = df["m_a_9d"],
	      x = df['Date'],
	      line=dict(color="purple", width=1),
	      name="",
	  ), row=1, col=1)


	fig.add_trace(go.Scatter(
	      y = buy_df["Close"],
	      x = buy_df['Date'],
	      line=dict(color="purple", width=1),
	      name="Buy",
	  ), row=1, col=1)

	fig.add_trace(go.Scatter(
	      y = sell_df["Close"],
	      x = sell_df['Date'],
	      line=dict(color="red", width=1),
	      name="Sell",
	  ), row=1, col=1)

	fig.add_hline(y=df['Close'].iloc[0],
	              line_dash="dot",
	              annotation_text="{}".format(df['Date'][0].date()),
	              annotation_position="bottom left",
	              line_width=2, line=dict(color='black'),
	              annotation=dict(font_size=10),
	              row=1, col=1)


	# Indicateurs #####################

	fig.add_trace(go.Indicator(
	    mode = "number+delta",
	    value = round(df['Close'].iloc[-1],4),
	    number={'prefix': "$", 'font_size' : 40},
	    delta = {"reference": df['Close'].iloc[-1*fenetre], "valueformat": ".6f", "position" : "bottom", "relative":False},
	    title = {"text": name+" Since {}-days".format(fenetre)},
	    domain = {'y': [0.5, 0.7], 'x': [0.55, 0.75]}),
	row=1, col=2)


	# layout #############

	fig.update_layout(
	    template='simple_white',
	    showlegend=False,
	    font=dict(size=10),
	    autosize=False,
	    width=1400, height=300,
	    margin=dict(l=40, r=500, b=40, t=40),
	    paper_bgcolor='rgba(0,0,0,0)',
	    plot_bgcolor='rgba(0,0,0,0)',
	    xaxis_showticklabels=True,
	)

	st.plotly_chart(fig)

	return fig

