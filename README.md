# README


# Trail Finder (Streamlit)

This is a simple Streamlit app to explore and filter trails from
`all_trails.csv`. A dataset made from scraping hikingproject.com.
Currently, there is data from all of the sites’ available trails in
Indiana, Utah, and Pennsylvania.

## Requirements

Install the dependencies (PowerShell):

``` powershell
python -m pip install -r requirements.txt
```

## Run

From the project folder in PowerShell run:

``` powershell
streamlit run trail_app.py
```

The app will open in your browser. Use the sidebar to filter by state,
trail type, difficulty, distance, rating, ascent, and search text. You
can download the filtered results as CSV using the provided button.
