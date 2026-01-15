import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, "Engines"))

from helloworld import HelloWorld

hw = HelloWorld("Hi there")

print(hw.greet())