from flask import Flask, render_template, request,flash, redirect, session, abort
from flask_bootstrap import Bootstrap
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime, timedelta
import time
import calendar,math
import os
import requests



flag = False
message=""
app = Flask(__name__);
Bootstrap(app)

@app.route("/")
def home():
    return render_template("home.html", **locals())

def getStocksData(strategy_name, investment_per_strategy, stock_symbol_array, stock_symbol_set):
    stock_details = []
    five_days_history = []
    investment_per_company = investment_per_strategy / 3

    for stock_symbol in stock_symbol_array:

        ts = TimeSeries(key='L7LPZFOTDXED8KS0')
        data, meta_data = ts.get_daily_adjusted(stock_symbol)

        if meta_data:

            count = 0
            for each_entry in data:
                thisweek = datetime.today() - timedelta(days=8)
                if (each_entry > thisweek.strftime('%Y-%m-%d')):
                    if count < 5:
                        stock_details.append(
                            [strategy_name, stock_symbol, each_entry, data[each_entry]['5. adjusted close']])
                        five_days_history.append(each_entry)
                        count = count + 1
                    else:
                        break


    first_day = []
    first_day_history = []
    second_day_history = []
    third_day_history = []
    fourth_day_history = []
    fifth_day_history = []

    first_day_investment = 0
    second_day_investment = 0
    third_day_investment = 0
    forth_day_investment = 0
    fifth_day_investment = 0
    graph_results = []
    graph_results_detailed = []

    print(stock_details)
    for entry in stock_details:
        if entry[2] == sorted(set(five_days_history))[0]:
            first_day.append([entry[1], entry[3]])
            #no_of_stocks_per_company = math.floor(investment_per_company / float(entry[3]))
            no_of_stocks_per_company = math.floor((stock_symbol_set.get(entry[0]).get(entry[1]) * investment_per_strategy/float(100))/ float(entry[3]))
            first_day_history.append([entry[1], round(float(entry[3]), 2), no_of_stocks_per_company])
            first_day_investment += no_of_stocks_per_company * float(entry[3])

    graph_results.append([sorted(set(five_days_history))[0], round(first_day_investment, 2)])

    for entry in stock_details:

        if entry[2] == sorted(set(five_days_history))[1]:
            for company in first_day_history:
                if company[0] == entry[1]:
                    second_day_history.append([entry[1], round(float(entry[3]), 2), company[2]])
                    second_day_investment += (float(entry[3]) * company[2])

        elif entry[2] == sorted(set(five_days_history))[2]:
            for company in first_day_history:
                if company[0] == entry[1]:
                    third_day_history.append([entry[1], round(float(entry[3]), 2), company[2]])
                    third_day_investment += (float(entry[3]) * company[2])

        elif entry[2] == sorted(set(five_days_history))[3]:
            for company in first_day_history:
                if company[0] == entry[1]:
                    fourth_day_history.append([entry[1], round(float(entry[3]), 2), company[2]])
                    forth_day_investment += (float(entry[3]) * company[2])

        elif entry[2] == sorted(set(five_days_history))[4]:
            for company in first_day_history:
                if company[0] == entry[1]:
                    fifth_day_history.append([entry[1], round(float(entry[3]), 2), company[2]])
                    fifth_day_investment += (float(entry[3]) * company[2])

    graph_results.append([sorted(set(five_days_history))[1], round(second_day_investment, 2)])
    graph_results.append([sorted(set(five_days_history))[2], round(third_day_investment, 2)])
    graph_results.append([sorted(set(five_days_history))[3], round(forth_day_investment, 2)])
    graph_results.append([sorted(set(five_days_history))[4], round(fifth_day_investment, 2)])

    graph_results_detailed.append([sorted(set(five_days_history))[0], first_day_history])
    graph_results_detailed.append([sorted(set(five_days_history))[1], second_day_history])
    graph_results_detailed.append([sorted(set(five_days_history))[2], third_day_history])
    graph_results_detailed.append([sorted(set(five_days_history))[3], fourth_day_history])
    graph_results_detailed.append([sorted(set(five_days_history))[4], fifth_day_history])

    return graph_results, graph_results_detailed


@app.route('/stockportfolio', methods=['POST'])
def getSuggestion():
    amount = request.form['investment_value']
    strategies = request.form.getlist('strategy')
    if len(strategies) == 2:
        amount_per = int(amount) / 1
    elif len(strategies) == 1:
        amount_per = int(amount)

    print("Input Investment Value", amount)
    print("Input Investment Strategies", strategies)

    e_stock_set = {
        "AAPL": 30,
        "ADBE": 30,
        "NSRGY": 40
    }
    g_stock_set = {
        "VRTX":30,
        "T":30,
        "CMCSA":40
    }

    i_stock_set = {
        "VTI": 30,
        "IXUS": 30,
        "ILTB":40
    }

    q_stock_set = {
        "BAC":30,
        "HD":30,
        "KRMD":40
    }
    v_stock_set = {
        "ADVM":30,
        "ARWR":30,
        "MDCO":40
    }

    stock_set = {
        "Growth Investing" : e_stock_set,
        "Ethical Investing" : e_stock_set,
        "Index Investing" : i_stock_set,
        "Quality Investing": q_stock_set,
        "Value Investing" : v_stock_set
    }

    try:

        totalresults = []
        totalmoreresults = []

        for strategy in strategies:

            if strategy == 'Ethical Investing':
                print("Ethical Investing:")
                graph_results, graph_results_detailed = getStocksData(strategy, amount_per, e_stock_set, stock_set)

                totalresults.append([strategy, graph_results])
                totalmoreresults.append([strategy, graph_results_detailed])

                print("Graph Result : ", totalresults)
                print("Detailed Graph Result : ", totalmoreresults)
                print("")

            elif strategy == 'Growth Investing':
                print("Growth Investing:")
                # Wait for 1 minute before making the API Call
                time.sleep(60)
                graph_results, graph_results_detailed = getStocksData(strategy, amount_per, g_stock_set, stock_set)

                totalresults.append([strategy, graph_results])
                totalmoreresults.append([strategy, graph_results_detailed])

                print("Graph Result : ", totalresults)
                print("Detailed Graph Result : ", totalmoreresults)
                print("")

            elif strategy == 'Index Investing':
                print("Index Investing:")
                # Wait for 1 minute before making the API Call
                time.sleep(60)
                graph_results, graph_results_detailed = getStocksData(strategy, amount_per, i_stock_set, stock_set)

                totalresults.append([strategy, graph_results])
                totalmoreresults.append([strategy, graph_results_detailed])

                print("Graph Result : ", totalresults)
                print("Detailed Graph Result : ", totalmoreresults)
                print("")

            elif strategy == 'Quality Investing':
                print("Quality Investing:")
                # Wait for 1 minute before making the API Call
                time.sleep(60)
                graph_results, graph_results_detailed = getStocksData(strategy, amount_per, q_stock_set, stock_set)

                totalresults.append([strategy, graph_results])
                totalmoreresults.append([strategy, graph_results_detailed])

                print("Graph Result : ", totalresults)
                print("Detailed Graph Result : ", totalmoreresults)
                print("")

            elif strategy == 'Value Investing':
                print("Value Investing:")
                # Wait for 1 minute before making the API Call
                time.sleep(60)
                graph_results, graph_results_detailed = getStocksData(strategy, amount_per, v_stock_set, stock_set)

                totalresults.append([strategy, graph_results])
                totalmoreresults.append([strategy, graph_results_detailed])

                print("Graph Result : ", totalresults)
                print("Detailed Graph Result : ", totalmoreresults)
                print("")

        print("Graph Result Length : ", len(totalresults))
        print("Detailed Graph Result Length : ", len(totalmoreresults))

        if len(totalresults) == 1 and len(totalmoreresults) == 1:
            return render_template("Portfolio_One Strategy.html", fgr=totalresults, pgrd=totalmoreresults)

        elif len(totalresults) == 2 and len(totalmoreresults) == 2:
            return render_template("Portfolio_Two Strategies.html", fgr=totalresults, pgrd=totalmoreresults)
        else:
            print("Strategy selected Error")

    except ValueError:
        print('Stock Symbol NOT found')

    except requests.ConnectionError:
        print('Network connection lost. Please try again later')

if __name__=='__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=3000)
