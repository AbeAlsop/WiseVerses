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

testInput("How do you prepare for a intense Greek class?", "Preparation", "Chance favors the prepared mind.")

testInput("What if I'm really stupid?", "Self-respect", "Stupidity in its really oppressive form is traceable to a pretension to appear something different from what one is in fact...")

testInput("Which is more important, self worth or truth?", "Truth", "If you seek truth you will not seek victory by dishonorable means, and if you find truth you will become invincible.")

testInput("Should I become Catholic?", "Discernment", "In an age overloaded with information, we must wade through the ocean of data, discard what is misleading, manipulative, tempting and destructive, and reason properly about what remains.")

testInput("My family is planning to travel to Hawaii after Christmas.", "Journey", "The world is your ship and not your home.")

testInput("I will soon be 50 years old. When should I retire?", "Discernment", "In an age overloaded with information, we must wade through the ocean of data, discard what is misleading, manipulative, tempting and destructive, and reason properly about what remains.")

testInput("Life has become dull. I just want to be happy again.", "Renewal", "We do not lose heart. Though our outer nature is wasting away, our inner nature is being renewed every day...")

testInput("How can I make my wife happy?", "Love", "Husbands, love your wives, just as Christ loved the church and gave Himself up for her.")

testInput("The one thing that is missing in my life is happiness.", "Joy", "The grand essentials of happiness are: something to do, something to love, and something to hope for.")

testInput("Why are some employees unhappy with their raise?", "Contentment", "He who envies others does not obtain peace of mind. (Buddha) | Give me neither poverty nor riches, but give me only my daily bread. Otherwise I shall be full and deny you and say, 'Who is the Lord?', or I shall be poor and steal and profane the name of my God. (Proverbs 30:8)")

