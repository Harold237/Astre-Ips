import streamlit as st

def get_chart_78341403():
    import plotly.graph_objects as go

    schools = ["Brown", "NYU", "Notre Dame", "Cornell", "Tufts", "Yale",
               "Dartmouth", "Chicago", "Columbia", "Duke", "Georgetown",
               "Princeton", "U.Penn", "Stanford", "MIT", "Harvard"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[72, 67, 73, 80, 76, 79, 84, 78, 86, 93, 94, 90, 92, 96, 94, 112],
        y=schools,
        marker=dict(color="crimson", size=12),
        mode="markers",
        name="Women",
    ))

    fig.add_trace(go.Scatter(
        x=[92, 94, 100, 107, 112, 114, 114, 118, 119, 124, 131, 137, 141, 151, 152, 165],
        y=schools,
        marker=dict(color="gold", size=12),
        mode="markers",
        name="Men",
    ))

    fig.update_layout(title="Gender Earnings Disparity",
                      xaxis_title="Annual Salary (in thousands)",
                      yaxis_title="School")


    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        st.plotly_chart(fig, theme=None)