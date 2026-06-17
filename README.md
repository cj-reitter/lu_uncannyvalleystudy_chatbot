# Leiden University 2026 DSAI Bachelor Thesis -- Conformity, Comfortability, and Chatbots: How Virtual Avatars Affect the Likability of an Agent.

This repository contains the code, assets, and databased used to run/generated from testing for CJ Reitter's 2026 bachelor thesis at Leiden University.

<!-- Add link to thesis publication later.-->

The thesis can be found here. The thesis is comprised of two experiments, the first experiment acting as part of the pre-testing for the second experiment. The goal of thesis was to answer the research question: ""Does the level of anthropomorphisation of an LLM-based chatbot's digital avatar affect the chatbot's overall likeability, based on user perception?"." using Masahiro Mori's Uncanny Valley model as a refrence model to compare the relationship.

## Experiments

- **Experiment 1 — Avatar human-likeness ranking:**
	- Purpose: collect perceived human-likeness scores for a curated image dataset. These scores were used to assign avatar stimuli in Experiment 2.
	- Implementation: a web-based image-ranking interface (the `avatar_ranking` app) presented images to participants and saved their responses to the project database. The aggregation and plotting of ranking results are in `R_code/image_ranking_results.R`.

- **Experiment 2 — Chatbot Avatar Human Likeness vs. Chatbot Likeability:**
	- Purpose: measure likeability of a chatbot when paired with a randomly assigned avatar image, and test whether avatar human-likeness (from Experiment 1) predicts likeability.
	- Implementation: participants interacted with a chat UI served by the `thesis_survey` app. Each session displayed a random avatar image from the dataset and recorded the chat/session responses and post-chat questionnaire. Analysis is in `R_code/chatbot_test_results.R`.

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
