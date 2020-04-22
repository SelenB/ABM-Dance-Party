'''
Guidance taken from "Introduction to Mesa: Agent-based Modeling in Python" by Ng Wai Foong
https://towardsdatascience.com/introduction-to-mesa-agent-based-modeling-in-python-bcb0596e1c9a
'''

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

'''
Party Attendee Agent
'''


class PartyAgent(Agent):

    '''
    Create a new agent.
    Args:
        unique_id: Unique identifier for the agent.
        x, y: Agent initial location.
        agent_type: Indicator for the agent's socialization type (introvert, ambivert, extrovert)
    '''

    def __init__(self, pos, model, agent_type):

        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type
        self.dance_counter = 0
        if self.type == "introvert":
            self.happy_min_neighbors = 0
            self.happy_max_neighbors = 4
            self.happy_min_dancing = 0
            self.happy_max_dancing = 3
            self.base_dancing_probability = 0.05
        if self.type == "ambivert":
            self.happy_min_neighbors = 2
            self.happy_max_neighbors = 7
            self.happy_min_dancing = 0
            self.happy_max_dancing = 7
            self.base_dancing_probability = 0.3
        if self.type == "extrovert":
            self.happy_min_neighbors = 6
            self.happy_max_neighbors = 9
            self.happy_min_dancing = 3
            self.happy_max_dancing = 9
            self.base_dancing_probability = 0.55

    def step(self):

        # Count number of neighbors
        number_neighbors = 0
        number_dancing = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.dance_counter > 0:
                number_dancing += 1
            number_neighbors += 1

        dancing_probability = self.base_dancing_probability + 0.05 * number_dancing

        # When an agent starts dancing, they commit to dancing for three turns
        # After those three turns, it is up to chance whether the agent dances again
        if self.dance_counter >= 3:
            self.dance_counter = 0

        # If agent is dancing, then increase the dance counter
        if self.dance_counter > 0:
            self.dance_counter += 1

        # If agent has dance counter of 0, agent has random chance of dancing
        if self.dance_counter == 0:
            dancing = self.model.random.random()
            if dancing < dancing_probability:
                self.dance_counter += 1

        # If number of neighbors does not fall into happy range, move
        if number_neighbors <= self.happy_max_neighbors:
            if number_neighbors >= self.happy_min_neighbors:
                if number_dancing <= self.happy_max_dancing:
                    if number_dancing >= self.happy_min_dancing:
                        self.model.happy += 1
                        return
        self.model.grid.move_to_empty(self)


'''
Model class for the party model
'''


class PartyModel(Model):

    def __init__(self, height=20, width=20, number_introvert=30, number_ambivert=40, number_extrovert=30):
        '''
        '''

        self.height = height
        self.width = width

        self.number_attendees = 1.0 * \
            (number_introvert + number_ambivert + number_extrovert)

        self.number_introvert = number_introvert
        self.number_ambivert = number_ambivert
        self.number_extrovert = number_extrovert

        self.percent_introvert = number_introvert / self.number_attendees
        self.percent_ambivert = number_ambivert / self.number_attendees
        self.percent_extrovert = number_extrovert / self.number_attendees

        self.introvert_cutoff = self.percent_introvert
        self.ambivert_cutoff = self.percent_introvert + self.percent_ambivert

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)

        self.happy = 0
        self.happy_introverts = 0
        self.happy_ambiverts = 0
        self.happy_extroverts = 0
        self.datacollector = DataCollector(
            {"happy": "happy"},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})

        count = 0

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if count < self.number_attendees:
                extroversion = self.random.random()
                if extroversion < self.introvert_cutoff:
                    agent_type = "introvert"
                else:
                    if extroversion < self.ambivert_cutoff:
                        agent_type = "ambivert"
                    else:
                        agent_type = "extrovert"

                agent = PartyAgent((x, y), self, agent_type)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)
                count = count + 1
        self.running = True
        self.datacollector.collect(self)

    '''
    Run one step of the model. If all agents are happy, halt the model.
    '''

    def step(self):

        # Reset counters of happy agents
        self.happy = 0
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        if self.happy > self.schedule.get_agent_count() * 0.95:
            self.running = False
