"""Interactive Plotly Dash dashboard for the included demonstration dataset."""
from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

DATA = Path(__file__).resolve().parents[1] / "data" / "spacex_launches_demo.csv"
df = pd.read_csv(DATA)
app = Dash(__name__)
app.title = "SpaceY Launch Intelligence"
app.layout = html.Div([
    html.H1("SpaceY | Launch Intelligence"),
    html.P("Demonstration dashboard — included dataset is synthetic, not official launch history."),
    html.Div([
        html.Div([html.H3("Launch records"), html.H2(f"{len(df):,}")], className="kpi"),
        html.Div([html.H3("Reuse rate"), html.H2(f"{df.first_stage_reused.mean():.1%}")], className="kpi"),
        html.Div([html.H3("Median payload"), html.H2(f"{df.payload_mass_kg.median():,.0f} kg")], className="kpi"),
    ], style={"display":"flex","gap":"24px"}),
    dcc.Dropdown(options=[{"label":x,"value":x} for x in sorted(df.orbit.unique())],
                 value=sorted(df.orbit.unique()), multi=True, id="orbit-filter"),
    dcc.Graph(figure=px.bar(df.groupby("orbit",as_index=False).first_stage_reused.mean(),
                            x="orbit",y="first_stage_reused",title="Reuse rate by orbit")),
    dcc.Graph(figure=px.scatter(df,x="payload_mass_kg",y="booster_reuse_count",
                                color="first_stage_reused",hover_data=["orbit","launch_site"],
                                title="Payload mass vs. booster reuse history")),
], style={"fontFamily":"Arial","padding":"24px","maxWidth":"1100px","margin":"auto"})
if __name__ == "__main__":
    app.run(debug=True)
