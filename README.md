# Sustainable Fertilizer Optimizer

## Overview
The **Sustainable Fertilizer Optimizer** is a web application designed to assist farmers in optimizing fertilizer usage based on soil health, crop type, and weather patterns. The app provides AI-powered recommendations for sustainable farming practices and supports multilingual output for a global audience. It also features a sleek, responsive design with dark mode support and an engaging image carousel.

---

## Features

- **Soil Health Analysis**:
  Select from predefined soil types or input specific soil details.

- **Crop-Specific Recommendations**:
  Choose a crop type or input custom crop data for targeted suggestions.

- **Weather Pattern Integration**:
  Customize recommendations based on weather conditions to maximize yield.

- **Multilingual Support**:
  Translate recommendations into multiple languages, including English, Tamil, Hindi, and Arabic.

- **Dark Mode**:
  Toggle between light and dark themes for improved accessibility and user experience.

- **Image Carousel**:
  Display relevant images to enhance user engagement and provide visual context.

---

## Technologies Used

- **Python**: Core programming language.
- **Dash**: For building interactive web applications.
- **Dash Bootstrap Components**: For styling and responsive design.
- **Google Generative AI (Gemini)**: To generate AI-powered recommendations.
- **Deep Translator**: For language translation.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/4LPH7/Eco_fertil.git
   cd Eco_fertil
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:
   - Create a `.env` file and add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

5. **Run the Application**:
   ```bash
   python app.py
   ```

6. **Access the App**:
   Open `http://127.0.0.1:8050` in your web browser.

---

## Usage

1. Select or input:
   - Soil health data.
   - Crop type.
   - Weather patterns.
2. Optionally, select a language for translation.
3. Click on **"Get Recommendations"** to view AI-powered suggestions.


---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Google Generative AI**: For providing the API used in the project.
- **Dash**: For making interactive web development simple and efficient.
- **Deep Translator**: For seamless multilingual support.


---

## Author

- GitHub: [@4LPH7](https://github.com/4LPH7)

Feel free to contribute or suggest improvements!

---
### Show your support

Give a ⭐ if you like this website!

<a href="https://buymeacoffee.com/arulartadg" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-violet.png" alt="Buy Me A Coffee" height= "60px" width= "217px" ></a>
