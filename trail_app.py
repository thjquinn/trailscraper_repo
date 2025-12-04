import streamlit as st
import pandas as pd
import numpy as np


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
	df = pd.read_csv(path)
	# Normalize some columns for safer filtering
	if 'difficulty' in df.columns:
		df['difficulty'] = df['difficulty'].fillna('Unknown').astype(str)
	if 'type' in df.columns:
		df['type'] = df['type'].fillna('Unknown').astype(str)
	if 'trail_name' in df.columns:
		df['trail_name'] = df['trail_name'].astype(str)
	if 'description' in df.columns:
		df['description'] = df['description'].astype(str)
	return df


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
	st.sidebar.header('Filter trails')

	# State filter
	states = sorted(df['state'].dropna().unique().tolist()) if 'state' in df.columns else []
	selected_states = st.sidebar.multiselect('State', options=states, default=states)
	if selected_states:
		df = df[df['state'].isin(selected_states)]

	# Type filter
	if 'type' in df.columns:
		types = sorted(df['type'].dropna().unique().tolist())
		sel_types = st.sidebar.multiselect('Trail type', options=types, default=types)
		if sel_types:
			df = df[df['type'].isin(sel_types)]

	# Difficulty filter
	if 'difficulty' in df.columns:
		difficulties = sorted(df['difficulty'].dropna().unique().tolist())
		sel_diff = st.sidebar.multiselect('Difficulty', options=difficulties, default=difficulties)
		if sel_diff:
			df = df[df['difficulty'].isin(sel_diff)]

	# Numeric ranges
	def range_slider_for(col, name, fmt=None):
		if col in df.columns:
			mn = float(np.nanmin(df[col].replace([np.inf, -np.inf], np.nan)))
			mx = float(np.nanmax(df[col].replace([np.inf, -np.inf], np.nan)))
			if np.isnan(mn) or np.isnan(mx):
				return df
			lo, hi = st.sidebar.slider(name, min_value=mn, max_value=mx, value=(mn, mx))
			return df[(df[col] >= lo) & (df[col] <= hi)]
		return df

	df = range_slider_for('distance(mi)', 'Distance (mi)')
	df = range_slider_for('rating', 'Rating')
	df = range_slider_for('ascent(ft)', 'Ascent (ft)')
	df = range_slider_for('avg_grade(%)', 'Avg grade (%)')

	# Text search
	text = st.sidebar.text_input('Search in name / description')
	if text:
		mask = df['trail_name'].str.contains(text, case=False, na=False) | df['description'].str.contains(text, case=False, na=False)
		df = df[mask]

	return df


def main():
	st.set_page_config(page_title='Trail Finder', layout='wide')
	st.title('Trail Finder — find the best trail for you')

	df = load_data('all_trails.csv')

	filtered = filter_data(df.copy())

	st.markdown(f"**{len(filtered)}** trails match your filters")

	sort_by = st.selectbox('Sort by', options=['rating', 'distance(mi)', 'ascent(ft)', 'avg_grade(%)', 'max_grade(%)'], index=0)
	ascending = st.checkbox('Ascending', value=False)
	if sort_by in filtered.columns:
		filtered = filtered.sort_values(by=sort_by, ascending=ascending)

	cols_to_show = ['trail_name', 'state', 'distance(mi)', 'type', 'difficulty', 'rating', 'ascent(ft)', 'avg_grade(%)']
	present_cols = [c for c in cols_to_show if c in filtered.columns]

	# Paging / number to show
	n_show = st.number_input('Number of results to show', min_value=1, max_value=500, value=20, step=1)
	st.dataframe(filtered[present_cols].head(n_show).reset_index(drop=True))

	# Show details for top result
	if not filtered.empty:
		st.subheader('Top match')
		top = filtered.iloc[0]
		c1, c2 = st.columns([2, 3])
		with c1:
			st.markdown(f"### {top.get('trail_name', 'Unknown')}")
			st.write(f"**State:** {top.get('state', '')}")
			st.write(f"**Distance (mi):** {top.get('distance(mi)', '')}")
			st.write(f"**Type:** {top.get('type', '')}")
			st.write(f"**Difficulty:** {top.get('difficulty', '')}")
			st.write(f"**Rating:** {top.get('rating', '')}")
		with c2:
			st.markdown('**Description**')
			st.write(top.get('description', 'No description'))

	# Expanders for multiple results
	st.subheader('Results (details)')
	for _, row in filtered.head(n_show).iterrows():
		with st.expander(f"{row.get('trail_name','Unknown')} — {row.get('state','')}"):
			st.write(row.to_dict())

	# Download filtered data
	csv = filtered.to_csv(index=False)
	st.download_button('Download filtered CSV', data=csv, file_name='filtered_trails.csv', mime='text/csv')


if __name__ == '__main__':
	main()
