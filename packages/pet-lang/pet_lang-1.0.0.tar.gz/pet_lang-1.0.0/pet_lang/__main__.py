from .pet_lang import PetLang

if __name__ == "__main__":
    AQI = PetLang({}, "")
    answer = AQI.ask_question("How old are you?", "uint")
    ADD_S = ""
    if answer > 1:
        ADD_S = "s"
    print(f"You are {answer} year{ADD_S} old")
    answer = AQI.ask_question("Enter a ufloat:", "ufloat")
    print(f"You entered {answer}")
    AQI.pause()
