from openai import OpenAI
import json
import board
import neopixel
import time
from datetime import datetime
import random
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# LED Strip Configuration
LED_PIN = board.D18
LED_COUNT = 143
LED_BRIGHTNESS = 0.05 # Brightness (0.0 to 1.0)
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False)

api_key = ""

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


role = """
I have a WS2812B LED strip with 143 LEDs, controlled by a Raspberry Pi using the neopixel library in Python.
I want to dynamically generate Python functions that create LED effects based on a word or phrase.

**Requirements:**
- The AI should return a JSON response with a `"function"` key containing a valid Python function as a string.
- The function should take a `pixels` object (from neopixel.NeoPixel) and modify it based on the theme.
- The function must be named `light_func()`.
- The function will be called repeatedly in a loop, so it should perform ONE FRAME of animation per call.
- Each call should make a small change to create smooth animations.
- DO NOT use time.sleep() in the function - timing is handled by the main loop.
- DO NOT set pixels.brightness in the function - brightness is controlled globally.
- Use a class variable to track animation state between calls:
  - Define: light_func.step = 0 at the start of the function if not hasattr(light_func, 'step')
  - Increment: light_func.step += 1 at the end of each call
  - Use light_func.step to control animation progression

**Animation Guidelines:**
- For smooth movement effects: Move 1 pixel position per function call
- For color transitions: Change RGB values by small amounts (1-5) per call
- For blinking/flashing: Toggle state every 20-30 calls to create slow effects
- Always call pixels.show() at the end of the function

**Example JSON Output for a smooth rainbow wave:**
{
  "function": "def light_func(pixels):\\n    if not hasattr(light_func, 'step'):\\n        light_func.step = 0\\n    num_pixels = len(pixels)\\n    for i in range(num_pixels):\\n        # Create smooth rainbow colors\\n        hue = (i + light_func.step) % 255\\n        # Convert hue to RGB (simplified conversion)\\n        pos = hue / 255.0\\n        if pos < 0.33:\\n            r = int(255 * (1 - pos * 3))\\n            g = int(255 * pos * 3)\\n            b = 0\\n        elif pos < 0.67:\\n            pos = pos - 0.33\\n            r = 0\\n            g = int(255 * (1 - pos * 3))\\n            b = int(255 * pos * 3)\\n        else:\\n            pos = pos - 0.67\\n            r = int(255 * pos * 3)\\n            g = 0\\n            b = int(255 * (1 - pos * 3))\\n        pixels[i] = (r, g, b)\\n    pixels.show()\\n    light_func.step = (light_func.step + 1) % 255"
}

**Example JSON Output for slow blinking between colors:**
{
  "function": "def light_func(pixels):\\n    if not hasattr(light_func, 'step'):\\n        light_func.step = 0\\n    # Toggle every 25 frames for slow blinking\\n    color = (255, 0, 0) if light_func.step // 25 % 2 == 0 else (0, 0, 255)\\n    pixels.fill(color)\\n    pixels.show()\\n    light_func.step += 1"
}
"""

prompt = "Create a rainbow effect that moves across the strip"  # Default prompt

def generate_and_run_effect(new_prompt=None):
    global prompt, light_func
    if new_prompt:
        prompt = new_prompt

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {
                "role": "system",
                "content": role
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500
    )

    response_content = response.choices[0].message.content
    logging.info("\n=== Generated LED Effect Function ===")
    logging.info(f"Prompt: {prompt}")
    logging.info("Function code:")
    ai_data = json.loads(response_content)
    logging.info(ai_data["function"])
    logging.info("===================================\n")
    exec(ai_data["function"], globals())  # Execute in global scope to make light_func available
    return light_func

def main():
    try:
        effect_func = generate_and_run_effect()
        while True:
            effect_func(pixels)
    except KeyboardInterrupt:
        pixels.fill((0, 0, 0))
        pixels.show()

if __name__ == "__main__":
    main()
