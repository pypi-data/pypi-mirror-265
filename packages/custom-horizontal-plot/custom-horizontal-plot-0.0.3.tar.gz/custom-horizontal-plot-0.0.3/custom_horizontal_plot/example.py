import streamlit as st
from __init__ import horizontal_plot

st.set_page_config(layout="wide")

data = [
    {
      "index": 0,
      "label": "test",
      "valueLabel": "Total Skill Damage",
      "value": .45,
      "valueString": "4000",
      "frequencyLabel": "Total Number of Heroes",
      "frequency": 10,
      "freqPer": .5,
      "moreD": [
        { "id": 0, "label": "test", "value": 100, "perc": .5, "imgUrl":"" },
        { "id": 1, "label": "test", "value": 100, "perc": .25 },
        { "id": 2, "label": "test", "value": 100, "perc": .25 },
      ],
    },
    {
      "index": 0,
      "label": "test",
      "valueLabel": "Total Skill Damage",
      "value": .25,
      "valueString": "4000",
      "frequencyLabel": "Total Number of Heroes",
      "frequency": 10,
      "freqPer": .1,
      "moreD": [
        { "id": 0, "label": "test", "value": 100, "perc": .5 },
        { "id": 1, "label": "test", "value": 100, "perc": .25 },
        { "id": 2, "label": "test", "value": 100, "perc": .25 },
      ],
    },
    {
      "index": 0,
      "label": "test",
      "valueLabel": "Total Skill Damage",
      "value": .15,
      "valueString": "4000",
      "frequencyLabel": "Total Number of Heroes",
      "frequency": 10,
      "freqPer": .1,
      "moreD": [
        { "id": 0, "label": "test", "value": 100, "perc": .5 },
        { "id": 1, "label": "test", "value": 100, "perc": .25 },
        { "id": 2, "label": "test", "value": 100, "perc": .25 },
      ],
    },
    {
      "index": 0,
      "label": "test",
      "valueLabel": "Total Skill Damage",
      "value": .15,
      "valueString": "4000",
      "frequencyLabel": "Total Number of Heroes",
      "frequency": 10,
      "freqPer": .3,
      "moreD": [
        { "id": 0, "label": "test", "value": 100, "perc": .5 },
        { "id": 1, "label": "test", "value": 120, "perc": .25 },
        { "id": 2, "label": "test", "value": 150, "perc": .25 },
      ],
    },
  ]


titlesForChart = [
    { "index": 0, "label": "Total Damage" },
    { "index": 1, "label": "Hero Groups" }
  ]
with st.columns([1,8,1])[1]:
    horizontal_plot(data=data, titlesForChart=titlesForChart)