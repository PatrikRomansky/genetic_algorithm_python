import gc
import time
import random
import functools
import numpy as np 
import multiprocessing
import logger as logger
from progress.bar import Bar
import evolution_individual as ind
import evolution_objective as objective

Adaptive_shift = None
Adaptive_fit = None


file_fits = 'fits'
file_final = 'final'
file_generations = 'gen'

evolution_name = 'evolution'

NUMBER_FORMAT = ''

start_eva = None
init_time = None

# creates the individual (random permutation)
def create_ind(ind_len, height, width):
    return ind.Individual(ind_len, height= height, width= width)

# creates the population using the create individual function
def create_pop(pop_size, create_individual):
    return [create_individual() for i in range(pop_size)]

def fitness(ind, targetInd):
    return  1 / (1 + objective.objective(ind, targetInd.geneType))
    
# applies a list of genetic operators (functions with 1 argument - population) 
def mate(pop, operators):
  
    for o in operators: 
        pop = o(pop)
    return pop

def mutate(ind, number_of_mutations, fit):
    global Adaptive_shift
    global Adaptive_fit

    f = fit(ind)
    if Adaptive_shift > 2 and Adaptive_fit* 1.5 <= f:
        Adaptive_shift -= 5
        Adaptive_fit = f
    
        if Adaptive_shift < 2 :
            Adaptive_shift = 2


    x_man = ind.mutate(number_of_mutations, Adaptive_shift)
    return x_man
    
# applies the mutate function (implementing the mutation of a single individual)
# to the whole population with probability mut_pro b)
def mutation(pop, mutate, mut_prob, new_ind, map_fn):
    # TODO: Parallel
    
    # func_distance = functools.partial(mutate, ind = pop)
    # return list(map_fn(func_distance, range(new_ind)))
    return [mutate(pop) if random.random() < mut_prob else pop for _ in range(new_ind)]

# max selection
def selection(pop, parent, fitFunc):
    bi = max(pop, key=fitFunc)

    if fitFunc(ind= bi) > fitFunc(ind= parent):
        parent.modify(bi.modifications)

    return parent

# implements the evolutionary algorithm
# arguments:
#   pop_size  - the initial population
#   max_gen   - maximum number of generation
#   fitness   - fitness function (takes individual as argument and returns 
#               FitObjPair)
#   operators - list of genetic operators (functions with one arguments - 
#               population; returning a population)
#   mate_sel  - mating selection (funtion with three arguments - population, 
#               fitness values, number of individuals to select; returning the 
#               selected population)
#   map_fn    - function to use to map fitness evaluation over the whole 
#               population (default `map`)
#   log       - a utils.Log structure to log the evolution run
def evolutionary_algorithm(pop, max_gen, fitness, operators, mate_sel, *, map_fn= map, log= 1, term_condition= 1):
    
    global evolution_name
    # best individual(string representation) for each generation
    out_bi_gen = []
    # best objective for each generation
    out_fit_gen = []

    # pre-processed fitness

    f = fitness(ind = pop[0])
    global Adaptive_fit 
    Adaptive_fit = f


    # INIT TIME 
    global start_eva
    global init_time
    start_eva = time.time()
    init_time = start_eva - start_time

    count = 0

    for G in Bar('Evolution').iter(range(max_gen)):
        
        offspring = mate(pop[0], operators)
        pop[0] = mate_sel(pop= offspring, parent= pop[0])

        bi = pop[0] 
        
        fit_value = fitness(ind=bi)
        
        gen = str(G).zfill(NUMBER_FORMAT) 
        

        out_fit_gen.append(gen + ' : ' + str(fit_value))
        
        if G % log == 0 or G == max_gen-1:
            count += 1
            out_bi_gen.append(gen + '\n' + bi.ToString())

            
            if count == 1000:
                logger.log_data(data= out_fit_gen, file_name= file_fits)
                logger.log_data(data= out_bi_gen, file_name= file_generations)
                # best individual(string representation) for each generation
                out_bi_gen = []
                # best objective for each generation
                out_fit_gen = []
                
                count = 0 
         
        if fit_value >= 1:
            # add last Best ind
            out_bi_gen.append(gen + '\n' + bi.ToString())
            break
        
        
    return pop, out_bi_gen, out_fit_gen

#   target
#   height        - target height
#   width         - target width
#   IND_SIZE      - individual size
#   MAX_GEN       - maximum number of generations
#   POP_SIZE      - population size
#   NEW_IND       - number of mutants in new generation
#   MUT_COUNT     - number of modifications in mutation
#   MUT_IND_PROB  - mutation individual probability
def run(target, height, width, ind_size, max_gen, log, pop, pop_size= 1, adaptive_mut= False,
            new_ind= 20, mut_ind_prob= 1, eva_name= '', px = 1):

    # START TIME
    global start_time
    start_time = time.time()
    
    global Adaptive_shift
    Adaptive_shift = 100

    global NUMBER_FORMAT
    NUMBER_FORMAT = len(str(max_gen))

    global evolution_name
    evolution_name = eva_name
    
    MUT_COUNT = 1

    if adaptive_mut:
        MUT_COUNT = ind_size // 500

    if MUT_COUNT < 1:
        MUT_COUNT = 1
    
    logger.create_file(file_name= file_fits)   
    logger.create_file(file_name= file_final)
    logger.create_file(file_name= file_generations, data= [str((max_gen // log) + 1 if max_gen % log == 0 else 2)])


    import multiprocessing
    # parallel = multiprocessing.Pool()
    # we can use multiprocessing to evaluate fitness in parallel
    pool = multiprocessing.Pool()
    # use `functool.partial` to create fix some arguments of the functions 
    # and create functions with required signatures

    # Individual initialozation func.
    cr_ind = functools.partial(create_ind, ind_len= ind_size, height= height, width= width)
    
    # fitness func.
    fit = functools.partial(fitness, targetInd= target)

    # mutation function
    mut_ind = functools.partial(mutate, number_of_mutations = MUT_COUNT, fit = fit)
    
    mut = functools.partial(mutation, mut_prob= mut_ind_prob, mutate= mut_ind, new_ind= new_ind, map_fn = pool.map)

    sel = functools.partial(selection, fitFunc= fit)
    

    
    # create population
    if pop == None:
        pop = create_pop(pop_size, cr_ind)
    else: 
        pop = pop
        for p in pop:
            p.obj = None
    

    const_term = 1
    term_cond = 1/(const_term*(px*px + px*px)*4*ind_size)

    # run evolution - notice we use the pool.map as the map_fn
    # remember the best individual from last generation, save it to file
    final_ind, generations, objs = evolutionary_algorithm(pop, max_gen, fit, [mut], sel, map_fn= pool.map, 
                                                            log= log, term_condition= term_cond)

    # EVOLUTION TIME
    global start_eva 
    start_log = time.time()
    eva_time = start_log - start_eva
    
    # log last bi
    final_str = [f.ToString() for f in final_ind]
    logger.log_data(data= final_str, file_name= file_final)

    # log all generations
    logger.log_data(data= generations, file_name= file_generations)

    # Log objective function
    logger.log_data(data= objs, file_name= file_fits)

    #LOG TIME 
    log_time = time.time() - start_log
    all_time = time.time() - start_time

    
    global init_time


    # log BENCHMARK
    logger.log_benchmark(ind_size= ind_size, pop_size= pop_size, new_ind= new_ind, max_gen= max_gen, 
                            init_time= init_time, eva_time= eva_time, log_time= log_time, all_time= all_time)

    return final_ind