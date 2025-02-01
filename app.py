from flask import Flask, render_template, request, jsonify
import threading
import ai_led
import traceback
import time
from prompts import get_matching_prompt

app = Flask(__name__)

# Global variables to control the LED thread
led_thread = None
stop_thread = False

def run_led_effect():
    global stop_thread, last_error
    try:
        effect_func = ai_led.generate_and_run_effect()
        while not stop_thread:
            try:
                effect_func(ai_led.pixels)
                # Sleep for 50ms (20 FPS) for smooth animations
                time.sleep(0.05)
            except ValueError as e:
                error = f"Effect error: Invalid LED values - {str(e)}"
                print(error)
                app.last_error = error
                break
            except IndexError as e:
                error = "Effect error: LED strip index out of range. The effect tried to access non-existent LEDs."
                print(error)
                app.last_error = error
                break
            except TypeError as e:
                error = "Effect error: Invalid color values. The effect produced invalid LED colors."
                print(error)
                app.last_error = error
                break
            except MemoryError as e:
                error = "Effect error: Out of memory. The effect is using too much memory."
                print(error)
                app.last_error = error
                break
            except Exception as e:
                error = f"Effect error: Unexpected error in animation - {str(e)}"
                print(error)
                app.last_error = error
                break
    except Exception as e:
        error = f"Error in LED thread: {str(e)}"
        print(error)
        app.last_error = error
    finally:
        try:
            ai_led.pixels.fill((0, 0, 0))
            ai_led.pixels.show()
        except Exception as e:
            error = f"Error cleaning up LEDs: {str(e)}"
            print(error)
            app.last_error = error

def safe_stop_thread():
    global led_thread, stop_thread
    if led_thread and led_thread.is_alive():
        stop_thread = True
        try:
            # Wait up to 2 seconds for thread to stop
            led_thread.join(timeout=2)
            if led_thread.is_alive():
                print("Warning: LED thread did not stop gracefully")
        except Exception as e:
            print(f"Error stopping thread: {e}")

# Initialize last error storage
app.last_error = None

@app.route('/', methods=['GET', 'POST'])
def home():
    global led_thread, stop_thread
    
    if request.method == 'POST':
        try:
            user_input = request.form.get('prompt')
            new_prompt = get_matching_prompt(user_input)
            
            # Stop existing LED thread if running
            safe_stop_thread()
            
            # Reset thread control
            stop_thread = False
            
            try:
                # Generate new effect with the new prompt
                ai_led.generate_and_run_effect(new_prompt)
                
                # Start new LED thread
                led_thread = threading.Thread(target=run_led_effect)
                led_thread.start()
                
                return render_template('index.html', message="New effect applied!")
            except Exception as e:
                error_msg = str(e)
                if "Permission denied" in error_msg:
                    error_msg = "Error: LED control requires sudo privileges. Please run the server with sudo."
                elif "Invalid parameter" in error_msg:
                    error_msg = "Error: Failed to generate effect. Please try a different description."
                elif "Rate limit" in error_msg:
                    error_msg = "Error: Too many requests to AI service. Please wait a moment and try again."
                elif "Connection error" in error_msg:
                    error_msg = "Error: Failed to connect to AI service. Please check your internet connection."
                elif "Timeout" in error_msg:
                    error_msg = "Error: Request timed out. Please try again."
                elif "Bad gateway" in error_msg:
                    error_msg = "Error: AI service temporarily unavailable. Please try again in a few minutes."
                elif "function" not in error_msg and "json" in error_msg.lower():
                    error_msg = "Error: AI response was not in the correct format. Please try a different description."
                elif "memory" in error_msg.lower():
                    error_msg = "Error: Out of memory. Try a simpler effect."
                elif "index" in error_msg.lower() and "range" in error_msg.lower():
                    error_msg = "Error: LED strip index out of range. The effect tried to access LEDs beyond the strip length."
                elif "RuntimeError" in error_msg and "GPIO" in error_msg:
                    error_msg = "Error: GPIO access failed. Make sure no other process is controlling the LED strip."
                return render_template('index.html', message=error_msg), 500
                
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"Detailed error: {traceback.format_exc()}")
            return render_template('index.html', message=error_msg), 500
    
    # Check for any errors from the effect thread
    error_message = None
    if app.last_error:
        error_message = app.last_error
        app.last_error = None  # Clear the error
    return render_template('index.html', message=error_message)

@app.route('/kill', methods=['POST'])
def kill_effect():
    global led_thread, stop_thread
    try:
        safe_stop_thread()
        try:
            ai_led.pixels.fill((0, 0, 0))
            ai_led.pixels.show()
        except Exception as e:
            print(f"Error cleaning up LEDs: {e}")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    try:
        print("\nNOTE: LED control requires sudo privileges!")
        print("Please run with: sudo python3 app.py\n")
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        # Cleanup when the server stops
        safe_stop_thread()
        try:
            ai_led.pixels.fill((0, 0, 0))
            ai_led.pixels.show()
        except Exception as e:
            print(f"Error during final cleanup: {e}")
