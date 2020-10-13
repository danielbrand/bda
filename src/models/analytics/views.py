from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.analytics.analytics import Dataset
import pandas as pd

analytics_blueprint = Blueprint('analytics', __name__)


@analytics_blueprint.route('/data_input')
def data_input():
    return render_template('analytics/import_data.html')


@analytics_blueprint.route('import_data', methods=['GET', 'POST'])
def data_overview():
    dataset = request.files['data']
    user_email = session['email']
    Dataset.save_data(dataset=dataset, user_email=user_email)
    overview_list = Dataset.retrieve_data()

    return render_template('analytics/data_overview.html', overview_list=overview_list)


#@analytics_blueprint.route('import_data', methods=['GET', 'POST'])
#def import_data():
    #dataset = request.files['data']
    #Dataset.save_data(dataset=dataset)
    #sources = Dataset.all()
    #return render_template('analytics/statistics.html', sources=sources)


#@analytics_blueprint.route('/analytics_results', methods=['GET', 'POST'])
#def show_results():
 #   if request.method == 'POST':
  #      dataset = request.files['data']
   #     return Dataset.prediction_score(dataset)
    #else:
    #    return "Fail"


