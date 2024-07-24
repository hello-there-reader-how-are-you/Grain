from llama_cpp import Llama
from clock import *
from youtube import *
from banna_prompt import PROMPT
import re
import time


output = "sometbing [[[play, rise guys, chalkeaters, N/A]]] or other"

output = f"{re.search(r'\[\[.*?\[(.*?)\].*?\]\]', output).group(1)}".split(",")
output = [item for item in output if item != " None"]

print(output)


if output[0] == "play":
    yt(*output[1:])

if output[0] == "timer":
    clock().timer(output[1])

if output[0] == "alarm":
    clock().alarm(output[1])





time.sleep(10)
print("done")
time.sleep(5)