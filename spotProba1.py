# example 1, no uncertainty, optimum 70

nbImages = 3

TY = [1, 2, 1] # type for each image (1 : mono, 2 : stereo)

PM = [10, 20, 10] # memory for each image

PA = [10, 20, 40] # gain for each image

nbInstruments = 3

DD = [[130, 230, 330], [150, 0, 350], [220, 320, 420]] # NB_image * NB_instruments : starting time for each image on each instrument

AN = [[10, 10, 10], [5, 0, 5], [20, 20, 20]] # NB_images * NB_instruments: off-pointing angle required to target the image

DU = 20 # duration acquisition

VI = 1 # angular velocity of mirror

PMmax = 50 # maximum memory




# Probability of Cloudy Weather
ProbaInf = [0, 0, 0]
ProbaSup = [0, 0, 0]
# proba of failure of each instrument
Failure = [0, 0, 0]


## other examples

# Maximum value of the objective : 63  (proba of cloud  = 0.1 during all the day; instruments ok)
#ProbaInf =   [0.1, 0.1, 0.1];
#ProbaSup =   [0.1, 0.1, 0.1];
#Failure = [0, 0, 0];



# Maximum value of the objective : 49  (proba of cloud  in  [0.1, 0,3] during all the day; instruments ok)
#ProbaInf =   [0.1, 0.1, 0.1];
#ProbaSup =   [0.3, 0.3, 0.3];
#Failure = [0, 0, 0];

# Maximum value of the objective : 60  (no cloud; instrument 2 is down )
#  no image is assigned on instrument 2 ; 
# image 1 is not selected but it would be selected if we increase its payoff
#  image 1 is assigned on instrument 2 if its probability of failure is decreased
#ProbaInf =    [0, 0, 0];
#ProbaSup =    [0, 0, 0];
#Failure = [0, 1, 0];


# Maximum value of the objective : 14.661  
#ProbaInf =    [0, 0, 0];
#ProbaSup =    [0.1, 0.5, 0.9];
#Failure = [0.01, 0.9, 0.01];
