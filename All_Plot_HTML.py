import pandas as pd
import plotly.graph_objects as go

# ------------------------------------------------------------------
# File path
# ------------------------------------------------------------------
file_path = r"C:\Users\dialameh.1\OneDrive - The Ohio State University\General - Automated Drainage Water Managent\Flow and Load Data\Henry (Rettig)\Data Processing\All_Plot.xlsx"

# ------------------------------------------------------------------
# Read Excel file (LOCK columns A–G)
# ------------------------------------------------------------------
df = pd.read_excel(file_path, usecols="A:G")

df.columns = [
    "Date",
    "Manual_Structure_WL",
    "Manual_Piez_S1",
    "Manual_Piez_S2",
    "Auto_Structure_WL",
    "SHIN_N1",
    "SHIN_N2"
]

df["Date"] = pd.to_datetime(df["Date"])

cm_to_ft = 0.0328084

# ------------------------------------------------------------------
# Create interactive plot
# ------------------------------------------------------------------
fig = go.Figure()

def add_line(y, name):
    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=y,
        mode="lines",
        name=name,
        customdata=(y.values * cm_to_ft),  # IMPORTANT for hover
        hovertemplate=
            f"Data: {name}<br>"
            "Date: %{x|%Y-%m-%d}<br>"
            "Hour: %{x|%H:%M}<br>"
            "Value: %{y:.0f} cm (%{customdata:.1f} ft)"
            "<extra></extra>"
    ))

add_line(df["Manual_Structure_WL"], "Water-Level in Manual Structure")
add_line(df["Auto_Structure_WL"], "Water-Level in Automated Structure")
add_line(df["Manual_Piez_S1"], "Piezometer W1 (Manual Edge)")
add_line(df["Manual_Piez_S2"], "Piezometer W2 (Manual Center)")
add_line(df["SHIN_N1"], "Piezometer E1 (Automated Edge)")
add_line(df["SHIN_N2"], "Piezometer E2 (Automated Center)")

# ------------------------------------------------------------------
# AXIS & GRID CONTROL (cm + ft)
# ------------------------------------------------------------------
tick_start = 20450
tick_end = 20700
tick_step = 10

shared_ticks = list(range(tick_start, tick_end + tick_step, tick_step))

left_tick_text = [
    f"{v} cm ({v * cm_to_ft:.1f} ft)"
    for v in shared_ticks
]

fig.update_layout(
    title=dict(
        text="Water-Table and Water-Level in Manual and Automated Structures "
             "(OWDA Rettig Site, Henry County, Ohio)",
        font=dict(size=20, family="Arial", weight="bold")
    ),

    # X-axis
    xaxis=dict(
        tickformat="%B-%Y",
        dtick="M1",
        tickangle=-45,
        showline=True,
        linewidth=2,
        linecolor="black",
        mirror=True,
        tickfont=dict(size=14, family="Arial", weight="bold"),
        showgrid=True,
        gridcolor="lightgray"
    ),

    # Y-axis (Elevation cm + ft)
    yaxis=dict(
        title="Elevation (cm / ft)",
        range=[20450, 20700],
        tickmode="array",
        tickvals=shared_ticks,
        ticktext=left_tick_text,
        showline=True,
        linewidth=2,
        linecolor="black",
        mirror=True,
        tickfont=dict(size=14, family="Arial", weight="bold"),
        titlefont=dict(size=16, family="Arial", weight="bold"),
        showgrid=True,
        gridcolor="lightgray"
    ),

    template="plotly_white",
    hovermode="x unified",

    legend=dict(
        font=dict(size=13, family="Arial"),
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="black",
        borderwidth=1
    )
)

# ------------------------------------------------------------------
# SHOW ONLINE
# ------------------------------------------------------------------
fig.show()
# ------------------------------------------------------------------
# SAVE HTML FOR GITHUB (EXPLICIT)
# ------------------------------------------------------------------
output_path = r"C:\Users\dialameh.1\OneDrive - The Ohio State University\General - Automated Drainage Water Managent\Flow and Load Data\Henry (Rettig)\Data Processing\index.html"

fig.write_html(
    output_path,
    include_plotlyjs=True,   # self-contained, GitHub-safe
    auto_open=True           # opens browser to confirm
)

print("HTML file created at:")
print(output_path)
