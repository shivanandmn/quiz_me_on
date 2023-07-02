# import json
# from send_quiz import telegram_polling

# def main():
#     telegram_polling()

questions = [{'question_text': "What is Bayes' Theorem used for?",
              'options': ['Calculating probabilities of events based on prior knowledge',
                          'Solving linear equations', 'Measuring distances in geometry',
                          'Predicting stock market trends'],
              'correct_option_idx': [0, 3], 'explanation': "Bayes' Theorem is used to calculate probabilities of events based on prior knowledge or information."}, {
    'question_text': "Who developed Bayes' Theorem?",
    'options': ['Thomas Bayes', 'Isaac Newton', 'Albert Einstein', 'Leonhard Euler'],
    'correct_option_idx': [0], 'explanation': "Bayes' Theorem was developed by Thomas Bayes, an English statistician and Presbyterian minister, in the 18th century."}]
