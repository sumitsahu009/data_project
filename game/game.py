import pandas as pd

class Game_class():  
    def __init__(self):
        pass
        
    def game_g(self,current_word,letters_guessed,failed_attempt,correct_attempt,failed_guess,correct_guess,Game,df,out_df_l,out_df_g):
        self.Game=Game
        self.correct_guess=correct_guess
        self.failed_guess=failed_guess
        self.df=df
        self.da1=pd.DataFrame()
        noOfTries=0
        self.out_df_l=out_df_l
        self.out_df_g=out_df_g
        self.option='g'
        while noOfTries <= 100:
            guess = input ("Enter the guessed word :") 
            print ('current_word:'+current_word)
            noOfTries += 1
                
            if guess == current_word:
                self.correct_guess=self.correct_guess+1
                self.status="Success"
                print("You guessed the correct word!")
                print ('correct_guess:'+str(self.correct_guess))
                break
                
            elif guess != current_word: 
                print("Sorry, that wild guess is not correct")
                self.failed_guess=self.failed_guess+1
                print ('failed_guess:'+str(self.failed_guess))
                
                option=self.guess_menu()
                if option=='l':
                    self.Game,self.correct_attempt,self.failed_attempt,self.letters_guessed,self.out_df_l,self.out_df_g,self.option=Game_class().game_l(current_word,letters_guessed,failed_attempt,correct_attempt,self.failed_guess,self.correct_guess,Game,self.df,self.out_df_l,self.out_df_g)                    
                    break
                if option=='t':
                    print("The Correct Word is")
                    print (current_word)
                    self.option='t'
                    break
                if option=='q':
                    print ('here')
                    self.option='q'
                    break
                else:
                    pass

        out_df_g=pd.DataFrame({'Game':self.Game,'Word':current_word,
                         'Correct Guess':self.correct_guess, 'Bad Guess':self.failed_guess}, index=[0])

        self.out_df_g=self.out_df_g.append(out_df_g,sort=True)
        
        return self.Game,self.correct_guess,self.failed_guess,self.out_df_l,self.out_df_g,self.option
          

    def game_l(self,current_word,letters_guessed,failed_attempt,correct_attempt,failed_guess,correct_guess,Game,df,out_df_l,out_df_g):
        self.letters_guessed=letters_guessed
        self.failed_attempt=failed_attempt
        self.correct_attempt=correct_attempt
        self.Game=Game
        self.df=df
        self.out_df_l=out_df_l
        self.out_df_g=out_df_g
        self.correct_guess=correct_guess
        self.option='l'
        word_length = len(current_word)
        guess = ' _ ' * word_length
        while True:
            guess_letter = input ("Please guess a letter: ")
            if len(guess_letter) != 1:
                print ("Please guess one letter at a time")
            if guess_letter in self.letters_guessed:
                print ("\n You already guessed that letter, please try again")
                
            if guess_letter not in current_word:
                    print("Hey  try again this letter is incorrect  , You can do it , Give It one more Shot")
                    self.failed_attempt += 1
            else: 
                self.letters_guessed += guess_letter
                if guess_letter in current_word:
                    self.correct_attempt+=1
                    you_have = ''.join(x if x in self.letters_guessed else ' _ ' for x in current_word)
                    print ("So far you have guseed thse letters in the words: ", you_have)
                    
                if you_have == current_word:
                    self.correct_guess+=1
                    print("Hurray!You guessed the correct word")
                    self.Game=self.Game+1
                    break

            print ('letters_guessed: ')
            print (self.letters_guessed)
            print("length of letters guessed")
            print(len(letters_guessed))
            print ('failed_attempts:'+str(self.failed_attempt))
            print ('correct_attempts:'+str(self.correct_attempt))
            
            option=self.guess_menu()
            if option=='g':
                self.Game,self.correct_guess,self.failed_guess,self.out_df_l,self.out_df_g,self.option=self.game_g(current_word,self.letters_guessed,self.failed_attempt,self.correct_attempt,failed_guess,correct_guess,self.Game,self.df,self.out_df_l,self.out_df_g)
                break
            if option=='t':
                print("The Correct Word is ")
                print (current_word)
                self.option='t'
                break
            if option=='q':
                self.option='q'
                break
            else:
                pass
                
        print('failed_attempt:'+str(self.failed_attempt))
        print('correct_attempt:'+str(self.correct_attempt))
        
        letters_guessed_t=''.join(x if x in self.letters_guessed else '' for x in current_word)
        
        out_df_l=pd.DataFrame({'Game':self.Game,'Word':current_word,'Correct_attempt':self.correct_attempt,
                             'Missed_letters':self.failed_attempt,'Letters_guessed':letters_guessed_t}, index=[0])
        self.out_df_l=self.out_df_l.append(out_df_l,sort=True)

        return self.Game,self.correct_attempt,self.failed_attempt,self.letters_guessed,self.out_df_l,self.out_df_g,self.option
     

    def guess_menu(self):
        print("The great word guessing game")
        print("Current Guess : ---- ")
        print("g = guess, t = tell me, l for a letter, and q to quit")
        option = input ("Enter the option :") 
        
        if option not in('g','q','t','l'):
            print("please select the correct option")
            option = input ("Enter the option :")         
        return option