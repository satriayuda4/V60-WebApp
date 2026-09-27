from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def Coffee():
    if request.method == 'POST':
        raw_weight = request.form.get('formGroupWeightInput', '')
        raw_water = request.form.get('formGroupWaterInput', '')
        raw_pour = request.form.get('formGroupPourInput', '')

        form_data = {
            'weight': raw_weight,
            'water': raw_water,
            'pour': raw_pour
        }

        try:
            weight = float(raw_weight)
            water = float(raw_water)
            pour = int(raw_pour)
            if weight <= 0 or water <= 0 or pour <= 0:
                raise ValueError("Values must be positive numbers.")
        except (ValueError, TypeError):
            flash("Please enter valid positive numbers for all brewing inputs.", category="error")
            return render_template("home.html", form_data=form_data)

        total_water = round(weight * water, 1)
        base_water_pour = round(total_water / pour, 1)

        pouring_steps = []
        cumulative = 0.0
        for i in range(1, pour + 1):
            if i == pour:
                incremental = round(total_water - cumulative, 1)
            else:
                incremental = base_water_pour
            cumulative = round(cumulative + incremental, 1)
            pouring_steps.append({
                'step': i,
                'is_bloom': (i == 1),
                'incremental': int(incremental) if incremental.is_integer() else incremental,
                'target_weight': int(cumulative) if cumulative.is_integer() else cumulative
            })

        legacy_pouring = [step['target_weight'] for step in pouring_steps]

        summary = {
            'coffee_weight': int(weight) if weight.is_integer() else weight,
            'water_ratio': int(water) if water.is_integer() else water,
            'total_water': int(total_water) if total_water.is_integer() else total_water,
            'pour_count': pour,
            'water_pour': int(base_water_pour) if base_water_pour.is_integer() else base_water_pour,
        }

        return render_template(
            "home.html",
            pouring=legacy_pouring,
            pouring_steps=pouring_steps,
            summary=summary,
            form_data=form_data
        )

    return render_template("home.html", form_data={})


@views.route('/sample')
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
