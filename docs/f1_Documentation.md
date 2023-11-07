# Formula 1 Simulation

## Overview

This Python script simulates a Formula 1 race, including practice sessions, qualifying, and the actual race. It uses a roster of F1 drivers and 2022 F1 tracks. The simulation takes into account driver morale, car performance, and randomness to generate realistic results for practice, qualifying, and the race.

## Prerequisites

To run the simulation, you need to have Python installed. The script uses the following libraries: random, statistics, and matplotlib. You can install them using pip:

```bash
pip install matplotlib
```

## Usage

To run the simulation, simply execute the Python script:

```bash
python main.py
```

## Features

### Track Selection

The script selects a random F1 track from the 2022 season for the simulation.

### Practice Session

The practice session simulates the performance of each driver on the selected track. It calculates lap times considering driver morale and car performance. The results are displayed in the console and saved as a bar chart in 'practice_results.png'.

### Qualifying Session

The qualifying session determines the starting grid for the race. Like the practice session, it calculates lap times and displays the results in the console and saves them as a bar chart in 'qualifying_results.png'.

### Race Simulation

The race simulation runs over a specified number of laps on the selected track. It simulates the drivers' lap times, and the results are displayed in the console. The driver with the best overall performance is declared the winner.

## Results

The simulation provides results for the practice session, qualifying, and the final race, including the winner and the driver of the day.

## Authors

- [Mert Ahmetoğlu]

## License

This project is licensed under the [License Name] - see the [LICENSE.md](https://github.com/asikLEMMY/formula1-simulation/blob/main/LICENSE) file for details.

## Acknowledgments

- Python and Matplotlib library was used.

## Conclusion

This documentation provides an overview of the Formula 1 simulation script. You can use this as a starting point and expand it to include more detailed explanations, additional features, or customizations based on your project's requirements.

