import random
import pandas as pd
import shutil
import os, shutil
from stringDatabase import stringDatabase
from game import Game_class


def remove_files(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def get_latest(folder):
    a=[]
    for the_file in os.listdir(folder):
        a.append(int(the_file[:1]))
        fin=str(max(a))
    return fin

def get_score(g,l):
    if (len(g)+len(l)>0):
        k = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        v = [8.17,1.49,2.78,4.25,12.7,2.23,2.02,6.09,6.97,0.15,0.77,4.03,2.41,6.75,7.51,1.93,0.10,5.99,6.33,9.06,2.76,0.98,2.36,0.15,1.97,0.07]
        data=pd.DataFrame({'word':k,
                'value':v})
        
        l['Status_letter']='Gave up'
        l.loc[(l['Letters_guessed']==l['Word']),'Status_letter']='Success'
        g['Status_guess']='Gave up'
        g.loc[(g['Correct Guess']==1),'Status_guess']='Success'
        d=g.merge(l, how='outer', on=['Game','Word'])
        d['Status']='Gave up'
        d.loc[(d['Status_guess']=='Success'),'Status']='Success'
        d.loc[(d['Status_letter']=='Success'),'Status']='Success'
        d['Correct Guess']=d['Correct Guess'].fillna(0)
        d['rank']=d.groupby('Game')['Correct Guess'].rank(ascending=0,method='dense')
        d1=d[d['rank']==1].drop_duplicates()
        d1['total_letters']=d1['Missed_letters']+d1['Correct_attempt']
        d1['status_score']=-1
        d1.loc[(d1['Status_guess']=='Success'),'status_score']=1
        d1[['Letters_guessed']]=d1[['Letters_guessed']].fillna('0')
        d1=d1.fillna(0)
        d1['letters_not_guess']=None
        for i, row in d1.iterrows():
            d1['letters_not_guess'][i]=([x for x in row['Word'] if x not in row['Letters_guessed']])
        
        chunk_out = d1.set_index('Letters_guessed')['letters_not_guess'].apply(pd.Series).stack().reset_index().rename(columns={0:'unguessed'}).drop('level_1',axis=1)
        d2=d1.merge(chunk_out,how='left',on='Letters_guessed')
        d3=d2.merge(data,left_on='unguessed',right_on='word')
        
        dout=d3[['Game','Word','Status','Bad Guess','Missed_letters','value','Correct_attempt','Correct Guess']]
        
        dout_f=dout.groupby(['Game','Word','Status','Bad Guess','Missed_letters','Correct_attempt','Correct Guess'])['value'].sum().reset_index()
        dout_f['Score']=0
        
        dout_f_suc=dout_f[dout_f['Status']=='Success']
        dout_f_fail=dout_f[dout_f['Status']=='Gave up']
        dout_f_suc['Score']=(dout_f_suc['value']/(dout_f_suc['Correct_attempt']+dout_f_suc['Missed_letters']+dout_f_suc['Correct Guess']))-(0.1*dout_f_suc['Bad Guess']*(dout_f_suc['value']/(dout_f_suc['Correct_attempt']+dout_f_suc['Missed_letters']+dout_f_suc['Correct Guess'])))
        dout_f_fail['Score']=dout_f_fail['value']*-1
        
        dout_final=dout_f_suc.append(dout_f_fail,sort=True).dropna()
        dout_final_table=dout_final[['Game','Word','Status','Bad Guess','Missed_letters','Score']]

        print ('Printing Scores table:')

        print (dout_final_table)
        final_score=sum(dout_final.Score)
        print ('Final Score:'+str(final_score))
    else:
        final_score=0
        print ('Final Score:'+str(final_score))
    
    
class Guess(object):  
    def __init__(self):
        pass
        
    def guess_menu(self):
        print("The great word guessing game")
        print("Current Guess : ---- ")
        print("g = guess, t = tell me, l for a letter, and q to quit")
        option = input ("Enter the option :") 
        
        if option not in('g','q','t','l'):
            print("please select the correct option")
            option = input ("Enter the option :")         
        return option

    def game_start(self,Game,df,out_df_l,out_df_g):
        Game=Game+1
        words=stringDatabase().get_file()
        current_word= random.choice(words)
        self.current_word=current_word
        self.df=df
        self.out_df_l=out_df_l
        self.out_df_g=out_df_g
        #To be commented on sbmission
        print(self.current_word)
        
        option=Guess().guess_menu()
        
        self.letters_guessed = []
        self.failed_attempt=0
        self.correct_attempt=0
        self.failed_guess=0
        self.correct_guess=0
        self.score=0
        
        if(option == 'g'):
            self.Game,self.correct_guess,self.failed_guess,self.out_df_l,self.out_df_g,self.option=Game_class().game_g(self.current_word,self.letters_guessed,self.failed_attempt,self.correct_attempt,self.failed_guess,self.correct_guess,Game,df,self.out_df_l,self.out_df_g)
            if self.option=='q':
                pass
            else:    
                Guess().game_start(Game,self.df,self.out_df_l,self.out_df_g)
        elif(option=='l'):
            self.Game,self.correct_attempt,self.failed_attempt,self.letters_guessed,self.out_df_l,self.out_df_g,self.option=Game_class().game_l(self.current_word,self.letters_guessed,self.failed_attempt,self.correct_attempt,self.failed_guess,self.correct_guess,Game,df,self.out_df_l,self.out_df_g)
            if self.option=='q':
                pass
            else:    
                Guess().game_start(Game,self.df,self.out_df_l,self.out_df_g)
        elif(option=='t'):
            print("The Correct Word is")
            print (self.current_word)
            
            Guess().game_start(Game,self.df,self.out_df_l,self.out_df_g)
            pass
        
        elif(option=='q'):
            pass
        else:
            pass        

        self.out_df_l.to_csv('l/'+str(Game)+'.csv')
        self.out_df_g.to_csv('g/'+str(Game)+'.csv')
        
        final_g=pd.read_csv('g/'+get_latest('g')+'.csv')
        final_l=pd.read_csv('l/'+get_latest('l')+'.csv')
        
        return final_g,final_l
        
    
    def run(self):
        try:
            os.mkdir('l')
        except:
            pass
        
        try:
            os.mkdir('g')
        except:
            pass
        
        remove_files('l')
        remove_files('g')
        Game=0
        df=pd.DataFrame()
        self.out_df_l=pd.DataFrame(columns={'Correct_attempt','Game','Word','Letters_guessed','Missed_letters'})
        self.out_df_g=pd.DataFrame(columns={'Bad Guess','Correct Guess','Game','Word'})
        
        g,l=self.game_start(Game,df,self.out_df_l,self.out_df_g)
        get_score(g,l)


Guess().run()