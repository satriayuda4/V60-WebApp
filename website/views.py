from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json

views = Blueprint('views', __name__)


@views.route('/', methods = ['GET', 'POST'])
def Coffee():
    if request.method == 'POST':
        weight = request.form.get('formGroupWeightInput',type=int)
        water = request.form.get('formGroupWaterInput',type=int)
        pour = request.form.get('formGroupPourInput',type=int)
        weight = int(weight)
        water = int(water)
        total_water = weight*water
        water_pour = total_water/pour

        container = 0
        weight_list = []
        for i in range(pour):
            container += water_pour
            weight_list.append(container)
    else :
        return render_template("home.html")    
    
    return render_template("home.html", pouring = weight_list)


@views.route('/')
def sample_view():
    data = [
        [
            'Frutta', 
            ['M01', '2018-08-06 08:35:00', '2018-08-06 10:13:00'], 
            ['M02', '2018-08-06 10:18:00', '2018-08-06 11:42:00'],
            ['M04', '2018-08-06 15:19:00', '2018-08-06 16:37:00']
         ], 
        ['verdura', ['M01', '2018-08-06 08:35:00', '2018-08-06 10:25:00']]
    ]

    return render_template("home.html", data=data)
