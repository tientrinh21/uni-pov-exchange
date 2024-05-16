from flask_restful import Resource
from flask import jsonify
import pandas as pd

class getExchangeData(Resource):
    def exchData():
        try:
            exchange_data = pd.read_excel('exchange.xlsx', header=0)

            # Group the data by country
            grouped_data = exchange_data.groupby(exchange_data.columns[0])

            # Convert grouped data to JSON
            json_data = {}

            for country, group_data in grouped_data:
                country = country[0] + country[1:].lower()
                country_data = []
                for index, row in group_data.iterrows():
                    university_name = row[1]  # Assuming university name is in the second column
                    university_info = {university_name: row[2:].to_dict()}
                    country_data.append(university_info)
                json_data[country] = country_data

            return jsonify(json_data)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # @app.route('/rank')   
    # def ranking():
    #     try:
    #         ranking_data = pd.read_csv('ranking.csv', usecols=[0, 1], header=0)

    #         # Initialize JSON data structure
    #         json_data = []

    #         # Iterate over each row in the DataFrame
    #         for index, row in ranking_data.iterrows():
    #             ranking = row[0]
    #             university_name = row[1]

    #             # Create a dictionary for the current row
    #             university_info = {
    #                 'ranking': ranking,
    #                 'university_name': university_name
    #             }

    #             # Add the dictionary to the json_data list
    #             json_data.append(university_info)

    #         return jsonify(json_data)
    #     except Exception as e:
    #         return jsonify({'error': str(e)}), 500