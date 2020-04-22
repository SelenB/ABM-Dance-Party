'''
Guidance taken from "Introduction to Mesa: Agent-based Modeling in Python" by Ng Wai Foong
https://towardsdatascience.com/introduction-to-mesa-agent-based-modeling-in-python-bcb0596e1c9a
'''

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import PartyModel

'''
Display a text count of how many happy agents there are.
'''


class HappyElement(TextElement):

    def __init__(self):
        pass

    def render(self, model):
        return "Happy agents: " + str(model.happy)


'''
Portrayal Method for canvas
'''


def party_draw(agent):

    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    portrayal["stroke_color"] = "#000000"
    if agent.type == "introvert":
        if agent.dance_counter == 0:
            portrayal["Color"] = ["#FF0000", "#FFFFFF"]
        else:
            portrayal["Color"] = ["#FF0000", "#FF9999"]
    else:
        if agent.type == "ambivert":
            if agent.dance_counter == 0:
                portrayal["Color"] = ["#461f7a", "#FFFFFF"]
            else:
                portrayal["Color"] = ["#461f7a", "#9a71d1"]
        else:
            
            if agent.dance_counter == 0:
                portrayal["Color"] = ["#0000FF", "#FFFFFF"]
            else:
                portrayal["Color"] = ["#0000FF", "#9999FF"]
    return portrayal


happy_element = HappyElement()
canvas_element = CanvasGrid(party_draw, 20, 20, 500, 500)
happy_chart = ChartModule([{"Label": "happy", "Color": "Black"}])

model_params = {
    "height": 20,
    "width": 20,
    "number_introvert": UserSettableParameter("slider", "Number of Introverts (Red)", 30, 1, 101, 10),
    "number_ambivert": UserSettableParameter("slider", "Number of Ambiverts (Purple)", 40, 1, 101, 10),
    "number_extrovert": UserSettableParameter("slider", "Number of Extroverts (Blue)", 30, 1, 101, 10)
}

server = ModularServer(PartyModel,
                       [canvas_element, happy_element, happy_chart],
                       "Party Simulation", model_params)
