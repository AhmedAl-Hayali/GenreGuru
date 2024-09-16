## Music Generation

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
- Limited options in terms of music recommendation, namely Spotify's mediocre (at best) algorithm; Few avenues to create music without extensive training in instruments, production tools, and software.

#### Inputs & Outputs
Inputs:
- Recommender system: reference song(s).
- Generative system 1: reference song(s)
- Generative system 2: reference song snippet(s).
- Analysis system: reference song or song snippet(s).
* **Spotify API song previews**, **Spotify API song features**, **Billboard Hot 100 song lists**, lyric sources, other song sources (e.g., Deezer), (technical) music stats sources, music ranking boards (other than Hot 100)

Outputs:
- Recommender system: song suggestion(s).
- Generative system 1: generated song.
- Generative system 2: expanded song.
- Analysis system: song features.

#### Stakeholders
- *Music producers* hoping to: generate ideas given a set of songs in relevant genre of work; experiment with relevant and new genres; generate ideas on how to extend or augment an existing (potentially finished) work.
- *Hobbyist musicians* tinkering with familiar sounds, exploring new sounds, and breaking things along the way.
- *Music theorists* hoping to experiment with and explore different aspects of music analysis from a foundational perspective (note that they are not producing like a producer, and are not arranging/composing like a theorist - they're a well-informed hobbyist). As an example, consider the study and analysis of pitch and rhythm in contemporary blues.
- *Audio engineers* <span style='color:red'>Not sure what to put here, but I'm confident they're relevant stakeholders</span>.

#### Environment
- Local (not cloud) server deployed to process music-generation and recommendation queries.

### Goals
- Limited in genres: Pop, Hip Hop, Rock, RnB, and other widely-published genres.
- Recommender system: given a song, though preferably many songs, classify it, reveal some of the features, e.g., signature, genre, key, rhythm, pitch, or timbre, to the user, allowing modification of each, and suggest existing songs in the catalog that match the adjusted features.
- Generative system 1: given a song, potentially multiple, classify it, reveal some of the features to the user, allowing modification of each, and generate (a) new "song"(s) (it's a generative system, it'll struggle) that match the adjusted features.
- Generative system 2: given a song *snippet*, classify it, reveal some of the features to the user, allowing modification of each, and generate (a) new "song"(s) (generative system will struggle) that extrapolates from the snippet. This could extend to include a "guiding" song, i.e., given snippet A, extend it so that it sounds like song B.
- Analysis system: given a song or song *snippet*, perform sound analysis and generate features, similar to those of Spotify, e.g., danceability, energy, and instrumentalness, potentially aiding music producers, though definitely helping expand the feature space available to a recommender or generative model.

### Stretch Goals
- *Stretch*: include not-as-popular genres, e.g., jazz, funk, blues, etc... that could expand into quite-not-popular genres, e.g., gnawa, libyan funk, etc...
- *Stretch*: incorporate cover art of music in some variety - either search for songs/albums with similar cover art, create new cover art for the (existing/generated) song.

### Challenge Level (advanced, general, or basic) & Extras (2)
- General, sort-of advanced challenge
    - Requires domain knowledge about signal (audio) processing, music theory, learning models, generative models, and infrastructure setup.
    - Implementation is non-trivial - algorithm implementations, training and testing models, assessing their performance, automating the extraction-processing-storage workflow and the live-response workflow.
    - Novelty is not really a contributor - recommender systems are not new, we're just trying to find and use features to create a better recommender system, and the generative component has been done before with images and video, so scaling down to audio and frequency should be attainable, especially because it's a field that was researched quite deeply even before GenAI took off.
- User and API documentation; ?
#### Challenge level contributors: domain knowledge, implementation, novelty.
I think the novelty factor is very high and self explanatory. The implementation (mostly training the algo) could prove to be very tedious due to the nature of frame-by-frame drawing boxes on the skeletons. The domain knowledge about MMA should be fine, the main issue is working with the machine learning algorithms. From my research, we most likely want to make use of some form of computer vision algorithms, where we go a step beyond image recognition. I think some form of iteration on the computer vision projects where they do some form of hand tracking is where we would start to look. 

#### Extras (2): usability testing, code walkthroughs, user documentation, formal proof, GenderMag personas, Design Thinking. 
Usability testing - compare against fights that are really, really obvious to score
N/A - not sure about the rest tbh

---

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
