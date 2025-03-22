#Quiz game, keeping track of scores and such. 
import random



options = ["rock", "paper", "scissors", "x"]
enemy_options = ["rock", "paper", "scissors"]





def enemy_choice(enemy_options):
    return random.choice(enemy_options)


def player_choice(options):
    svar = input("Rock, paper, scissors? Or X to stop: ").lower().strip()
    if svar not in options:
        print("Please answer correctly.")
        return player_choice(options)
    return svar


def check(options, score):
    player_answer = player_choice(options)
    enemy_answer = enemy_choice(enemy_options)
    if player_answer == "x":
        return score, False
    else:

        print(f"You chose {player_answer} and enemy chose {enemy_answer}")
        if player_answer == "rock" and enemy_answer == "scissors":
            score += 1 
            print(f"Correct! One point added good sir, score is {score}")
        elif player_answer == "scissors" and enemy_answer == "paper":
            score +=1
            print(f"Correct! One point added good sir, score is {score}")

        elif player_answer == "paper" and enemy_answer == "rock":
            score +=1
            print(f"Correct! One point added good sir, score is {score}")

        elif player_answer == enemy_answer:
            print("Same answer, no change in points")
        else:
            score -=1
            print(f"Wrong answer, you lose a point score is {score}")
        return score, True

    
        
    


def game():
    print("Welcome to the game")
    score = 0
    n = -1
    play = True
    while play:
        score, play = check(options, score)
        
    print(f"Thanks for playing, you got {score} which will be turned into {n*score} tickles")
    
        

        


game()


    


