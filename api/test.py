from openAI import get_virtue
from chat import Chatter

chat = Chatter()

def testInput(prompt, baseline_virtue, baseline_response):
    new_virtue = get_virtue(prompt)
    full_prompt = chat.append_virtue(prompt, new_virtue)
    new_pop_response = chat.quote_db.lookup_pop_quote(full_prompt)
    new_faith_response = chat.quote_db.lookup_faith_quote(full_prompt)
    print(f"Prompt: {prompt}")
    print(f"Previous virtue: {baseline_virtue}")
    print(f"Previous response: {baseline_response}")
    print(f"New virtue: {new_virtue}")
    print(f"New pop response with score {new_pop_response['score']}: {new_pop_response['metadata']['Quote']}")
    print(f"New faith response with score {new_faith_response['score']}: {new_faith_response['metadata']['Quote']}")
    print()

#same, enhanced by additional faith quote
testInput("How do you prepare for a intense Greek class?", "Preparation", "Chance favors the prepared mind.")

#Self-respect or self-awareness?
testInput("What if I'm really stupid?", "Self-respect", "If I am not for myself, who will be for me?")

#same, enhanced by additional faith quote
testInput("Which is more important, self worth or truth?", "Truth", "If you seek truth you will not seek victory by dishonorable means, and if you find truth you will become invincible.")

#same
testInput("Should I become Catholic?", "Discernment", "In an age overloaded with information, we must wade through the ocean of data, discard what is misleading, manipulative, tempting and destructive, and reason properly about what remains.")

#should be Journey or maybe Preparation, not Gratitude
testInput("My family is planning to travel to Hawaii after Christmas.", "Preparation", "I will prepare, and some day my chance will come.")

#same, enhanced by additional pop quote
testInput("I will soon be 50 years old. When should I retire?", "Discernment", "In an age overloaded with information, we must wade through the ocean of data, discard what is misleading, manipulative, tempting and destructive, and reason properly about what remains.")

#same, enhanced by additional pop quote
testInput("Life has become dull. I just want to be happy again.", "Renewal", "Create in me a clean heart, O God, and renew a right spirit within me.")

#should be Love
testInput("How can I make my wife happy?", "Compassion", "The more you care, the stronger you can be.")

#should be Joy (better result than deprecated Happiness)
testInput("The one thing that is missing in my life is happiness.", "Happiness", "Happiness is found in doing, not merely possessing.")

testInput("Why are some employees unhappy with their raise?", "Contentment", "He who envies others does not obtain peace of mind. (Buddha) | Give me neither poverty nor riches, but give me only my daily bread. Otherwise I shall be full and deny you and say, 'Who is the Lord?', or I shall be poor and steal and profane the name of my God. (Proverbs 30:8)")

