from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/chart')
def chart():
	from pandas_datareader import data
	import pandas as pd
	import datetime
	from bokeh.plotting import figure, show, output_file
	from bokeh.models.annotations import Title
	from bokeh.embed import components
	from bokeh.resources import CDN

	start_time = datetime.datetime(2017,1,1)
	end_time = datetime.datetime(2018,3,10)

	df = data.DataReader(name="BTC-USD", data_source="yahoo",start=start_time,end=end_time)

	def inc_dec(c,o):
	    if c-o > 0:
	        value="Increase"
	    elif c-o < 0:
	        value ="Decrease"
	    else:
	        value = "Equal"
	    return value

	df['Status'] = [inc_dec(c,o) for c,o in zip(df.Close, df.Open)]

	df['Middle'] = (df.Open + df.Close)/2

	df['Height'] = abs(df.Open - df.Close)


	df

	#rect methods

	p = figure(x_axis_type='datetime',width=1000, height=300, sizing_mode = "scale_width")
	t = Title()
	t.text= "Candlestick"
	p.title = t
	p.grid.grid_line_alpha=0.5

	hours_12=12*60*60*1000

	p.segment(df.index, df.High, df.index, df.Low, color="black")

	p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
	       hours_12, df.Height[df.Status == "Increase"], fill_color="#6495ED")

	p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"],
	       hours_12, df.Height[df.Status == "Decrease"], fill_color="#FF0000")

	script, div1 = components(p)
	cdn_js=CDN.js_files[0]
	cdn_css=CDN.css_files

	#output_file("CS.html")

	#show(p)
	return render_template("chart.html", webapp=script,
		div1=div1, cdn_js=cdn_js)


@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
