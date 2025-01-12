import os
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import google.generativeai as genai
from deep_translator import GoogleTranslator

# Configure the API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b-exp-0827",
    generation_config=generation_config
)

# Dash app initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H2("🌿 Sustainable Farming & Fertilizer Optimizer", className="text-center my-4"), width=12)
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Soil Health Data:", className="fw-bold"),
                        dcc.Dropdown(
                            id="soil_health",
                            options=[
                                {"label": "Loamy", "value": "Loamy"},
                                {"label": "Clayey", "value": "Clayey"},
                                {"label": "Sandy", "value": "Sandy"},
                                {"label": "Silty", "value": "Silty"},
                                {"label": "Peaty", "value": "Peaty"},
                                {"label": "Saline", "value": "Saline"},
                                {"label": "Chalky", "value": "Chalky"},
                                {"label": "Organic", "value": "Organic"}
                            ],
                            placeholder="Select Soil Type",
                            className="mb-3"
                        ),
                        dcc.Input(
                            id="soil_input",
                            type="text",
                            placeholder="Or enter specific soil details",
                            className="mb-3 form-control"
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Label("Crop Type:", className="fw-bold"),
                        dcc.Dropdown(
                            id="crop_type",
                            options=[
                                {"label": "Wheat", "value": "Wheat"},
                                {"label": "Rice", "value": "Rice"},
                                {"label": "Corn", "value": "Corn"},
                                {"label": "Soybean", "value": "Soybean"},
                                {"label": "Barley", "value": "Barley"},
                                {"label": "Sugarcane", "value": "Sugarcane"},
                                {"label": "Cotton", "value": "Cotton"},
                                {"label": "Tomato", "value": "Tomato"},
                                {"label": "Potato", "value": "Potato"},
                                {"label": "Maize", "value": "Maize"}
                            ],
                            placeholder="Select Crop Type",
                            className="mb-3"
                        ),
                        dcc.Input(
                            id="crop_input",
                            type="text",
                            placeholder="Or enter specific crop details",
                            className="mb-3 form-control"
                        ),
                    ],
                    width=6,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Weather Patterns:", className="fw-bold"),
                        dcc.Dropdown(
                            id="weather_patterns",
                            options=[
                                {"label": "Sunny", "value": "Sunny"},
                                {"label": "Rainy", "value": "Rainy"},
                                {"label": "Cloudy", "value": "Cloudy"},
                                {"label": "Windy", "value": "Windy"},
                                {"label": "Snowy", "value": "Snowy"},
                                {"label": "Humid", "value": "Humid"},
                                {"label": "Dry", "value": "Dry"},
                                {"label": "Stormy", "value": "Stormy"}
                            ],
                            placeholder="Select Weather Pattern",
                            className="mb-3"
                        ),
                        dcc.Input(
                            id="weather_input",
                            type="text",
                            placeholder="Or enter specific weather details",
                            className="mb-3 form-control"
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Label("Translate to Language:", className="fw-bold"),
                        dcc.Dropdown(
                            id="language",
                            options=[
                                {"label": "English", "value": "english"},
                                {"label": "Tamil", "value": "tamil"},
                                {"label": "Hindi", "value": "hindi"},
                                {"label": "Arabic", "value": "arabic"}
                            ],
                            placeholder="Select Language",
                            className="mb-3"
                        ),
                    ],
                    width=6,
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Get Recommendations", id="submit-button", color="success", className="mt-3", n_clicks=0),
                width={"size": 4, "offset": 4},
                className="text-center"
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    id="loading-output",
                    type="circle",
                    children=[
                        html.Div(id="output_recommendations", className="mt-4", style={"white-space": "pre-wrap"})
                    ]
                ),
                width=12
            )
        ),
    ],
    fluid=True,
)


# Callbacks
@app.callback(
    Output("output_recommendations", "children"),
    [Input("submit-button", "n_clicks")],
    [State("soil_health", "value"), State("soil_input", "value"),
     State("crop_type", "value"), State("crop_input", "value"),
     State("weather_patterns", "value"), State("weather_input", "value"),
     State("language", "value")]
)
def get_recommendations(n_clicks, soil_health, soil_input, crop_type, crop_input, weather_patterns, weather_input, language):
    if n_clicks > 0:
        # Use either the dropdown value or the custom input value
        soil_info = soil_input if soil_input else soil_health
        crop_info = crop_input if crop_input else crop_type
        weather_info = weather_input if weather_input else weather_patterns

        if soil_info and crop_info and weather_info:
            # Formulate a prompt for the AI model
            prompt = f"Based on the following data:\n" \
                     f"Soil Health: {soil_info}\n" \
                     f"Crop Type: {crop_info}\n" \
                     f"Weather Patterns: {weather_info}\n" \
                     f"Provide the best type of fertilizer, recommended amount, cost-efficient farming methods, and simple ideas for using organic fertilizers to enhance soil health and crop yield."

            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(prompt)

            output_text = response.text.replace("## ", "\n\n").replace("**", "")

            # Translate if necessary
            if language and language != "english":
                try:
                    output_text = GoogleTranslator(source='auto', target=language).translate(output_text)
                except Exception as e:
                    return f"Error translating text: {e}"

            return output_text
        else:
            return "Please select all fields."
    else:
        return ""


if __name__ == '__main__':
    app.run_server(debug=True)
