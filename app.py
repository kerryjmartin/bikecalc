import os
import pandas as pandas
import plotly.express as px
import numpy as np
import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import math
import sympy
import mpmath
import dash_daq as daq

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[external_stylesheets])

def calc(weight, bike , acc , vo2max, threshold, economy, position, crr, grade, wind, alt, temp):
    weight = float(weight)
    bike = float(bike)
    acc = float(acc)
    temp = float(temp)
    alt = float(alt)
    vo2max = float(vo2max)
    threshold = float(threshold)
    position = float(position)
    economy = float(economy)
    crr = float(crr)
    grade = float(grade)
    wind = float(wind)
    mass = (weight+bike+acc)/2.2
    watts = round((vo2max*(weight/2.2))*(threshold/100)*(economy/60),2)
    rho = 1.2754*(373/((temp-32)*5/9+273.15))*np.exp(-1.2754*9.8070*alt*.3048/100000)
    B = mpmath.atan(grade/100)
    Crv = .1
    Crvn = Crv*(math.cos(B))
    Cm = .97
    Frg = 9.8072*(mass)*((crr*(math.cos(B)))+(math.sin(B)))
    cda = position
    W = wind*1609.344/3600
    A1 = (W**3+Crvn**3)/27
    A2 = W*(5*W*Crvn+(8+Crvn**2)/(cda*rho)+6*Frg)/(9*cda*rho)                
    A3 = (2*Frg*Crvn)/(3*((cda*rho)**2))
    A4 = watts/(Cm*cda*rho)
    A = A1 - A2 + A3 + A4
    X = (((2)/(9*cda*rho))*((3*Frg)-(4*W*Crvn)-((W**2)*cda*(rho/2))-((2*Crvn)/(cda*rho))))
    C = A**2 + X**3
    if C >= 0: 
        V1 = (A+(A**2+X**3)**(1/2))**(1/3)
        V2 = np.cbrt(A-(((A**2)+(X**3))**(1.0/2.0)))
        V3 = (2/3)*(W+((Crvn)/(cda*rho)))
        V = V1+V2-V3
    else : 
        V = (2*(-X)**(1/2))*math.cos((1/3)*math.acos((A)/(((-X)**3)**1/2)))-(2/3)*((W)+((Crvn)/(cda*rho)))
    speed = round(V*3600/1609.344, 2)
    return speed, watts

colors = {
    'background': '#090802',
    'text': '#BDB477'
}

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div(children = [
                html.Div(children = [
                    html.Div(children = [
                                html.H1('Bicycle Speed Calculator', style = {'color': colors['text'], 'text-align': 'center'}),
                                html.H5('This calculator is designed to be a demonstration of how VO2max, threshold, and cycling economy all affect cycling performance in steady-state/time trial-like efforts.', style = {'color':colors['text'], 'text-align':'center'}),
                                html.H5('More features are coming down the line and feature requests should be sent to: physiologydesign@gmail.com.', style = {'color':colors['text'], 'text-align':'center'})
                    ], className = 'row'),
                    html.Div(children =[
                        html.H5('Body Weight (lbs)', style = {'color': colors['text']}),
                        dcc.Input(id = 'weight', placeholder = 140, type = 'number', value = 140, style = {'textAlign': 'center'}),
                        html.H5('Bike Weight (lbs)', style = {'color': colors['text']}),
                        dcc.Input(id = 'bike', placeholder = 70, type = 'number',value = 16, style = {'textAlign': 'center'}),
                        html.H5('Accessories Weight (lbs)', style = {'color': colors['text']}),
                        dcc.Input(id = 'acc', placeholder = 3, type = 'number', value = 3, style = {'textAlign': 'center'}),
                        html.Br(),
                        html.H5('VO2max (ml/kg/min)', style = {'color': colors['text']}),
                        daq.Slider(id = 'vo2max', min = 0, max = 100, step = 1, value = 55, marks={
                                                30: {'label': 'Sedentary', 'style': {'color': '#bdb477'}},
                                                50: {'label': 'Fit', 'style': {'color':'#bdb477'}},
                                                70: {'label': 'Elite', 'style': {'color':'#bdb477'}},
                                                90: {'label': 'Olympian', 'style': {'color': '#bdb477'}}
                                                },updatemode='drag',handleLabel={"showCurrentValue": True,"label": "ml/kg/min",'color':'#bdb477'}),
                        html.Br(),
                        html.H5('Threshold (%)', style = {'color': colors['text']}),
                        daq.Slider(id = 'threshold', min = 50, max = 100, step = 1, value = 75, marks={
                                                65: {'label': 'Low', 'style': {'color': '#bdb477'}},
                                                75: {'label': 'Mod', 'style': {'color':'#bdb477'}},
                                                85: {'label': 'High', 'style': {'color':'#bdb477'}},
                                                },updatemode='drag',handleLabel={"showCurrentValue": True,"label": "Percent",'color':'#bdb477'}),
                        html.Br(),
                        html.H5('Cycling Economy (kj/L)', style = {'color': colors['text']}),
                        daq.Slider(id = 'economy', min = 3, max = 6, step = 0.1, value = 4.8, marks={
                                                3.5: {'label': 'Untrained', 'style': {'color': '#bdb477'}},
                                                4.5: {'label': 'Trained', 'style': {'color':'#bdb477'}},
                                                5.5: {'label': 'Exceptional', 'style': {'color':'#bdb477'}},
                                                },updatemode='drag',handleLabel={"showCurrentValue": True,"label": "kJ/L",'color':'#bdb477'}
                                    ),                                                
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.H5('Riding Position', style = {'color': colors['text']}),
                        dcc.Dropdown(id = 'position', options = [
                            {'label':'TT - Optimized', 'value':0.2},
                            {'label':'TT - Average', 'value':0.24},
                            {'label':'Drops', 'value':0.28},
                            {'label':'Hoods', 'value':0.3}
                            ],
                            value = .2,
                            style = {'textAlign': 'center','width': '50%'}),
                        html.H5('Tires', style = {'color': colors['text']}),
                        dcc.Dropdown(id = 'crr', options = [
                            {'label':'Tubular', 'value':.002},
                            {'label':'Tubeless - Low RR', 'value':.0022},
                            {'label':'Tubeless - Regular', 'value':.0028},
                            {'label':'Clincher - Low RR', 'value':.003},
                            {'label':'Clincher - Regular', 'value':.0034}
                            ],
                            value = .002, style = {'textAlign': 'center', 'width': '50%'}),
                        html.H5('Grade (%)', style = {'color': colors['text']}),
                        dcc.Input(id = 'grade', placeholder = 0, type = 'number', value = 0, style = {'textAlign': 'center'}),
                        html.H5('Wind (mph)', style = {'color': colors['text']}),
                        dcc.Input(id = 'wind', placeholder = 0, type = 'number', value = 0, style = {'textAlign': 'center'}),
                        html.H5('Altitude (ft)', style = {'color': colors['text']}),
                        dcc.Input(id = 'alt', placeholder = 0, type = 'number', value = 0, style = {'textAlign': 'center'}),
                        html.H5('Temperature (F)', style = {'color': colors['text']}),
                        dcc.Input(id = 'temp', placeholder = 75, type = 'number', value = 75, style = {'textAlign': 'center'}),
                        html.H2(id = 'power', style = {'color': colors['text']}),
                        html.H2(id='speed', style = {'color': colors['text']}),
                        html.Br(),
                        html.Br()  
                ], style = {'columnCount': 2}, className = 'row')
            ], style = {'backgroundColor':'#090802'})]
            )
                

@app.callback(
        Output('speed', 'children'),
        Output('power', 'children'),
        Input('weight', 'value'),
        Input('bike', 'value'),
        Input('acc', 'value'),
        Input('vo2max', 'value'),
        Input('threshold', 'value'),
        Input('economy', 'value'),
        Input('position', 'value'),
        Input('crr', 'value'),
        Input('grade', 'value'),
        Input('wind', 'value'),
        Input('alt', 'value'),
        Input('temp', 'value')
)

def callback_pred(weight, bike , acc , vo2max, threshold, economy, position, crr, grade, wind, alt, temp):
    pred = calc(weight = weight,
                bike = bike, 
                acc = acc, 
                vo2max = vo2max, 
                threshold = threshold, 
                economy = economy, 
                position = position, 
                crr = crr, 
                grade = grade, 
                wind = wind, 
                alt = alt, 
                temp = temp)
    return 'Power: {} Watts'.format(pred[1]),'Speed: {} mph'.format(pred[0])

if __name__ == '__main__':
    app.run_server(debug=False)

