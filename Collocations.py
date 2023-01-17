import numpy as np
import string
import math
import sys

def chi_square(N, bigram_count, sum_of_w1, sum_of_w2):
    o_val=[]
    e_val=[]
    chi_square=0

    #observed and Expected values

    O_11 = bigram_count
    O_12 = sum_of_w2 - bigram_count
    O_21 = sum_of_w1 - bigram_count
    O_22 = N - (sum_of_w1 + sum_of_w2 - bigram_count)

    o_val.extend([O_11, O_12, O_21, O_22])

    E_11 = sum_of_w1 * sum_of_w2 / N
    E_12 = (N - sum_of_w1) * sum_of_w2 / N
    E_21 = (N - sum_of_w2) * sum_of_w1 / N
    E_22 = (N - sum_of_w1) * (N - sum_of_w2) / N   

    e_val.extend([E_11, E_12, E_21, E_22])

    for i in range(4):
        individual_value =  ((o_val[i] - e_val[i])**2)/e_val[i]   
        chi_square += individual_value
    return chi_square

def chi_square_vals(bigram_corpus,unigram_corpus, count_as_w1, count_as_w2):
    #Chi_square
    chi_square_values={}
    N = sum(bigram_corpus.values())
    for each_bigram in bigram_corpus:

        #Variables        
        word_1 = each_bigram[0]
        word_2 = each_bigram[1]
        bigram_count = bigram_corpus[(word_1,word_2)]
        sum_of_w1 = count_as_w1[word_1]
        sum_of_w2 = count_as_w2[word_2]        
        cal_chi_sq_val = chi_square(N, bigram_count, sum_of_w1, sum_of_w2)
        chi_square_values[each_bigram] = cal_chi_sq_val
        
    # sorted Chi_square
    chi_square_values_list = sorted(chi_square_values.items(), key=lambda x:x[1] , reverse=True)
    sortdict_chi_sq = dict(chi_square_values_list)
    count1=0
    for k,v in sortdict_chi_sq.items():    
        if(count1==20):
            break
        print(k,v)
        count1+=1
    
    
def pmi_vals(bigram_corpus,unigram_corpus):
    
    pmi_values={}
    M = sum(unigram_corpus.values())
    for each_bigram in bigram_corpus:

        #Variables
        word_1 = each_bigram[0]
        word_2 = each_bigram[1]
        bigram_count = bigram_corpus[(word_1,word_2)]
        count_of_w1 = unigram_corpus[word_1]
        count_of_w2 = unigram_corpus[word_2]
        cal_pmi_val =  math.log((bigram_count * M)/(count_of_w1*count_of_w2))
        pmi_values[each_bigram] = cal_pmi_val
    #sorted PMI
    pmi_values_list = sorted(pmi_values.items(), key=lambda x:x[1] , reverse=True)
    sortdict_pmi = dict(pmi_values_list)
    count2=0
    for k,v in sortdict_pmi.items():

        if(count2==20):
            break
        print(k,v)
        count2+=1


if __name__ == "__main__":
    
    arguments = sys.argv  
    input_file = str(arguments[1])
    input_metric = str(arguments[2])
    file=open(input_file,"r")
    lines = file.readlines()

    #dictionary of unigrams and bigram
    unigram_corpus={}     
    bigram_corpus={}

    #dictionary of counts in bigrams
    count_as_w1={}     
    count_as_w2={}

    symbols=string.punctuation

    for line in lines:
        input_line = list(line.strip().split(' '))
        for each_word in range (len(input_line)-1):
            input_line[each_word]=input_line[each_word].lower()

        for current_index in range (len(input_line)):
            current_word= input_line[current_index]

            if current_word in symbols:
                continue

            #forming dictionary of unigrams and their frequency            
            if (current_word not in unigram_corpus):
                unigram_corpus[current_word] =1
            else:
                unigram_corpus[current_word]+=1


            #forming dictionary of bigrams and their frequency
            if current_index+1 >=  len(input_line):
                continue

            next_word_index = current_index+1
            next_word = input_line[next_word_index] 

            while(next_word in symbols) and (next_word_index +1 < len(input_line)):
                next_word_index += 1
                next_word = input_line[next_word_index] 

            if next_word in symbols:
                continue

            if ((current_word,next_word) not in bigram_corpus):
                bigram_corpus[(current_word,next_word)]=1

                #count of each word of bigram as w1 and w2
                if(current_word in count_as_w1):
                    count_as_w1[current_word] += 1
                else:
                    count_as_w1[current_word]= 1

                if(next_word in count_as_w2):
                    count_as_w2[next_word] += 1
                else:
                    count_as_w2[next_word]=1

            else:
                bigram_corpus[(current_word,next_word)]+=1

                #count of each word of bigram as w1 and w2
                if(current_word in count_as_w1):
                    count_as_w1[current_word] += 1
                else:
                    count_as_w1[current_word]= 1

                if(next_word in count_as_w2):
                    count_as_w2[next_word] += 1
                else:
                    count_as_w2[next_word]=1

    file.close()
#     print(bigram_corpus)
    if(input_metric == "chi-square"):
        chi_square_vals(bigram_corpus,unigram_corpus, count_as_w1, count_as_w2)     
    elif(input_metric == "PMI"):
        pmi_vals(bigram_corpus,unigram_corpus)
    else:
        print("invalid metric")
    
