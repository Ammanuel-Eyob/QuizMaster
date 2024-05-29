import random
import typer
import yaml
from InquirerPy import prompt
import time

app = typer.Typer()

def load_questions_from_yaml(file_path):
    with open(file_path, 'r') as file:
        questions_dict = yaml.safe_load(file)
    return questions_dict['questions']

def ask_question(question, options):
    question_prompt = {
        'type': 'list',
        'name': 'answer',
        'message': question,
        'choices': options
    }
    answer = prompt([question_prompt])
    return answer['answer']

def play_quiz(questions):
    num_questions = typer.prompt(
        "How many questions would you like to answer? (Choose 5, 10, 15, or 20): ",
        type=int)
    while num_questions not in [5, 10, 15, 20]:
        num_questions = typer.prompt(
            "Please choose a valid option (5, 10, 15, or 20): ", type=int)

    selected_questions = random.sample(questions,
                                       min(num_questions, len(questions)))
    score = 0

    for idx, q in enumerate(selected_questions, 1):
        print(f"\nQuestion {idx}:")
        time.sleep(0.5)  # Add delay to ensure terminal rendering
        answer = ask_question(q['question'], q['options'])
        if answer.startswith(q['answer']):
            score += 1

    print(f"\nQuiz Over! You scored {score} out of {len(selected_questions)}.")

@app.command()
def main():
    questions = load_questions_from_yaml('questions.yaml')
    while True:
        play_quiz(questions)
        play_again = typer.confirm("Do you want to play again?", default=True)
        if not play_again:
            print("Thank you for playing! Goodbye.")
            break

if __name__ == "__main__":
    app()
