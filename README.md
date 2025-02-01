# AI LED Strip Controller

A web-based LED strip controller that uses AI to generate dynamic lighting effects from natural language descriptions. Built for Raspberry Pi and WS2812B LED strips.

## Features

- 🎨 Natural Language Control: Describe any lighting effect you want
- 🌈 Predefined Effects:
  - `snake`: Snake game simulation
  - `police`: Emergency vehicle lighting
  - `rainbow`: Moving rainbow pattern
  - `fire`: Flickering flame effect
  - `ocean`: Calming ocean waves
- 📱 Mobile-Friendly Web Interface
- ⚡ Real-time Effect Generation
- 🛑 Emergency Kill Switch
- 🔄 Dynamic Effect Support
- ⚠️ Comprehensive Error Handling

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- WS2812B LED Strip
- 5V Power Supply (sized appropriately for your LED strip)
- Level Shifter (recommended for reliable signal)

## Software Requirements

- Python 3.7+
- pip3
- OpenAI API Key

## Installation

1. Clone the repository:
   ```bash
   git clone [your-repo-url]
   cd ai_led_strip
   ```

2. Install required packages:
   ```bash
   pip3 install flask openai adafruit-circuitpython-neopixel
   ```

3. Configure your OpenAI API key in ai_led.py:
   ```python
   api_key = "your-api-key-here"
   ```

4. Configure your LED strip in ai_led.py:
   ```python
   LED_PIN = board.D18  # GPIO pin number
   LED_COUNT = 143      # Number of LEDs in your strip
   ```

## Port Configuration

The default port (5000) can be changed to any available port on your system. To use a different port:

1. Modify app.py:
   ```python
   app.run(host='0.0.0.0', port=YOUR_PORT, debug=False)
   ```

2. Common port choices:
   - 5000: Flask default
   - 8080: Common alternative
   - 3000: Another popular choice
   
Note: Avoid ports below 1024 (they require root privileges) and check that your chosen port isn't already in use.

To check if a port is available:
```bash
sudo lsof -i :PORT_NUMBER
```

## Usage

1. Start the server (requires sudo for GPIO access):
   ```bash
   sudo $(which python3) python3 app.py
   ```
    `which python` is necessary since sudo run as admin it does not know the specific environment

2. Access the web interface:
   - If on the same network: http://raspberrypi.local:PORT
   - Or use the IP address: http://YOUR_PI_IP:PORT
   (Replace PORT with your configured port number, default is 5000)

3. Control Methods:
   - Use predefined effects by typing keywords (snake, police, rainbow, fire, ocean)
   - Or describe any custom effect you want
   - Use the Kill button to stop any effect

## Project Structure

- `app.py`: Flask web server and thread management
- `ai_led.py`: Core LED control and OpenAI integration
- `prompts.py`: Predefined effect descriptions
- `templates/index.html`: Web interface

## Error Handling

The system provides detailed feedback for various issues:

1. API Related:
   - Rate limiting
   - Connection issues
   - Timeouts
   - Service availability

2. Hardware Related:
   - GPIO access errors
   - LED strip bounds
   - Invalid color values

3. Runtime Errors:
   - Memory issues
   - Invalid effect patterns
   - Thread management

## Troubleshooting

1. Permission Denied:
   - Make sure to run with sudo: `sudo python3 app.py`

2. Can't Access Web Interface:
   - Check your network connection
   - Verify the Raspberry Pi's IP address
   - Ensure your chosen port is not blocked
   - Try a different port if needed

3. LED Effects Not Working:
   - Verify LED strip connections
   - Check power supply
   - Ensure correct GPIO pin configuration

4. Effect Freezes:
   - Use the Kill button to stop the effect
   - Restart the server if needed

## Network Access

To ensure reliable access to the web interface:

1. Find your Pi's IP:
   ```bash
   hostname -I
   ```

2. Options for consistent access:
   - Set up a static IP in /etc/dhcpcd.conf
   - Use hostname: raspberrypi.local
   - Create a bookmark once you find a working address

## Safety Notes

1. Power Supply:
   - Use an adequate power supply for your LED count
   - Calculate: LEDs × 60mA = Minimum power supply current

2. Data Signal:
   - Use a level shifter for reliable operation
   - Keep data wires short to minimize interference

3. Software:
   - Don't modify running effects
   - Use Kill button before shutdown
   - Always run with sudo for proper GPIO access

## Contributing

Feel free to submit issues and enhancement requests!

## License

Apache 2.0

## Credits

- OpenAI GPT-4 for effect generation
- Flask for web framework
- Adafruit for NeoPixel library
