# Eye Tracker Analyzer

**Eye Tracker Analyzer** is a tool for analyzing and visualizing eye-tracking data collected in an academic experiment. The project includes data cleaning, statistical analysis, and visualization to better understand observed patterns.

## Project Structure

```
Python Project/
├── data
│   ├── Clean_data
│   └── Raw_Data
│       ├── participants
│       └── fixations_on_face_by_recording
├── src
│   ├── data_cleaner.py         # Cleans and processes raw data
│   ├── data_analysis.py        # Analyzes data and calculates statistics
│   └── data_visualizer.py      # Generates visualizations from processed data
├── pyproject.toml              # Dependency management
└── README.md                   # Project documentation
```

## Installation & Usage

### 1. Install Dependencies

To install the dependencies, use the following command:

```sh
pip install .
```

For development dependencies, use:

```sh
pip install .[dev]
```

### 2. Run the Project
put raw participants folders in the participants directory and fixations_on_face in the raw data directory and you're good to go!
run main.py for full analysis! or you can run each python file seperatly 

```sh
python src/main.py
```

## File Descriptions

### `data_cleaner.py`
- Cleans raw data files.
- Splits CSV files by participant.
- Converts recording IDs to sequential numbers.
- Removes unnecessary columns.
- Labels trials by stimulus type (noisy/quiet).
- Deletes irrelevant data.

### `data_analysis.py`
- Generates overall averages and standard deviations.
- Groups data by **trial ID**.

### `data_visualizer.py`
- Creates visualizations comparing noisy vs. quiet conditions.
- Shows trends in fixations, blinks, and saccades.
- Saves plots in the **Clean_data** directory.

## Important Directories

- **Raw_Data/** – Contains raw data files.
- **Clean_data/** – Contains processed data and summary results.
- **src/** – Contains the main source code files.

## Authors

- Omer Aharonovich <omer.aharonovich@live.biu.ac.il>
- Yaarah Edel <yaarah.edel@gmail.com>
