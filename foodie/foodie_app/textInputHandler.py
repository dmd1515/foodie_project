# foodie/foodie_app/textInputHandler.py
def processTextInput(user_input):
    """Funkcija, kurią testuoja jūsų testai"""
    stripped_input = user_input.strip()
    if not stripped_input:
        return "Error: input is empty"
    return f"You entered: {stripped_input}"