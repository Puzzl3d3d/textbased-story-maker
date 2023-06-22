import json

with open("story.json", "r") as file:
    story = json.load(file)

previousChoice = None

class ChoiceFunctions:
    # Put all of your functions into here on each choice

    # For example, if choice A is a trigger for something
    # special to happen, you would do it like so:

    # Each function gets given a "previousChoice" if needed.

    def onChoiceA():
        # Code here!

        print("Special event triggered!", previousChoice)

def process_data(data):
    global previousChoice

    data_type = data.get("type", "context")
    prompt = data.get("prompt", "")

    print(prompt)

    if data_type == "choice":
        choices = data.get("choices", {})
        inputText = data.get("inputText", "Choose: ")

        for choice in choices:
            description = choices[choice]
            print(f"{choice}: {description}")
        
        while True:
            choice = input(inputText)

            if choices.get(choice, None): break

        previousChoice = choice
    elif data_type == "choiceExtend":
        if not previousChoice: return

        choiceData = data.get(previousChoice, None)

        if not choiceData: return

        if str(type(choiceData)) == "<class 'str'>":
            print(choiceData)
        else:
            function = choiceData.get("function", "(lambda *args: None)")
            response = choiceData.get("response", "")

            print(response)
            try:
                exec("ChoiceFunctions."+function+"()", {"choice": previousChoice, "ChoiceFunctions": ChoiceFunctions})
            except NameError:
                print(f"\033[93mWARNING: {function} does not exist!\033[0m")

for index in range(1, len(story)+1):
    process_data(story[str(index)])