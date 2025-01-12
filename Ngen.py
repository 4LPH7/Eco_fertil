import os
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import google.generativeai as genai
from deep_translator import GoogleTranslator, exceptions

# Configure the API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

genai.configure(api_key=api_key)

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
        # Title
        dbc.Row(
            dbc.Col(html.H2("\ud83c\udf3f Sustainable Farming & Fertilizer Optimizer", className="text-center my-4"), width=12)
        ),
        # Image Carousel
        dbc.Row(
            dbc.Col(
                dbc.Carousel(
                    items=[
                        {"key": "1", "src": "https://via.placeholder.com/800x400?text=Loamy+Soil", "alt": "Loamy Soil"},
                        {"key": "2", "src": "https://via.placeholder.com/800x400?text=Crop+Varieties", "alt": "Crops"},
                        {"key": "3", "src": "https://via.placeholder.com/800x400?text=Weather+Patterns", "alt": "Weather"},
                        {"key": "4", "src": "https://via.placeholder.com/800x400?text=Organic+Fertilizers", "alt": "Organic Fertilizers"},
                    ],
                    controls=True,
                    indicators=True,
                    interval=3000,
                    className="mb-4",
                ),
                width=12,
            )
        ),
        # Input Fields
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Soil Health Data:", className="fw-bold"),
                        dcc.Dropdown(
                            id="soil_health",
                            options=[
                                {"label": soil, "value": soil}
                                for soil in ["Loamy", "Clayey", "Sandy", "Silty", "Peaty", "Saline", "Chalky", "Organic"]
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
                                {"label": crop, "value": crop}
                                for crop in ["Wheat", "Rice", "Corn", "Soybean", "Barley", "Sugarcane", "Cotton", "Tomato", "Potato", "Maize"]
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
                                {"label": weather, "value": weather}
                                for weather in ["Sunny", "Rainy", "Cloudy", "Windy", "Snowy", "Humid", "Dry", "Stormy"]
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
                                {"label": lang.capitalize(), "value": lang}
                                for lang in ["english", "tamil", "hindi", "arabic"]
                            ],
                            placeholder="Select Language",
                            className="mb-3"
                        ),
                    ],
                    width=6,
                ),
            ]
        ),
        # Submit Button
        dbc.Row(
            dbc.Col(
                dbc.Button("Get Recommendations", id="submit-button", color="success", className="mt-3", n_clicks=0),
                width={"size": 4, "offset": 4},
                className="text-center"
            )
        ),
        # Output Display
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    id="loading-output",
                    type="circle",
                    children=[html.Div(id="output_recommendations", className="mt-4", style={"white-space": "pre-wrap"})],
                ),
                width=12,
            )
        ),
    ],
    fluid=True,
)

# Helper function for translation
def safe_translate(text, target_language):
    if target_language == "english":
        return text
    try:
        return GoogleTranslator(source='auto', target=target_language).translate(text)
    except exceptions.TranslationNotFound:
        return "Translation service is unavailable for the selected language."
    except Exception as e:
        return f"Error during translation: {e}"

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
        soil_info = soil_input or soil_health
        crop_info = crop_input or crop_type
        weather_info = weather_input or weather_patterns

        if soil_info and crop_info and weather_info:
            prompt = f"Based on the following data:\n" \
                     f"Soil Health: {soil_info}\n" \
                     f"Crop Type: {crop_info}\n" \
                     f"Weather Patterns: {weather_info}\n" \
                     f"Provide fertilizer suggestions, organic methods, and yield optimization tips."

            try:
                chat_session = model.start_chat(history=[])
                response = chat_session.send_message(prompt)
                output_text = response.text.replace("## ", "\n\n").replace("**", "")
                return safe_translate(output_text, language)
            except Exception as e:
                return f"Error generating recommendations: {e}"
        else:
            return "Please provide input for all required fields."
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
