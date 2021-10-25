import io
from textfsm import TextFSM

textFSM_template = """Value Year (\d+)
Value MonthDay (\d+)
Value Month (\w+)
Value Timezone (\S+)
Value Time (..:..:..)

Start
  ^${Time}.* ${Timezone} \w+ ${Month} ${MonthDay} ${Year} -> Record"""

raw_data = "17:00:00.0 CET Mon Okt 26 2021"

template = io.StringIO(textFSM_template)
parser = TextFSM(template)
output = parser.ParseTextToDicts(text=raw_data)

print(output)
