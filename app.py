import streamlit as st
import pandas as pd

# Load CSV Data
@st.cache_data
def load_data(file_path):

    return pd.read_csv(file_path).drop(["Unnamed: 0"], axis=1)

def filter_data(df, column, filter_string):
    if filter_string:
        return df[df[column].str.contains(filter_string, case=False, na=False)]
    return df

def sort_data(df, sort_column, ascending=True):
    return df.sort_values(by=sort_column, ascending=ascending)

# Load the data
file_path = "scenes_synopses_html.csv"  # Path to your CSV file
scenes_df = load_data(file_path)
performers_df = load_data("performers_html.csv").drop_duplicates()


tab = st.radio("Select a table", ["Scenes Table", "Performers Table"])

st.sidebar.header("Filter Options")

if tab == "Scenes Table":
    column_to_filter = st.sidebar.selectbox("Select Column to Filter",scenes_df.columns)
    filter_string = st.sidebar.text_input("Enter Substring to Search", "")
    filtered_df = filter_data(scenes_df, column_to_filter, filter_string)
    
    # Sort settings
    sort_column = st.sidebar.selectbox("Select Column to Sort By", scenes_df.columns)
    ascending = st.sidebar.checkbox("Sort Ascending", value=True)

    st.write("### Table 1: Film Information")
    if filter_string:
        st.write(f"#### {len(filtered_df)} Results")

    html_table = filtered_df.to_html(escape=False, index=False)
    # Custom CSS for table formatting
    css = """
        <style>
            table {
                width: 150%;
                border-collapse: collapse;
            }
            th, td {
                padding: 10px;
                text-align: left;
                border: 1px solid #ddd;
            }
            th {
                background-color: #f2f2f2;
            }
            td:nth-child(1) {
                max-width: 500px;  /* Adjust width for the first column (Title) */
            }
            td:nth-child(2) {
                max-width: 500px;  /* Adjust width for the second column (Doorway) */
            }
            td:nth-child(3) {
                max-width: 100px;  /* Adjust width for the third column (Year) */
            }
            td:nth-child(4) {
                max-width: 250px;  /* Adjust width for the fourth column (Link) */
            }
            td:nth-child(5) {
                max-width: 1500px;  /* Adjust width for the fifth column (Synopsis) */
            }

        </style>
    """

    if sort_column:
        sort_df = sort_data(filtered_df, sort_column, ascending)
        html_table_sort = sort_df.to_html(escape=False, index=False)

        st.markdown(css, unsafe_allow_html=True)
        st.markdown(html_table_sort, unsafe_allow_html=True)

    else:
            # Display the table with clickable links
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(html_table, unsafe_allow_html=True)



elif tab == "Performers Table":
    st.write("### Table 2: Performer Information")
    column_to_filter = st.sidebar.selectbox("Select Column to Filter", performers_df.columns)
    filter_string = st.sidebar.text_input("Enter Substring to Search", "")

    filtered_df = filter_data(performers_df, column_to_filter, filter_string)
    html_table = filtered_df.to_html(escape=False, index=False)
    
    # Sort settings
    sort_column = st.sidebar.selectbox("Select Column to Sort By", performers_df.columns)
    ascending = st.sidebar.checkbox("Sort Ascending", value=True)

    if filter_string:
        st.write(f"#### {len(filtered_df)} Results")

    # Display the table with clickable links
    if sort_column:
        sort_df = sort_data(filtered_df, sort_column, ascending)
        html_table_sort = sort_df.to_html(escape=False, index=False)

        st.markdown(html_table_sort, unsafe_allow_html=True)
    else:
        st.markdown(html_table, unsafe_allow_html=True)



# # Filter the DataFrame if a filter string is provided
# if filter_string:
#     filtered_df = df[df[column_to_filter].str.contains(filter_string, case=False, na=False)]
#     st.write(
#         f"### Videos Table (filtered to rows where `{column_to_filter}` contains `{filter_string}`)"
#     )   

#     html_table = filtered_df.to_html(escape=False, index=False)
    
#     # Adjustable dimensions
#     table_height = st.sidebar.slider("Table Dimensions (px)", min_value=200, max_value=800, value=600)

#     # Display the table with clickable links
#     st.markdown(html_table, unsafe_allow_html=True)
# else:
#     st.write("### Videos Table (full)")
#     html_table = df.to_html(escape=False, index=False)

#         # Adjustable dimensions
#     table_height = st.sidebar.slider("Table Height (px)", min_value=200, max_value=800, value=600)

#     # Display the table with adjustable dimensions
#     st.markdown(html_table, unsafe_allow_html=True)



