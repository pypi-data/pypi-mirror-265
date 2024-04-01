import screeninfo
import asyncio

screen_width = screeninfo.get_monitors()[0].width
middle = " "*int(((screen_width/10)-128)/2)

def centre(title,symbol=" ",str_end="\n") :
    #aligns the title in centre with symbols around it
    gap = str(symbol)*(64-int((len(title)/2)))
    gap2 = str(symbol)*(128- len(title) - len(gap))
    if str_end != '\r' :
        print(( middle + "|" + gap + title + gap2 + "|" + "\n" + middle + "|" + 128*" " + "|"),end=str_end)
    else :
        print(( middle + "|" + gap + title + gap2 + "|"),end='\r')
    return screen_width, middle

def int_check(answer='') :
    answer = str(answer).strip()
    integer = -1
    while integer < 1 :
        try : 
            int(answer)
            integer = int(answer)
        except : 
            centre("Please enter a valid integer !")
            ques = "Enter a number -"
            string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
            answer = input(string) 
            continue
    return int(answer)

def format_input(ques='') : 
    string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
    output = input(string)
    return output

def ans_check(option_list=[]) :    

    #prints and detetcs the answers and returns the choose answer
    centre("-","-")
    for i in option_list : 
        centre(symbol=" ", title=(str(option_list.index(i) + 1) + ".) " + str(i)))
    centre("-","-")
    ques = "Choose a option"
    string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
    answer = input(string)
    answer = answer.strip()
    answer = int_check(answer)
    while int(answer) > len(option_list) :
            centre("Not a valid answer !")
            answer = format_input("Choose a option")
            try :
                int(answer) 
            except  :
                answer = int_check(answer)
        
    return option_list[int(answer) - 1]

async def redirect_function(redirect):
    for i in range(3,0,-1):
        title = f"Redirecting to {redirect} in {i}..."
        symbol = " "
        gap = str(symbol)*(64-int((len(title)/2)))
        gap2 = str(symbol)*(128- len(title) - len(gap))
        print(( middle + "|" + gap + title + gap2 + "|"),end='\r') 
        await asyncio.sleep(1) 

async def redirect(redirect='UNKNOWN'):
    await redirect_function(redirect)