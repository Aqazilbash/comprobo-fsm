# RoboBehaviors and Finite State Machines Project
Author Names: Alex Qazilbash, Mik Miller, and Maddy Fahey

For Olin ENGR3590 Computational Introduction to Robotics

## Project Overview
This is where you should provide an overall description of the project, including motivation (you may, for instance, want to link to the original assignment prompt), key design choices you made, and a summary of key takeaways. The rest of this markdown file then contains the specific details about your project.

## Individual Behaviors
In this section you will provide the details of each individual behavior you created / is part of this repository. At a minimum, you should have an emergency stop, driving in a shape, and wall-following. Any additional behaviors you created as part of your finite-state-machine should also be described here.

### Behavior 1: Name of the Behavior
This section should be composed of the following:
* A descriptive paragraph (what is the behavior and its intent).
* A paragraph of implementation details (what do you subscribe to, what do you publish, is this multi-threaded, did you implement a parameter server, and anything else essential to your implementation). This can include any testing/debugging interfacing you added.
* A paragraph that summarizes your key design decisions (and justifications, if relevant).
* A figure, gif, or embedded video demonstrating the behavior, with a link to the relevant `rosbag` in your repository. Any other explanatory visuals (e.g., geometric diagrams, flow charts, etc.) are also welcome.

### Behavior 1: Drive Square
The node directs the Neato to drive in a 1x1m square shape.

* A paragraph of implementation details (what do you subscribe to, what do you publish, is this multi-threaded, did you implement a parameter server, and anything else essential to your implementation). This can include any testing/debugging interfacing you added.
The node subscribes to the /estop topic, and if the received boolean is true, it publishes a linear and angular velocity of 0 to /twist. The node calculates its progress on its desired path based on odometry data


* A paragraph that summarizes your key design decisions (and justifications, if relevant).
* A figure, gif, or embedded video demonstrating the behavior, with a link to the relevant `rosbag` in your repository. Any other explanatory visuals (e.g., geometric diagrams, flow charts, etc.) are also welcome.

## Finite State Machine
In this section you will provide a description of your finite state machine including your intent, design decisions, and implementation details.

### Overall Design
In this section, you will have:
* At least one paragraph describing the intended performance of a Neato executing your finite state machine.
* Some explanation of your finite-state machine that includes:
    * A list of nodes with brief descriptions.
    * A list of transition criteria with brief descriptions.
    * This explanation can be in words or in a well-annotated diagram (or both)

### Implementation Details
In this section, you will describe how you implemented your finite state machine, with pointers to relevant code in the repository.

### Demonstration
In this section, you can provide some remarks about the current performance of your finite state machine, and can include figures, gifs, or embedded videos that demonstrate the performance. You can also link to relevant `rosbag` files in the repository.

## Learning Objectives and Final Takeaways
In this section, please report on each individual's learning objectives with this project and key takeaways. If there are any collective takeaways to report (such as possible future work), you may also report these here. 

## How To Run
This section should provide someone instructions for downloading, building, and running your code and any associated bagfiles.
