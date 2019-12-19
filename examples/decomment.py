#coding=utf-8

# quote:  状态机处理删除注释问题
# 
class rmcmnt :
    ### members
    m_type = 'CPP'

    ### contructed function
    def __init__(self, type):
        m_type = type

    ### member function

    # remove code comments
    def removecomment(seft, strInput) :
        state = 0;
        strOutput = ''
        strRemoved = ''

        for c in strInput :
            if state == 0 and c == '/' :        # ex. [/]
                state = 1
            elif state == 1 and c == '*' :      # ex. [/*]
                state = 2
            elif state == 1 and c == '/' :      # ex. [//] [#]
                state = 4
            elif state == 1 :                   # ex. [<secure/_stdio.h> or 5/3]
                print('/')
                state = 0
            elif state == 3 and c == '*':       # ex. [/*he**]
                state = 3
            elif state == 2 and c == '*':       # ex. [/*he*]
                state = 3
            elif state == 2:                    # ex. [/*heh]
                state = 2
            elif state == 3 and c == '/':       # ex. [/*heh*/]
                state = 0
            elif state == 3:                    # ex. [/*heh*e]
                state = 2
            elif state == 4 and c == '\\':      # ex. [//hehe\]
                state = 9
            elif state == 9 and c == '\\':      # ex. [//hehe\\\\\]
                state = 9
            elif state == 9:                    # ex. [//hehe\<enter> or //hehe\a]
                state = 4
            elif state == 4 and c == '\n':      # ex. [//hehe<enter>]
                state = 0
            elif state == 0 and c == '\'':      # ex. [']
                state = 5
            elif state == 5 and c == '\\':      # ex. ['\]
                state = 6
            elif state == 6:                    # ex. ['\n or '\' or '\t etc.]
                state = 5
            elif state == 5 and c == '\'':      # ex. ['\n' or '\'' or '\t' ect.]
                state = 0
            elif state == 0 and c == '\"':      # ex. ["]
                state = 7
            elif state == 7 and c == '\\':      # ex. ["\]
                state = 8
            elif state == 8:                    # ex. ["\n or "\" or "\t ect.]
                state = 7
            elif state == 7 and c == '\"':      # ex. ["\n" or "\"" or "\t" ect.]
                state = 0
            ### new request
            #  []
            elif state == 0 and c == '[':       # ex. [[]
                state = 10
            elif state == 10 and c == ']':      # ex. []]
                state = 11
            # [[]]
            elif state == 10 and c == '[':      # ex. []]
                state = 12
            elif state == 12 and c == ']':      # ex. [[]
                state = 13
            elif state == 13 and c == ']':      # ex. [[]
                state = 14
            # remove character in []
            elif state == 10:                
                state = 10
            # remove character in [[]]
            elif state == 12:                
                state = 12
            elif state == 13:                
                state = 13
            # restore state
            elif state == 11:                
                state = 0
            elif state == 14:                
                state = 0
            
            elif state == 11 and c == ']':     
                state = 14
            elif state == 1 and c == ']':     
                state = 13
            elif state == 10:                
                state = 10
            elif state == 12:                
                state = 12
            elif state == 11:                
                state = 13
            elif state == 12:                
                state = 0
            elif state == 13:                
                state = 0
            # remove "=-1" in "int a = -1;"
            #elif state == 0 and c == '=':     
            #    state = 15
            elif state == 15 and c == ';':    
                state = 0

            if (state == 0 and c != '/') or state == 5 or\
                state == 6 or state == 7 or state == 8 :
                strOutput += c
            else:
                # removed chareters
                strRemoved += c

        return strOutput,strRemoved
