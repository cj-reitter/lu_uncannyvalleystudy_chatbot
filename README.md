# Leiden University 2026 DSAI Bachelor Thesis -- Conformity, Comfortability, and Chatbots: How Virtual Avatars Affect the Likability of an Agent.

This repository contains the code, assets, and databased used to run/generated from testing for CJ Reitter's 2026 bachelor thesis at Leiden University.

<!-- Add link to thesis publication later.-->

The thesis can be found here. The thesis is comprised of two experiments, the first experiment acting as part of the pre-testing for the second experiment. The goal of thesis was to answer the research question: ""Does the level of anthropomorphisation of an LLM-based chatbot's digital avatar affect the chatbot's overall likeability, based on user perception?"." using Masahiro Mori's Uncanny Valley model as a refrence model to compare the relationship.

## Experiments

- **Experiment 1 — Avatar human-likeness ranking:**
	Experiment 1 aimed to collect data on the perceived human likeness of 50 profile pictures used throughout the thesis. It was made to serve as pre-testing data for Experiment 2 and create an open source database that other academics can use for their own research. Human likeness was on a 10-100% scale based on Mori's Uncanny Valley model. Participants were a page where they were presented with one of the 50 avatars and asked to rank the human likeness of the avatar for 10-100%, repeated until all 50 images were ranked. 83 unique participants responded for a total of 2339 ranking entries. For Experiment 2, 34 of the 83 participants were used for a total of 1700 ranking entries.

- **Experiment 2 — Chatbot Avatar Human Likeness vs. Chatbot Likeability:**
	Experiment 2 looked to answer the rq described above by comparing the human likeness of the chatbot's avatar with the likeability of the chatbot, by comparing it to the reference model described in Masahiro Mori's Uncanny Valley model. Human likeness was on a 10%-100% scale based on Mori's Uncanny Valley model, and likeability was on a 1-5 Likert scale based on the "likeability" section of the Godspeed Questionnaire. Participants were given 5 minutes to interact with a chatbot with a random avatar from the image dataset attatched to it, then asked to rate the likeability of various aspects of the chatbot. 128 participants responded, with 3 filtered out for the analysis.

## Repo Navigation

- Django Website Framework: [thesis_uv_website](thesis_uv_website), Django was the main framework used to run the websites used for testing, with commented out code used during pre-testing.
    - [avatar_ranking](thesis_uv_website/avatar_ranking/): Django framework for Experiment 1's ranking system.
    - [thesis_survey](thesis_uv_website/thesis_survey/): Django framework for collecting survey results for Experiment 2.
    - [thesis_uv_website](thesis_uv_website/thesis_uv_website/): Django framework for the lu-thesis-study.com site and chatbot integration.
- Thesis Database: [thesis_uv_website/chatbot_database.sqlite3](thesis_uv_website/chatbot_database.sqlite3)
    - Table "avatar_ranking_imageranking" contains ranking results from Experiment 1.
    - Table "thesis_survey_surveyresponse" contains survey results from Experiment 2
- Avatar images: [thesis_uv_website/media](thesis_uv_website/media)
- Analysis scripts: [R_code](R_code) (run these to replicate results used in the thesis)
    - Experiment 1 analysis: [image_ranking_results.R](R_code/image_ranking_results.R)
    - Experiment 2 analysis: [chatbot_test_results.R](R_code/chatbot_test_results.R)
- Experiment 1 Results: csv view of the ranking/image summary, along with the raw results can be found in [ranking_results](ranking_results)
    - [ranking_results/raw_ranking_data.csv](ranking_results/raw_ranking_data.csv): Raw dataset
    - [ranking_results/rater_ranking_data.csv](ranking_results/rater_ranking_data.csv): Dataset summarized by rater
    - [ranking_results/image_ranking_data.csv](ranking_results/image_ranking_data.csv): Dataset summarized by image

## Website Deployment

For the thesis, the website was deployed on PythonAnywhere using the domain name "lu-thesis-study.com". To run the website locally:

- Create and activate a virtual environment, then install the requirements via requirements.txt:
```powershell
pip install -r requirements.txt
```

- Create a `.env` file within the `thesis_uv_website` branch and populate it with the enviornmental variables used in [thesis_uv_website/thesis_uv_website/settings.py](thesis_uv_website/thesis_uv_website/settings.py).
    - For best results when running locally, `DEBUG = True` should be set and all other boolean variables should be set to `False`.
    - `SECRET_KEY` can be set to any desired key, though it's recommended you use a a site like [djecrety](https://djecrety.ir) to generate a unique key.
    - For the chatbot to work properly, set `OLLAMA_HOST = 'https://ollama.com'`, and create an [Ollama](https://ollama.com/) account, generate an API key and set `OLLAMA_API_KEY` to that key.

- Navigate to "thesis_uv_website":
```powershell
cd thesis_uv_website
```
- Optional: to activate a fresh database, delete `chatbot_database.sqlite3` and run:
```powershell
python manage.py migrate
```

- Run server:
```powershell
python manage.py runserver
```

Server will likely be run at http://127.0.0.1:8000/. See [thesis_uv_website/thesis_uv_website/urls.py](thesis_uv_website/thesis_uv_website/urls.py) for specific page navigation.

## Important Notes

- Per the consent form read and digitally signed by participants throughout all phases of the thesis, unpublished raw results will be destroyed and, by extension, removed from this repository, six months after the termination of the study (on 1 January 2027). Unpublished results include:
    - Date/time of response submission
    - Session ids (will be replaced with randomized integers)
    - Demographic data (age & gender)
- The code in this repository is intended purely for the reproduction of either/both experiments, archival of the code, and use of databases/code for foundational use/extensions of the experiment for academia. It is not intended for non-academic/commerical use.

## Contact

For any questions about the thesis, repository, or licensing, please contact the researcher, CJ Reitter, at [s3794490@leidenuniv.nl](mailto:s3794490@leidenuniv.nl), or his thesis supervisor, Peter Van der Putten, at [p.w.h.van.der.putten@liacs.leidenuniv.nl](mailto:p.w.h.van.der.putten@liacs.leidenuniv.nl).

## License

[MIT Liscense](LICENSE)
