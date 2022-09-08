from quickchart import QuickChart

qc = QuickChart()
# qc.width = 200
# qc.height = 150

# Config can be set as a string or as a nested dict


config_1="""{type: 'radialGauge',data: { datasets: [{ data: [ """

config_2="""], backgroundColor: getGradientFillHelper('horizontal', ['red', 'blue']),  }]  },
  options: { // See https://github.com/pandameister/chartjs-chart-radial-gauge#options    domain: [0, 100],
    trackColor: '#f0f8ff', centerPercentage: 90, centerArea: {  text: (val) => val + '%', },}
}"""

number='45'
qc.config = f"{config_1}{number}{config_2}"

image_url=qc.get_url()
# You can get the chart URL...
print(image_url)