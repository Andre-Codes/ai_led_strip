# Dictionary of predefined prompts with their keywords
PREDEFINED_PROMPTS = {
    "snake": """
simulate the snake game using a loop where a segment of 
lights slowly moves back and forth and 'eats' a single led and the 
segment grows and moves along. Remember this is all on a single led strip with only 2 dimensions, back and forth.
The 'apple' led can appear anywhere on the strip.
Do not use any game libraries.

Include any import statements of built-in libraries needed for the function to work.
""",
    
    "police": """
Create a first responder car light effect where the LEDs alternate between red and blue,
with a smooth transition and realistic lighting pattern.
Make it dynamic with varying intensities and speeds.

IMPORTANT: Do not use time.sleep() or any blocking operations. Instead, use a phase
variable that changes each time the function is called to create the alternating pattern.
The function should complete quickly and return control to the caller.
""",
    
    "rainbow": """
Create a smooth rainbow effect that moves across the LED strip.
Use the full RGB spectrum with gentle transitions between colors.
The pattern should slowly shift along the strip creating a flowing rainbow effect.
Include subtle variations in brightness to add depth to the animation.

IMPORTANT: Do not use time.sleep() or any blocking operations. Instead, use an offset
variable that changes each time the function is called to shift the colors.
The function should complete quickly and return control to the caller.
""",
    
    "fire": """
Create a realistic fire effect with flickering orange, red, and yellow LEDs.
Simulate the natural randomness and intensity variations of flames.
Include occasional bright flares and dimmer embers.
The effect should be dynamic and never exactly repeat.

IMPORTANT: Do not use time.sleep() or any blocking operations. Use random.random()
for intensity variations but avoid any blocking operations. The function should
complete quickly and return control to the caller.
""",
    
    "ocean": """
Create a calming ocean wave effect using blues and whites.
Simulate gentle waves moving across the strip with varying intensities.
Include occasional white caps and deeper blue undertones.
The movement should be smooth and natural like real ocean waves.

IMPORTANT: Do not use time.sleep() or any blocking operations. Instead, use a phase
variable that changes each time the function is called to create wave motion.
The function should complete quickly and return control to the caller.
"""
}

def get_matching_prompt(user_input):
    """
    Check if the user's input contains any keywords from predefined prompts.
    Returns the matching predefined prompt or the original input if no match found.
    """
    # Convert user input to lowercase for case-insensitive matching
    user_input_lower = user_input.lower()
    
    # Check each keyword
    for keyword, prompt in PREDEFINED_PROMPTS.items():
        if keyword in user_input_lower:
            print(f"Using pre-defined prompt for: {keyword}")
            return prompt
            
    # If no match found, return the original input
    print("Using custom prompt")
    return user_input
