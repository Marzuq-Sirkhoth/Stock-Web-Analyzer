from flask import Flask, render_template,request, session
from API_STATS_CLASS import AccessAPI
import matplotlib.pyplot as plt #pyplot module
import mpld3
from datetime import datetime

#Flask is a class
#session allows access to data across various requests, store in dictionary 
#request in an instance of the Request class in flask, handles HTTP requests)
#render_template, function to access HTML files
                                                                                                    #in my 'Web App' folder
myApp = Flask(__name__,template_folder='templates')
myApp.secret_key = 'apply_selfMINDforXtradeBONUSBLOOD173566'

@myApp.route('/')
def getHTML():
    return render_template('index.html')    #creates the first html web page, index.2

@myApp.route("/ops", methods=["POST"])  #post
def displayOps():
    session['link']=request.form.get("url")
    return render_template('displayOps.html')

@myApp.route('/DataFrame', methods=['GET','POST'])   #function associated with 'display' route #Post requests 
def displayDataFrame():
    link = session['link']
    df = AccessAPI.accessStockData(link) #url--> name="url" in, <input type="text" id="url" name="url">
    session['df'] = df.to_dict(orient='split')  #can't store DataFrame, can store dictionary
    return render_template('dataFrame.html', html_df = df.to_html()) #pandas function which converts data structure to html

@myApp.route("/stats", methods=['Get', 'POST']) #get: data from.... post: data to
def displayStats():
    keys = ['1. open', '2. high', '3. low', '4. close']
    link = session['link']
    df = AccessAPI.accessStockData(link)
    list_of_means = AccessAPI.getMean(df)    #static, no instance needed
    list_of_medians = AccessAPI.getMedian(df) #static, no instance needed
    #list_of_modes = AccessAPI.getMode(df) #static, no instance needed
    list_of_var = AccessAPI.calc_Volatility(df) #static, no instance needed
    
    return render_template('stats_Display.html', keys_array=keys, means=list_of_means, medians=list_of_medians, vars=list_of_var)
    
@myApp.route('/graph', methods=['POST'])
def graph_data():
    link = session['link']
    df = AccessAPI.accessStockData(link)
    dictionary = df.to_dict(orient='index') #pandas function, DataFrame function
                                            #the keys are the indices, not the columns
    #list_of_dates = list(dictionary.keys())   #the keys are the dates(index)
                                              #keys() function, each key
    
    list_of_dates = [datetime.strptime(date, "%Y-%m-%d") for date in dictionary.keys()]
    list_of_openingPrices = [entry["1. open"] for entry in dictionary.values()]
    list_of_highPrices = [entry["2. high"] for entry in dictionary.values()]
    list_of_lowPrices = [entry["3. low"] for entry in dictionary.values()]
    list_of_closingPrices = [entry["4. close"] for entry in dictionary.values()] #each value of key[4. close]

    figure1,ax1 = plt.subplots()  #returns two variables, a figure and axis
    figure2,ax2 = plt.subplots()
    figure3,ax3 = plt.subplots()
    figure4,ax4 = plt.subplots()

    ax1.plot(list_of_dates,list_of_openingPrices,marker='o', linestyle='-', color='blue', label='OPENING PRICES')
    ax2.plot(list_of_dates,list_of_highPrices, marker='^', linestyle='-', color='red', label='HIGH PRICES')
    ax3.plot(list_of_dates, list_of_lowPrices, marker='s', linestyle='-', color='green', label='LOW PRICES')
    ax4.plot(list_of_dates, list_of_closingPrices, marker='v', linestyle='-', color='purple', label='CLOSING PRICES' )
    
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Prices')
    ax1.set_title('Opening prices VS Time')

    ax2.set_xlabel('Dates')
    ax2.set_ylabel('Prices')
    ax2.set_title('High prices VS Time')

    ax3.set_xlabel('Dates')
    ax3.set_ylabel('Prices')
    ax3.set_title('Low prices VS Time')

    ax4.set_xlabel('Dates')
    ax4.set_ylabel('Prices')
    ax4.set_title('Closing prices VS Time')

    html_o = mpld3.fig_to_html(figure1)
    html_h = mpld3.fig_to_html(figure2)
    html_l = mpld3.fig_to_html(figure3)
    html_c = mpld3.fig_to_html(figure4)

    content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <title>GRAPH</title>
    </head>
    <body>
    <h2>GRAPH</h2>
    {html_o} {html_h}
    {html_l} {html_c}
    </body>
    </html>
    """
    return content #similar to return render_template(file)

if __name__ == '__main__':
    myApp.run(debug=True)