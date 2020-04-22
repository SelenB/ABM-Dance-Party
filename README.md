# ABM-Dance-Party
### Agent-Based Modeling of Different Personality Types at a Dance Party

#### How to run on Mac (I do not have access to a Windows machine, but I believe it should be a similar process for Windows)

0. Download the repository as a zip file and unzip. This will create a folder called `ABM-Dance-Party-master`

1. Install python 3 https://www.python.org/downloads/

2. Install pip for python 3 https://pip.pypa.io/en/stable/installing/

3. Install mesa by running `$ pip install mesa` (or if that does not work then `$ pip3 install mesa`) in the command line/terminal. Do not type the `$` into the command line/terminal.

4. Navigate to the ABM-Dance-Party-master folder using the command line/terminal.
  If the `ABM-Dance-Party-master` folder is in your downloads folder, you would navigate to it with the following commands:
  
  `$ cd Downloads`
  
  `$ cd ABM-Dance-Party-master`
 
 5. In the command line, type `$ mesa runserver` This should make a window with the simulation pop up in your browser.
 
 6. Adjust the sliders to change the composition of personality types at the party, click reset, and click start to run the simulation.
 
 7. Whenever you want to change the composition of the party and run the simulation again, remember to click reset before clicking start to update the composition of the party.
 
#### Installation Troubleshooting

If you receive the error message `-bash: mesa: command not found` when trying to install mesa, run the following in your command line:
`$ export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"` and then close and reopen the terminal.
