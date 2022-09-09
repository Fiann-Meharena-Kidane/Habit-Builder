import json

from dominate.svg import pattern
from quickchart import QuickChart

qc = QuickChart()
qc.width = 400
qc.height = 200


# Config can be set as a string or as a nested dict
qc.config = configure
#
# # You can get the chart URL...
print(qc.get_short_url())
