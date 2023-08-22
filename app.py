import os
import random
# import asyncio
import streamlit as st
# import subprocess
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# Major Arcana cards data
major_arcana_data = {
    "The Fool": ["Beginning, spontaneity, faith", "Naivety, foolishness, recklessness"],
    "The Magician": ["Manifestation, resourcefulness", "Deceit, manipulation"],
    "The High Priestess": ["Intuition, unconscious knowledge", "Hidden agendas, need to listen more"],
    "The Empress": ["Motherhood, fertility", "Dependency, smothering"],
    "The Emperor": ["Authority, structure", "Domination, excessive control"],
    "The Hierophant": ["Tradition, spiritual guidance", "Rigidity, dogmatic"],
    "The Lovers": ["Union, partnership", "Disconnection, unaligned values"],
    "The Chariot": ["Willpower, success", "Lack of direction, aggression"],
    "Strength": ["Courage, patience", "Self-doubt, lack of self-discipline"],
    "The Hermit": ["Introspection, guidance", "Loneliness, isolation"],
    "Wheel of Fortune": ["Fate, destiny", "Bad luck, interruptions"],
    "Justice": ["Fairness, truth", "Unfairness, lack of accountability"],
    "The Hanged Man": ["Sacrifice, perspective", "Stalling, needless sacrifice"],
    "Death": ["Endings, transformation", "Resistance, avoiding change"],
    "Temperance": ["Balance, moderation", "Extremes, imbalance"],
    "The Devil": ["Bondage, materialism", "Breaking free, detachment"],
    "The Tower": ["Upheaval, revelation", "Avoiding disaster, fear of change"],
    "The Star": ["Hope, inspiration", "Despair, lack of faith"],
    "The Moon": ["Intuition, dreams", "Deception, confusion"],
    "The Sun": ["Joy, success", "Negativity, depression"],
    "Judgement": ["Evaluation, reflection", "Denial, self-doubt"],
    "The World": ["Completion, accomplishment", "Incompleteness, lack of closure"]
}

# Minor Arcana cards data
suits = ["Cups", "Pentacles", "Swords", "Wands"]
minor_descriptions = {
    "Ace": ["New beginnings, opportunity", "Missed opportunities, lack of potential"],
    "Two": ["Balance, duality", "Imbalance, conflict"],
    "Three": ["Collaboration, initial fulfillment", "Lack of teamwork, misalignment"],
    "Four": ["Stability, foundation", "Instability, lack of appreciation"],
    "Five": ["Conflict, loss", "Reconciliation, recovery"],
    "Six": ["Reciprocity, harmony", "Egoism, jealousy"],
    "Seven": ["Reflection, assessment", "Lack of vision, limited success"],
    "Eight": ["Mastery, moving forward", "Confusion, fear of change"],
    "Nine": ["Contentment, nearing completion", "Lack of perspective, hesitation"],
    "Ten": ["Completion, accomplishment", "Resistance, delay"],
    "Page": ["New inspiration, discovery", "Lack of direction, immaturity"],
    "Knight": ["Action, energy", "Haste, undirected energy"],
    "Queen": ["Compassion, calmness", "Dependency, lack of emotional control"],
    "King": ["Authority, honor", "Stubbornness, emotional manipulation"]
}

minor_arcana_data = {}
for suit in suits:
    for card, meanings in minor_descriptions.items():
        name = f"{card} of {suit}"
        minor_arcana_data[name] = meanings


class TarotCard:
    def __init__(self, name, meanings):
        self.name = name
        self.meaning = meanings[0]
        self.reversed_meaning = meanings[1]
        self.is_reversed = False

    def reverse(self):
        self.is_reversed = not self.is_reversed

    def __str__(self):
        return self.name + (" (Reversed)" if self.is_reversed else "")


def shuffle_deck(deck):
    random.shuffle(deck)
    return deck


def draw_cards(deck, num=3):
    cards = [deck.pop() for _ in range(num)]
    for card in cards:
        if random.choice([True, False]):
            card.reverse()
    return cards


def tarot_reading(deck, num=3):
    shuffled_deck = shuffle_deck(deck)
    cards_drawn = draw_cards(shuffled_deck, num)
    reading_results = []

    for card in cards_drawn:
        card_name = str(card)
        card_meaning = card.reversed_meaning if card.is_reversed else card.meaning
        reading_results.append((card_name, card_meaning))

    return reading_results


# Convert data dictionaries to lists of TarotCard objects
major_arcana = [TarotCard(name, meanings)
                for name, meanings in major_arcana_data.items()]
minor_arcana = [TarotCard(name, meanings)
                for name, meanings in minor_arcana_data.items()]
full_deck = major_arcana + minor_arcana

# Example usage
# results = tarot_reading(full_deck, 5)
# for card_name, card_meaning in results:
#     print(f"Card: {card_name}\nMeaning: {card_meaning}\n")
# read_topic = input("What would you like a reading for?\nI would like a reading for:\n")
# number = input("How many cards would you like to draw?\nI would like to draw:\n")
# print(f"Reading for:\n{read_topic}\n")
# for card_name, card_meaning in pull:
#     print(f"Card: {card_name}\nMeaning: {card_meaning}\n")
# result = completion.choices[0].message
# print(result.content)

SYSTEM_MESSAGE = """
You are an expert tarot reader, the user will provide you with what they would like a reading for on the first line, and on the third line they will provide what card or cards they pulled.
You will respond with a reading based off of the pull, using your vast experience with tarot.

Don't introduce yourself or explain what you are doing, just start the reading.

Format your response as a python dict, and use the following format for the reading:
Topic: {read_topic, reworded}
Pull: {the card or cards pulled, each formatted with emojis that reflect card}
NoteA: {emojis matching the meaning of the card or each of the cards pulled}
NoteB: {meaning of the card or each of the cards pulled, formatted based on the number of cards pulled}
Reading: {reading}
Insights: {insights}
"""
# SYSTEM_MESSAGE = """
# You are an expert tarot reader, the user will provide you with what they would like a reading for on the first line, and on the third line they will provide what card or cards they pulled.
# You will respond with a reading based off of the pull, using your vast experience with tarot.

# Don't introduce yourself or explain what you are doing, just start the reading.

# Format your response in markdown, and use the following format for the reading:
# # {read_topic, reworded}
# ## Your pull:
# {the card or cards pulled, each formatted with emojis that reflect card}
# > {emojis matching the meaning of the card or each of the cards pulled}

# > {meaning of the card or each of the cards pulled, formatted based on the number of cards pulled}
# ### Reading:
# {reading}
# ### Insights:
# {insights}
# """
SPLASHES = [
    "Shuffling the deck for you...",
    "Connecting with the cosmos...",
    "Divining insights...",
    "Dealing the cards of fate...",
    "Aligning stars and cards...",
    "Seek and you shall find...",
    "The universe is whispering...",
    "Drawing from ancient wisdom...",
    "Reading the energies around you...",
    "Unveiling the mysteries...",
    "Seeking guidance from the cards...",
    "Your path is unfolding...",
    "Consulting the oracles...",
    "Looking beyond the veil...",
    "Guidance awaits...",
    "Revealing your cosmic story...",
    "Fate is in the cards...",
    "The cards speak truths...",
    "Delving into the unknown...",
    "Your journey begins here...",
    "Uncovering the arcane...",
    "What will the cards reveal?",
    "Peering into your destiny...",
    "Embrace the revelations...",
    "Synchronicities at play...",
    "The universe has a message for you...",
    "Finding your cosmic alignment...",
    "Tarot's wisdom, just for you...",
    "Discovering paths untrodden...",
    "Gathering celestial insights..."
]

st.set_page_config(
    page_title="Tarot Reading",
    page_icon=":crystal_ball:",
    layout="centered"
    # menu_items={
    #     "about": "https://twitter.com/StreamlitApp"
    #     }
)

with st.form("tarot"):
    st.title(':crystal_ball: Tarot Reading :crystal_ball:')
    read_topic = st.text_area('What would you like a reading for?')
    number = st.number_input('How many cards would you like to draw?', min_value=1, max_value=10)
    submit = st.form_submit_button('Submit')
    

if submit:
    pull = tarot_reading(full_deck, int(number))

    with st.spinner(random.choice(SPLASHES)):
        st.toast('Pulling your cards...')
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": f"{read_topic}\n\n{pull}"}
            ]
        )
        st.toast('Ready to read!')
    result = completion.choices[0].message['content']
    # st.code(result)
    ob = eval(result)
    out = f"# {ob['Topic']}\n## You drew:\n{ob['Pull']}\n> {ob['NoteA']}\n> {ob['NoteB']}\n### Reading:\n{ob['Reading']}\n### Insights:\n{ob['Insights']}"
    out
