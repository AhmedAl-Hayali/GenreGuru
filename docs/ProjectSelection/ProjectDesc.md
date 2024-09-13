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
#### Extras (2): usability testing, code walkthroughs, user documentation, formal proof, GenderMag personas, Design Thinking.