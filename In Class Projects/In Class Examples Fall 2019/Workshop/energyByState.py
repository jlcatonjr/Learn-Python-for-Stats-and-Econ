import pandas as pd
import numpy as np

state_names = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

df = pd.DataFrame({}, index = state_names)
print(df)
#energy_sources = ["Coal", "Natural Gas", "Crude Oil", "Nuclear"]
#for source in energy_sources:
#    
#    data_dict[source] = pd.from_excel("PSA (1)", sheet_name = source)
#    