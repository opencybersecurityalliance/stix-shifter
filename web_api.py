from flask import Flask, request, render_template, jsonify
from stix_shifter.stix_translation.src.patterns.translator import translate, SearchPlatforms, DataModels

# EXAMPLE Usage - accepts a STIX2 string as input via POST:
#    curl -X POST
#         -H "Content-Type:text/plain"
#         -d "[process:pid <= 5]"
#         http://127.0.0.1:5000/car-elastic

""" TODO: return the results in JSON.
    catch errors and render them in JSON back to requestor."""

app = Flask(__name__.split('.')[0])


def run_server():  # used only by test module to start dev server
    app.run(debug=True, port=5000, host='127.0.0.1')


@app.route('/car-elastic', methods=['POST'])
def car_elastic():
    outputLanguage = SearchPlatforms.ELASTIC
    outputDataModel = DataModels.CAR
    if request.data:
        pattern = request.data.decode("utf-8")  # decode the input string
        output = translate(
            pattern, outputLanguage, outputDataModel)
        return output['queries']
    else:
        print("No Request Data")  # when issues with input data
        return "No Request Data"


@app.route('/car-splunk', methods=['POST'])
def car_splunk():
    outputLanguage = SearchPlatforms.SPLUNK
    outputDataModel = DataModels.CAR
    if request.data:
        pattern = request.data.decode("utf-8")  # decode the input string
        output = translate(
            pattern, outputLanguage, outputDataModel)
        return output['queries']
    else:
        print("No Request Data")  # when issues with input data
        return "No Request Data"


@app.route('/cim-splunk', methods=['POST'])
def cim_splunk():
    outputLanguage = SearchPlatforms.SPLUNK
    outputDataModel = DataModels.CIM
    if request.data:
        pattern = request.data.decode("utf-8")  # decode the input string
        output = translate(
            pattern, outputLanguage, outputDataModel
        )
        return output['queries']
    else:
        print("No Request Data")  # when issues with input data
        return "No Request Data"


def main():
    app.run(debug=True, port=5000, host='127.0.0.1')


if __name__ == '__main__':
    # DEVELOPMENT Settings, change for production!!!
    main()
