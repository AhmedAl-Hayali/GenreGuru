## MMA JUDGING AI

### Problem Statement
#### Checklist
##### Clear scope
##### Abstract document - no programming language, no algorithm choice
##### Output is unambiguous
##### Inputs are unambiguous
##### Simplicity (no need for ToC)
##### Clearly-identified stakeholders
##### Clearly-identified environment
##### Problem importance convincingly stated
##### Goals (measurable) outline product's selling features
#### Problem
The problem is adelaide byrd and sal d'amato. Terrible decisions, due to human incompetence or straight up corruption has been happening on nearly every UFC card as of late. The goal is to get rid of them and replace them with a more predictacle, consistent solution: a machine learning driven AI judge bot that scores a fight the same way every, single time. No more fights where control time suddenly matters more than damage or vice versa. No more time where the judges just conveniently do not notice the blows one fighter is landing. 

#### Inputs & Outputs
The input will be MMA fights. Most likely the ones that have been posted for free, fed into the algorithm at 30 or 60 FPS. The fight will be split into separate clips, where each clip contains a singular round for review. 

The outputs will be primarily divided into 2 categories: one where the statistics about what happened in the round are reported, and another where based on weighting those statistics, one fighter is declared to have won the round. The main categories we wish to identify are: strikes landed (divided into soft, medium, hard), control time, submission attempts and takedowns. The weighting system should be similar to the real MMA scoring criteria: a heavy focus on damage (heavy strikes landed), submission attempts, followed by the other factors. 

#### Stakeholders
The main stakeholders are the MMA organizations (UFC, PFL, Bumlator), MMA fighters, and fighter comissions. 

#### Environment

### Goals
The primary goal of the bot is to judge a round. This is first done by recognizing strikes, submissions, control time and takedowns, before using an objective function where each aspect is weighted differently in order to produce a "score" for either fighter where the fighter with the higher score wins the round. 

### Stretch Goals
If judging and entire round ends up being infeasible for some reason, we can simply judge an individual sequences or limit the scope to striking. We can eventually also implement 10-8, 10-7 rounds if we get everything else running properly. We could also demonstrate the algorithm on a live fight if we manage to get it to be efficient and fast enough without sacrificing accuracy. I would say the full version of the AI is already somewhat of a stretch goal, but we could downscale the features as we go so it should not be a major problem. 

### Challenge Level (advanced, general, or basic) & Extras (2)
#### Challenge level contributors: domain knowledge, implementation, novelty.
I think the novelty factor is very high and self explanatory. The implementation (mostly training the algo) could prove to be very tedious due to the nature of frame-by-frame drawing boxes on the skeletons. The domain knowledge about MMA should be fine, the main issue is working with the machine learning algorithms. From my research, we most likely want to make use of some form of computer vision algorithms, where we go a step beyond image recognition. I think some form of iteration on the computer vision projects where they do some form of hand tracking is where we would start to look. 

#### Extras (2): usability testing, code walkthroughs, user documentation, formal proof, GenderMag personas, Design Thinking. 
Usability testing - compare against fights that are really, really obvious to score
N/A - not sure about the rest tbh