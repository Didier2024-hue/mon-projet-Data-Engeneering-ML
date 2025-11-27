.
├── airflow
│   ├── dags
│   │   ├── dag_insert.py
│   │   ├── dag_master.py
│   │   ├── dag_ml.py
│   │   ├── dag_scraping.py
│   │   └── __pycache__
│   ├── docker-compose-airflow.backup.yaml
│   ├── docker-compose-airflow.yaml
│   ├── kill.sh
│   ├── logs
│   │   ├── dag_id=cde_insert_pipeline
│   │   ├── dag_id=cde_scraping_pipeline
│   │   ├── dag_id=ml_pipeline_host
│   │   ├── dag_id=ml_pipeline_nohup
│   │   ├── dag_id=ml_pipeline_steps
│   │   ├── dag_processor_manager
│   │   └── scheduler
│   ├── plugins
│   ├── requirements_airflow.txt
│   └── scripts
│       └── run_all_scraping.sh
├── all_logs_consolidated.log
├── api
│   ├── Dockerfile.api
│   ├── main.py
│   ├── models
│   ├── requirements.txt
│   ├── routers
│   │   ├── auth.py
│   │   ├── commentaires.py
│   │   ├── default.py
│   │   ├── export.py
│   │   ├── __init__.py
│   │   ├── predict.py
│   │   └── societes.py
│   ├── scripts
│   │   └── app_api
│   ├── services
│   │   ├── export_service.py
│   │   ├── ml_service.py
│   │   └── mongo_service.py
│   └── tests
│       ├── conftest.py
│       ├── __init__.py
│       ├── test_commentaires.py
│       ├── test_export.py
│       ├── test_main.py
│       ├── test_predict.py
│       └── test_societes.py
├── cde_backup_safe
├── cde_env
│   ├── bin
│   │   ├── activate
│   │   ├── activate.csh
│   │   ├── activate.fish
│   │   ├── Activate.ps1
│   │   ├── alembic
│   │   ├── debugpy
│   │   ├── debugpy-adapter
│   │   ├── dotenv
│   │   ├── f2py
│   │   ├── fastapi
│   │   ├── flask
│   │   ├── fonttools
│   │   ├── git-filter-repo
│   │   ├── gunicorn
│   │   ├── httpx
│   │   ├── huggingface-cli
│   │   ├── ipython
│   │   ├── ipython3
│   │   ├── isympy
│   │   ├── jlpm
│   │   ├── jsonpointer
│   │   ├── jsonschema
│   │   ├── jupyter
│   │   ├── jupyter-console
│   │   ├── jupyter-dejavu
│   │   ├── jupyter-events
│   │   ├── jupyter-execute
│   │   ├── jupyter-kernel
│   │   ├── jupyter-kernelspec
│   │   ├── jupyter-lab
│   │   ├── jupyter-labextension
│   │   ├── jupyter-labhub
│   │   ├── jupyter-migrate
│   │   ├── jupyter-nbconvert
│   │   ├── jupyter-notebook
│   │   ├── jupyter-run
│   │   ├── jupyter-server
│   │   ├── jupyter-troubleshoot
│   │   ├── jupyter-trust
│   │   ├── jupytext
│   │   ├── jupytext-config
│   │   ├── mako-render
│   │   ├── markdown-it
│   │   ├── mlflow
│   │   ├── nltk
│   │   ├── normalizer
│   │   ├── p2j
│   │   ├── pathy
│   │   ├── pip
│   │   ├── pip3
│   │   ├── pip3.10
│   │   ├── proton
│   │   ├── proton-viewer
│   │   ├── pybabel
│   │   ├── pyftmerge
│   │   ├── pyftsubset
│   │   ├── pygmentize
│   │   ├── pyjson5
│   │   ├── pyrsa-decrypt
│   │   ├── pyrsa-encrypt
│   │   ├── pyrsa-keygen
│   │   ├── pyrsa-priv2pub
│   │   ├── pyrsa-sign
│   │   ├── pyrsa-verify
│   │   ├── python -> python3
│   │   ├── python3 -> /usr/bin/python3
│   │   ├── python3.10 -> python3
│   │   ├── send2trash
│   │   ├── spacy
│   │   ├── sqlformat
│   │   ├── streamlit
│   │   ├── streamlit.cmd
│   │   ├── tiny-agents
│   │   ├── torchfrtrace
│   │   ├── torchrun
│   │   ├── tqdm
│   │   ├── transformers
│   │   ├── transformers-cli
│   │   ├── ttx
│   │   ├── uvicorn
│   │   ├── watchmedo
│   │   ├── weasel
│   │   ├── wordcloud_cli
│   │   └── wsdump
│   ├── etc
│   │   └── jupyter
│   ├── include
│   │   └── site
│   ├── lib
│   │   └── python3.10
│   ├── lib64 -> lib
│   ├── pyvenv.cfg
│   └── share
│       ├── applications
│       ├── icons
│       ├── jupyter
│       └── man
├── cde_fastapi_env
│   ├── bin
│   │   ├── activate
│   │   ├── activate.csh
│   │   ├── activate.fish
│   │   ├── Activate.ps1
│   │   ├── dotenv
│   │   ├── f2py
│   │   ├── fastapi
│   │   ├── httpx
│   │   ├── jsonschema
│   │   ├── normalizer
│   │   ├── numpy-config
│   │   ├── pip
│   │   ├── pip3
│   │   ├── pip3.10
│   │   ├── pygmentize
│   │   ├── pyrsa-decrypt
│   │   ├── pyrsa-encrypt
│   │   ├── pyrsa-keygen
│   │   ├── pyrsa-priv2pub
│   │   ├── pyrsa-sign
│   │   ├── pyrsa-verify
│   │   ├── py.test
│   │   ├── pytest
│   │   ├── python -> python3
│   │   ├── python3 -> /usr/bin/python3
│   │   ├── python3.10 -> python3
│   │   ├── streamlit
│   │   ├── streamlit.cmd
│   │   ├── uvicorn
│   │   └── watchmedo
│   ├── etc
│   │   └── jupyter
│   ├── include
│   ├── lib
│   │   └── python3.10
│   ├── lib64 -> lib
│   ├── pyvenv.cfg
│   └── share
│       └── jupyter
├── data
│   ├── api
│   ├── export
│   │   ├── mongo_trustpilot_avis_trustpilot.csv
│   │   └── mongo_trustpilot_societe.csv
│   ├── model
│   │   ├── linearsvc_note.pkl
│   │   ├── linearsvc_sentiment.pkl
│   │   ├── logisticregression_note.pkl
│   │   ├── logisticregression_sentiment.pkl
│   │   ├── randomforest_note.pkl
│   │   ├── randomforest_sentiment.pkl
│   │   └── tfidf_vectorizer_dual.pkl
│   ├── processed
│   │   ├── export_clean_data.csv
│   │   ├── export_preprocess_clean_avis.csv
│   │   ├── export_sentiment_analysis.csv
│   │   ├── resources
│   │   ├── resultats_modeles.csv
│   │   ├── stats_clean_data.csv
│   │   ├── stats_preprocess_clean_avis.csv
│   │   └── stats_sentiment_analysis.csv
│   ├── raw
│   ├── report
│   │   ├── report_clean_data.png
│   │   ├── report_preprocess_clean_avis_lda.png
│   │   ├── report_preprocess_clean_avis_sentiment_hist.png
│   │   ├── report_preprocess_clean_avis_word_cloud.png
│   │   ├── report_preprocess_confusion_linearsvc_note.png
│   │   ├── report_preprocess_confusion_linearsvc_sentiment.png
│   │   ├── report_preprocess_confusion_logisticregression_note.png
│   │   ├── report_preprocess_confusion_logisticregression_sentiment.png
│   │   ├── report_preprocess_confusion_randomforest_note.png
│   │   ├── report_preprocess_confusion_randomforest_sentiment.png
│   │   ├── report_preprocess_top20_linearsvc_note.png
│   │   ├── report_preprocess_top20_linearsvc_sentiment.png
│   │   ├── report_preprocess_top20_logisticregression_note.png
│   │   ├── report_preprocess_top20_logisticregression_sentiment.png
│   │   ├── report_preprocess_top20_randomforest_note.png
│   │   ├── report_preprocess_top20_randomforest_sentiment.png
│   │   └── report_sentiment_analysis.png
│   ├── trustpilot
│   │   ├── chronopost
│   │   ├── temu
│   │   ├── tesla
│   │   └── vinted
│   └── wikipedia
│       ├── 1_infobox.json
│       ├── 2_infobox.json
│       ├── 3_infobox.json
│       ├── 4_infobox.json
│       └── entreprises_infobox.json
├── --default-artifact-root
│   ├── 0
│   │   └── meta.yaml
│   └── models
├── diagnostic_system.sh
├── docker  [error opening dir]
├── docker-compose.backup.yml
├── docker-compose.yml
├── docker-data
│   ├── mlflow
│   ├── mongodb
│   │   ├── collection-0-5058061492779698987.wt
│   │   ├── collection-0-603456789875448796.wt
│   │   ├── collection-0--7823192960342562149.wt
│   │   ├── collection-2-5058061492779698987.wt
│   │   ├── collection-3-603456789875448796.wt
│   │   ├── collection-4-5058061492779698987.wt
│   │   ├── collection-7-5058061492779698987.wt
│   │   ├── diagnostic.data
│   │   ├── index-1-5058061492779698987.wt
│   │   ├── index-1-603456789875448796.wt
│   │   ├── index-1--7823192960342562149.wt
│   │   ├── index-2-603456789875448796.wt
│   │   ├── index-2--7823192960342562149.wt
│   │   ├── index-3-5058061492779698987.wt
│   │   ├── index-4-603456789875448796.wt
│   │   ├── index-5-5058061492779698987.wt
│   │   ├── index-5-603456789875448796.wt
│   │   ├── index-6-5058061492779698987.wt
│   │   ├── index-6-603456789875448796.wt
│   │   ├── index-8-5058061492779698987.wt
│   │   ├── index-9-5058061492779698987.wt
│   │   ├── journal
│   │   ├── _mdb_catalog.wt
│   │   ├── mongod.lock
│   │   ├── sizeStorer.wt
│   │   ├── storage.bson
│   │   ├── WiredTiger
│   │   ├── WiredTigerHS.wt
│   │   ├── WiredTiger.lock
│   │   ├── WiredTiger.turtle
│   │   └── WiredTiger.wt
│   └── postgres  [error opening dir]
├── Dockerfile.mlflow
├── Dockerfile.streamlit
├── docs
│   └── mars_de_Rapport_Partie_5_Satisfaction_Client_v1.docx
├── find_derniere_page.sh
├── git_dev.sh
├── git_main.sh
├── log
│   ├── all_logs_consolidated.log
│   ├── bert_sentiment_20250723_185957.log
│   ├── bert_sentiment_20250723_192535.log
│   ├── bert_sentiment_20250723_195230.log
│   ├── bert_sentiment_20250723_195608.log
│   ├── bert_sentiment_20250723_201418.log
│   ├── bert_sentiment_20250723_213535.log
│   ├── bert_sentiment_20250724_164028.log
│   ├── bert_sentiment_20250724_170835.log
│   ├── bert_sentiment_20250725_121100.log
│   ├── bert_sentiment_20250813_170426.log
│   ├── bert_sentiment_20250813_193820.log
│   ├── bert_sentiment_20250813_203329.log
│   ├── bert_sentiment_20250902_123456.log
│   ├── bert_sentiment_20250902_135938.log
│   ├── bert_sentiment_20251023_174948.log
│   ├── bert_sentiment_20251024_203451.log
│   ├── bert_sentiment_20251026_151230.log
│   ├── bert_sentiment_20251027_125046.log
│   ├── bert_sentiment_20251120_155532.log
│   ├── bert_sentiment_20251120_164521.log
│   ├── bert_sentiment_20251120_165158.log
│   ├── bert_sentiment_20251120_172859.log
│   ├── chronopost_scraping.log
│   ├── create_company_tables_20250716_231844.log
│   ├── create_tables_20250716_201649.log
│   ├── create_tables_20250716_201932.log
│   ├── create_tables_20250716_202143.log
│   ├── create_tables_20250716_203941.log
│   ├── create_tables_20250716_204223.log
│   ├── create_tables_20250716_211927.log
│   ├── create_tables_20250716_212228.log
│   ├── create_tables_20250716_212839.log
│   ├── create_tables_20250716_212952.log
│   ├── create_tables_20250716_213221.log
│   ├── create_tables_20250716_223512.log
│   ├── create_tables_20250716_223920.log
│   ├── create_tables_20250716_225654.log
│   ├── create_tables_20250716_230402.log
│   ├── create_tables_20250717_013853.log
│   ├── create_tables_20250723_141109.log
│   ├── export_mongo_trustpilot_avis_20250723_181951.log
│   ├── export_mongo_trustpilot_avis_20250723_182014.log
│   ├── export_mongo_trustpilot_avis_20250723_185412.log
│   ├── export_mongo_trustpilot_avis_20250724_164023.log
│   ├── export_mongo_trustpilot_avis_20250724_170830.log
│   ├── export_mongo_trustpilot_avis_20250725_121049.log
│   ├── export_mongo_trustpilot_avis_20250813_161543.log
│   ├── export_mongo_trustpilot_avis_20250813_165902.log
│   ├── export_mongo_trustpilot_avis_20250813_193427.log
│   ├── export_mongo_trustpilot_avis_20250902_135819.log
│   ├── export_mongo_trustpilot_avis_20251023_174938.log
│   ├── export_mongo_trustpilot_avis_20251023_192704.log
│   ├── export_mongo_trustpilot_avis_20251024_203441.log
│   ├── export_mongo_trustpilot_avis_20251026_151216.log
│   ├── export_mongo_trustpilot_avis_20251027_125024.log
│   ├── export_mongo_trustpilot_avis_20251120_153257.log
│   ├── export_mongo_trustpilot_avis_20251120_154502.log
│   ├── export_mongo_trustpilot_avis_20251120_171841.log
│   ├── import_20250716_230734.log
│   ├── import_20250717_013603.log
│   ├── import_20250717_013758.log
│   ├── import_20250717_013857.log
│   ├── import_20250723_163341.log
│   ├── import_20250723_163734.log
│   ├── import_20250813_120009.log
│   ├── import_20250813_123050.log
│   ├── import_20250813_123848.log
│   ├── import_20250813_124030.log
│   ├── import_20250813_124851.log
│   ├── import_20250813_124954.log
│   ├── import_20250813_125303.log
│   ├── import_20250813_125948.log
│   ├── import_20250813_130158.log
│   ├── import_20250813_130601.log
│   ├── import_20250813_131120.log
│   ├── import_20250813_132105.log
│   ├── import_20250813_132357.log
│   ├── import_20250813_132501.log
│   ├── import_20250813_132946.log
│   ├── import_20250813_133004.log
│   ├── import_20250813_133204.log
│   ├── import_20250813_133606.log
│   ├── import_20250813_133945.log
│   ├── import_20250813_134028.log
│   ├── import_20250813_134546.log
│   ├── import_20250813_134658.log
│   ├── import_20250813_135610.log
│   ├── import_20250813_142015.log
│   ├── import_20250813_143033.log
│   ├── import_20250813_143431.log
│   ├── import_20250813_144042.log
│   ├── import_20250813_162117.log
│   ├── import_20250813_162758.log
│   ├── import_20250813_163136.log
│   ├── import_20250813_172954.log
│   ├── import_20250813_173749.log
│   ├── import_20250813_185439.log
│   ├── import_20250813_190152.log
│   ├── import_20250813_192909.log
│   ├── import_20250813_193036.log
│   ├── import_20251119_105719.log
│   ├── import_20251119_110635.log
│   ├── import_20251119_110838.log
│   ├── import_20251119_111404.log
│   ├── import_20251119_113558.log
│   ├── import_20251119_120036.log
│   ├── import_20251119_120150.log
│   ├── import_20251119_125901.log
│   ├── import_20251120_122704.log
│   ├── import_mongodb_20250717_014131.log
│   ├── import_mongodb_20250717_014723.log
│   ├── import_mongodb_20250723_164105.log
│   ├── import_mongodb_20250723_164200.log
│   ├── import_mongodb_20250723_164445.log
│   ├── import_mongodb_20250813_154828.log
│   ├── import_mongodb_20250813_160012.log
│   ├── import_mongodb_20250813_163533.log
│   ├── import_mongodb_20250813_165547.log
│   ├── import_mongodb_20250813_193109.log
│   ├── import_mongodb_20251119_105753.log
│   ├── import_mongodb_20251119_111441.log
│   ├── import_mongodb_20251119_113626.log
│   ├── import_mongodb_20251119_120056.log
│   ├── import_mongodb_20251119_120213.log
│   ├── import_mongodb_20251119_125937.log
│   ├── import_mongodb_20251120_122728.log
│   ├── import_wiki_20250723_171544.log
│   ├── import_wiki_20250723.log
│   ├── import_wiki_20250726_154554.log
│   ├── import_wiki_20250726_154742.log
│   ├── import_wiki_20250813_112601.log
│   ├── import_wiki_20250813_193036.log
│   ├── import_wiki_20251119_105719.log
│   ├── import_wiki_20251119_110634.log
│   ├── import_wiki_20251119_110838.log
│   ├── import_wiki_20251119_111404.log
│   ├── import_wiki_20251119_113557.log
│   ├── import_wiki_20251119_120035.log
│   ├── import_wiki_20251119_120149.log
│   ├── import_wiki_20251119_125901.log
│   ├── import_wiki_20251120_122703.log
│   ├── mongodb_import.log
│   ├── run_all_insert_2025-11-19_11-06-34.log
│   ├── run_all_insert_2025-11-19_11-08-38.log
│   ├── run_all_insert_2025-11-19_11-14-04.log
│   ├── run_all_insert_2025-11-19_11-35-56.log
│   ├── run_all_insert_2025-11-19_12-00-35.log
│   ├── run_all_insert_2025-11-19_12-01-49.log
│   ├── run_all_insert_2025-11-19_12-59-01.log
│   ├── run_all_insert_2025-11-20_12-27-03.log
│   ├── run_all_scraping_2025-11-18_19-16-14.log
│   ├── run_all_scraping_2025-11-18_19-26-21.log
│   ├── run_all_scraping_2025-11-18_19-32-56.log
│   ├── run_all_scraping_2025-11-18_19-38-38.log
│   ├── run_all_scraping_2025-11-18_19-46-55.log
│   ├── run_all_scraping_2025-11-18_20-14-17.log
│   ├── run_all_scraping_2025-11-20_12-25-29.log
│   ├── scraping_trustpilot_20250811_185855.log
│   ├── scraping_trustpilot_20250811_192001.log
│   ├── scraping_trustpilot_20250811_193753.log
│   ├── scraping_trustpilot_20250811_194824.log
│   ├── scraping_trustpilot_20250811_195216.log
│   ├── scraping_trustpilot_20250811_200507.log
│   ├── scraping_trustpilot_20250811_201021.log
│   ├── scraping_trustpilot_20250811_203301.log
│   ├── scraping_trustpilot_20250811_205255.log
│   ├── scraping_trustpilot_20250811_210458.log
│   ├── scraping_trustpilot_20250811_210855.log
│   ├── scraping_trustpilot_20250811_211702.log
│   ├── scraping_trustpilot_20250811_212227.log
│   ├── scraping_trustpilot_20250811_213414.log
│   ├── scraping_trustpilot_20250811_213513.log
│   ├── scraping_trustpilot_20250811_221347.log
│   ├── scraping_trustpilot_20250811_221415.log
│   ├── scraping_trustpilot_20250811_221532.log
│   ├── scraping_trustpilot_20250811_223348.log
│   ├── scraping_trustpilot_20250811_231538.log
│   ├── scraping_trustpilot_20250811_231921.log
│   ├── scraping_trustpilot_20250811_233644.log
│   ├── scraping_trustpilot_20250811_235307.log
│   ├── scraping_trustpilot_20250812_001237.log
│   ├── scraping_trustpilot_20250812_002525.log
│   ├── scraping_trustpilot_20250812_002827.log
│   ├── scraping_trustpilot_20250812_003614.log
│   ├── scraping_trustpilot_20250812_003814.log
│   ├── scraping_trustpilot_20250812_005005.log
│   ├── scraping_trustpilot_20250812_005403.log
│   ├── scraping_trustpilot_20250812_005727.log
│   ├── scraping_trustpilot_20250812_010234.log
│   ├── scraping_trustpilot_20250812_011113.log
│   ├── scraping_trustpilot_20250812_094310.log
│   ├── scraping_trustpilot_20250812_095208.log
│   ├── scraping_trustpilot_20250812_095222.log
│   ├── scraping_trustpilot_20250812_095841.log
│   ├── scraping_trustpilot_20250812_095908.log
│   ├── scraping_trustpilot_20250812_100336.log
│   ├── scraping_trustpilot_20250812_100437.log
│   ├── scraping_trustpilot_20250812_100814.log
│   ├── scraping_trustpilot_20250812_100901.log
│   ├── scraping_trustpilot_20250812_101256.log
│   ├── scraping_trustpilot_20250812_101340.log
│   ├── scraping_trustpilot_20250812_101733.log
│   ├── scraping_trustpilot_20250812_101800.log
│   ├── scraping_trustpilot_20250812_102225.log
│   ├── scraping_trustpilot_20250812_102241.log
│   ├── scraping_trustpilot_20250812_102442.log
│   ├── scraping_trustpilot_20250812_102649.log
│   ├── scraping_trustpilot_20250812_102712.log
│   ├── scraping_trustpilot_20250812_102907.log
│   ├── scraping_trustpilot_20250812_103030.log
│   ├── scraping_trustpilot_20250812_103135.log
│   ├── scraping_trustpilot_20250812_103202.log
│   ├── scraping_trustpilot_20250812_103527.log
│   ├── scraping_trustpilot_20250812_103710.log
│   ├── scraping_trustpilot_20250812_103721.log
│   ├── scraping_trustpilot_20250812_104148.log
│   ├── scraping_trustpilot_20250812_105734.log
│   ├── scraping_trustpilot_20250812_105748.log
│   ├── scraping_trustpilot_20250812_111348.log
│   ├── scraping_trustpilot_20250812_111400.log
│   ├── scraping_trustpilot_20250812_112052.log
│   ├── scraping_trustpilot_20250812_112101.log
│   ├── scraping_trustpilot_20250812_114339.log
│   ├── scraping_trustpilot_20250812_114345.log
│   ├── scraping_trustpilot_20250812_115040.log
│   ├── scraping_trustpilot_20250812_115046.log
│   ├── scraping_trustpilot_20250812_115744.log
│   ├── scraping_trustpilot_20250812_115746.log
│   ├── scraping_trustpilot_20250812_120446.log
│   ├── scraping_trustpilot_20250812_120448.log
│   ├── scraping_trustpilot_20250812_121149.log
│   ├── scraping_trustpilot_20250812_121151.log
│   ├── scraping_trustpilot_20250812_121854.log
│   ├── scraping_trustpilot_20250812_121855.log
│   ├── scraping_trustpilot_20250812_122556.log
│   ├── scraping_trustpilot_20250812_122557.log
│   ├── scraping_trustpilot_20250812_123256.log
│   ├── scraping_trustpilot_20250812_123304.log
│   ├── scraping_trustpilot_20250812_124025.log
│   ├── scraping_trustpilot_20250812_124038.log
│   ├── scraping_trustpilot_20250812_124725.log
│   ├── scraping_trustpilot_20250812_124740.log
│   ├── scraping_trustpilot_20250812_133950.log
│   ├── scraping_trustpilot_20250812_134007.log
│   ├── scraping_trustpilot_20250812_134651.log
│   ├── scraping_trustpilot_20250812_134711.log
│   ├── scraping_trustpilot_20250812_135352.log
│   ├── scraping_trustpilot_20250812_135413.log
│   ├── scraping_trustpilot_20250812_140051.log
│   ├── scraping_trustpilot_20250812_140116.log
│   ├── scraping_trustpilot_20250812_140751.log
│   ├── scraping_trustpilot_20250812_140821.log
│   ├── scraping_trustpilot_20250812_164612.log
│   ├── scraping_trustpilot_20250812_164644.log
│   ├── scraping_trustpilot_20250812_170619.log
│   ├── scraping_trustpilot_20250812_170723.log
│   ├── scraping_trustpilot_20250812_171321.log
│   ├── scraping_trustpilot_20250812_171428.log
│   ├── scraping_trustpilot_20250812_172022.log
│   ├── scraping_trustpilot_20250812_172132.log
│   ├── scraping_trustpilot_20250812_172724.log
│   ├── scraping_trustpilot_20250812_172835.log
│   ├── scraping_trustpilot_20250812_173425.log
│   ├── scraping_trustpilot_20250812_173541.log
│   ├── scraping_trustpilot_20250812_174129.log
│   ├── scraping_trustpilot_20250812_174244.log
│   ├── scraping_trustpilot_20250812_174829.log
│   ├── scraping_trustpilot_20250812_174945.log
│   ├── scraping_trustpilot_20250812_175529.log
│   ├── scraping_trustpilot_20250812_175650.log
│   ├── scraping_trustpilot_20250812_180229.log
│   ├── scraping_trustpilot_20250812_180354.log
│   ├── scraping_trustpilot_20250812_180931.log
│   ├── scraping_trustpilot_20250812_181058.log
│   ├── scraping_trustpilot_20250812_184017.log
│   ├── scraping_trustpilot_20250812_184113.log
│   ├── scraping_trustpilot_20250812_184717.log
│   ├── scraping_trustpilot_20250812_184818.log
│   ├── scraping_trustpilot_20250812_185416.log
│   ├── scraping_trustpilot_20250812_185523.log
│   ├── scraping_trustpilot_20250812_190116.log
│   ├── scraping_trustpilot_20250812_190227.log
│   ├── scraping_trustpilot_20250812_190818.log
│   ├── scraping_trustpilot_20250812_190932.log
│   ├── scraping_trustpilot_20250812_193911.log
│   ├── scraping_trustpilot_20250812_194030.log
│   ├── scraping_trustpilot_20250813_135313.log
│   ├── scraping_trustpilot_20250813_135853.log
│   ├── scraping_trustpilot_20250813_180454.log
│   ├── scraping_trustpilot_20250813_181159.log
│   ├── scraping_trustpilot_20250813_181900.log
│   ├── scraping_trustpilot_20250813_182602.log
│   ├── scraping_trustpilot_20250813_183306.log
│   ├── scraping_trustpilot_20250813_184747.log
│   ├── scraping_trustpilot_20250814_212750.log
│   ├── scraping_trustpilot_20250822_160208.log
│   ├── scraping_trustpilot_20250822_160225.log
│   ├── scraping_trustpilot_20250822_174124.log
│   ├── scraping_trustpilot_20250822_182448.log
│   ├── scraping_trustpilot_20250822_182658.log
│   ├── scraping_trustpilot_20250830_154708.log
│   ├── scraping_trustpilot_20250830_155952.log
│   ├── scraping_trustpilot_20250830_155958.log
│   ├── scraping_trustpilot_20250830_160003.log
│   ├── scraping_trustpilot_20250830_160009.log
│   ├── scraping_trustpilot_20250917_143713.log
│   ├── scraping_trustpilot_20251023_201122.log
│   ├── scraping_trustpilot_20251024_203301.log
│   ├── scraping_trustpilot_20251024_203319.log
│   ├── scraping_trustpilot_20251024_203336.log
│   ├── scraping_trustpilot_20251024_203348.log
│   ├── scraping_trustpilot_20251026_145617.log
│   ├── scraping_trustpilot_20251026_145636.log
│   ├── scraping_trustpilot_20251026_145653.log
│   ├── scraping_trustpilot_20251026_145710.log
│   ├── scraping_trustpilot_20251026_201755.log
│   ├── scraping_trustpilot_20251026_201824.log
│   ├── scraping_trustpilot_20251026_202107.log
│   ├── scraping_trustpilot_20251026_203103.log
│   ├── scraping_trustpilot_20251026_203118.log
│   ├── scraping_trustpilot_20251026_203129.log
│   ├── scraping_trustpilot_20251026_203149.log
│   ├── scraping_trustpilot_20251026_204101.log
│   ├── scraping_trustpilot_20251026_204127.log
│   ├── scraping_trustpilot_20251026_204202.log
│   ├── scraping_trustpilot_20251026_204235.log
│   ├── scraping_trustpilot_20251026_204538.log
│   ├── scraping_trustpilot_20251026_210810.log
│   ├── scraping_trustpilot_20251026_210819.log
│   ├── scraping_trustpilot_20251026_210944.log
│   ├── scraping_trustpilot_20251026_211229.log
│   ├── scraping_trustpilot_20251026_211600.log
│   ├── scraping_trustpilot_20251026_212537.log
│   ├── scraping_trustpilot_20251026_212607.log
│   ├── scraping_trustpilot_20251026_212641.log
│   ├── scraping_trustpilot_20251026_212708.log
│   ├── scraping_trustpilot_20251026_212809.log
│   ├── scraping_trustpilot_20251026_212823.log
│   ├── scraping_trustpilot_20251026_212834.log
│   ├── scraping_trustpilot_20251026_212848.log
│   ├── scraping_trustpilot_20251117_123347.log
│   ├── scraping_trustpilot_20251118_120410.log
│   ├── scraping_trustpilot_20251118_192624.log
│   ├── scraping_trustpilot_20251118_192641.log
│   ├── scraping_trustpilot_20251118_192704.log
│   ├── scraping_trustpilot_20251118_192725.log
│   ├── scraping_trustpilot_20251118_193258.log
│   ├── scraping_trustpilot_20251118_193843.log
│   ├── scraping_trustpilot_20251118_193907.log
│   ├── scraping_trustpilot_20251118_193928.log
│   ├── scraping_trustpilot_20251118_193948.log
│   ├── scraping_trustpilot_20251118_194659.log
│   ├── scraping_trustpilot_20251118_194712.log
│   ├── scraping_trustpilot_20251118_194729.log
│   ├── scraping_trustpilot_20251118_194744.log
│   ├── scraping_trustpilot_20251118_201418.log
│   ├── scraping_trustpilot_20251118_201434.log
│   ├── scraping_trustpilot_20251118_201449.log
│   ├── scraping_trustpilot_20251118_201508.log
│   ├── scraping_trustpilot_20251120_122533.log
│   ├── scraping_trustpilot_20251120_122547.log
│   ├── scraping_trustpilot_20251120_122609.log
│   ├── scraping_trustpilot_20251120_122627.log
│   ├── scraping_trustpilot.log
│   └── trustpilot_scraper.log
├── LOGFILE_ML
├── logs
│   ├── airflow_nohup.out
│   ├── audit_scraping_summary.json
│   ├── run_all_ml_2025-10-26_14-58-28.log
│   ├── run_all_ml_2025-10-27_12-31-17.log
│   ├── run_all_ml_2025-11-18_12-04-36.log
│   ├── run_all_ml_2025-11-20_15-14-27.log
│   ├── run_all_ml_2025-11-20_15-26-48.log
│   ├── run_all_ml_2025-11-20_15-32-56.log
│   ├── run_all_ml_2025-11-20_17-18-39.log
│   ├── run_all_scraping_2025-10-26_14-56-15.log
│   ├── run_all_scraping_2025-10-26_20-31-02.log
│   ├── run_all_scraping_2025-10-26_20-41-00.log
│   ├── run_all_scraping_2025-10-26_21-25-36.log
│   ├── run_all_scraping_2025-10-26_21-28-08.log
│   ├── run_all_scraping_2025-10-27_12-04-02.log
│   ├── run_all_scraping_2025-11-18_12-04-53.log
│   ├── run_all_scraping_2025-11-18_12-35-41.log
│   ├── run_all_scraping_2025-11-18_16-58-08.log
│   ├── run_all_scraping_2025-11-18_19-21-58.log
│   ├── run_all_scraping_2025-11-18_19-57-02.log
│   ├── run_all_scraping_2025-11-18_20-05-28.log
│   ├── scraping_trustpilot_20251027_120403.log
│   ├── scraping_trustpilot_20251027_120424.log
│   ├── scraping_trustpilot_20251027_120437.log
│   ├── scraping_trustpilot_20251027_120451.log
│   ├── scraping_trustpilot_20251118_120453.log
│   ├── scraping_trustpilot_20251118_120512.log
│   ├── scraping_trustpilot_20251118_120529.log
│   ├── scraping_trustpilot_20251118_120548.log
│   ├── scraping_trustpilot_20251118_123542.log
│   ├── scraping_trustpilot_20251118_123558.log
│   ├── scraping_trustpilot_20251118_123609.log
│   ├── scraping_trustpilot_20251118_123622.log
│   ├── scraping_trustpilot_20251118_165809.log
│   ├── scraping_trustpilot_20251118_165830.log
│   ├── scraping_trustpilot_20251118_165850.log
│   ├── scraping_trustpilot_20251118_165910.log
│   ├── scraping_trustpilot_20251118_192158.log
│   ├── scraping_trustpilot_20251118_192217.log
│   ├── scraping_trustpilot_20251118_192233.log
│   ├── scraping_trustpilot_20251118_192254.log
│   ├── scraping_trustpilot_20251118_195702.log
│   ├── scraping_trustpilot_20251118_195719.log
│   ├── scraping_trustpilot_20251118_195738.log
│   ├── scraping_trustpilot_20251118_195751.log
│   ├── scraping_trustpilot_20251118_200528.log
│   ├── scraping_trustpilot_20251118_200543.log
│   ├── scraping_trustpilot_20251118_200558.log
│   └── scraping_trustpilot_20251118_200613.log
├── lost+found
├── mlflow.log
├── mlruns
├── nltk_data
│   └── corpora
│       ├── stopwords
│       └── stopwords.zip
├── notebooks
│   ├── api_client.ipynb
│   ├── app.ipynb
│   ├── app_streamlit.ipynb
│   ├── audit_scraping_summary.ipynb
│   ├── auth.ipynb
│   ├── auto_scrap_chronopost.ipynb
│   ├── auto_scrap_temu.ipynb
│   ├── cde_insert_wiki.ipynb
│   ├── cde_scrap.ipynb
│   ├── cde_scrap_new.ipynb
│   ├── cde_scrap_old.ipynb
│   ├── cde_scrap_wiki.ipynb
│   ├── clean_data.ipynb
│   ├── commentaires.ipynb
│   ├── compte_mongodb.ipynb
│   ├── conftest.ipynb
│   ├── convert_scripts.ipynb
│   ├── creation_mongodb.ipynb
│   ├── creation_postgre.ipynb
│   ├── Dashboard.ipynb
│   ├── default.ipynb
│   ├── deplacement.ipynb
│   ├── deplacement_spacy.ipynb
│   ├── export.ipynb
│   ├── export_service.ipynb
│   ├── Exports.ipynb
│   ├── insert_mongodb.ipynb
│   ├── insert_postgre.ipynb
│   ├── main.ipynb
│   ├── mlflow_log.ipynb
│   ├── ml_service.ipynb
│   ├── modele_avis_trust_pilot.ipynb
│   ├── modele_regression.ipynb
│   ├── modele_sentiment_3classes.ipynb
│   ├── mongo_service.ipynb
│   ├── Prediction.ipynb
│   ├── predict.ipynb
│   ├── preprocess_clean_avis.ipynb
│   ├── sentiment_analysis.ipynb
│   ├── snapshot_data.ipynb
│   ├── societes.ipynb
│   ├── test_commentaires.ipynb
│   ├── test_export.ipynb
│   ├── test.ipynb
│   ├── test_main.ipynb
│   ├── test_mongo.ipynb
│   ├── test_predict.ipynb
│   ├── test_societes.ipynb
│   ├── TopAvis.ipynb
│   ├── train_dual_models.ipynb
│   ├── version.ipynb
│   └── voir_mongodb.ipynb
├── README.md
├── recupere_token.sh
├── requirements_api.txt
├── requirements.txt
├── restart_compose.sh
├── run_all_insert.log
├── run_all_insert.sh
├── run_all_ml.sh
├── run_all_scraping.sh
├── run_all.sh
├── run_with_heartbeat.sh
├── scripts
│   ├── app
│   │   └── app_streamlit.py
│   ├── db
│   │   ├── compte_mongodb.py
│   │   ├── creation_mongodb.py
│   │   ├── creation_postgre.py
│   │   ├── logs
│   │   ├── voir_mongodb.py
│   │   └── vue_societes_wiki_harmonisee
│   ├── insert
│   │   ├── cde_insert_wiki.py
│   │   ├── insert_mongodb.py
│   │   └── insert_postgre.py
│   ├── log
│   │   ├── scraping_trustpilot_20250811_191040.log
│   │   ├── scraping_trustpilot_20250811_191805.log
│   │   └── scraping_trustpilot_20250811_191915.log
│   ├── models
│   │   ├── mlflow_log.py
│   │   ├── mlruns
│   │   ├── modele_avis_trust_pilot.py
│   │   ├── modele_regression.py
│   │   ├── modele_sentiment_3classes.py
│   │   ├── train_dual_models.py
│   │   └── train_dual_models.py.old
│   ├── preprocess
│   │   ├── clean_data.py
│   │   ├── preprocess_clean_avis.py
│   │   ├── sentiment_analysis.py
│   │   └── snapshot_data.py
│   ├── scraping
│   │   ├── cde_scrap_new.py
│   │   ├── cde_scrap_wiki.py
│   │   └── old
│   └── utils
│       ├── audit_scraping_summary.py
│       ├── convert_scripts.py
│       ├── deplacement.py
│       ├── deplacement_spacy.py
│       ├── start_api.sh
│       ├── test_mongo.py
│       ├── valide_api.sh
│       ├── version.py
│       └── voir_mongodb.py
├── setup.sh
├── snap
│   ├── bare
│   │   ├── 5
│   │   └── current -> 5
│   ├── bin
│   │   ├── snap-store -> /usr/bin/snap
│   │   ├── snap-store.ubuntu-software -> /usr/bin/snap
│   │   └── snap-store.ubuntu-software-local-file -> /usr/bin/snap
│   ├── core20
│   │   ├── 2599
│   │   └── current -> 2599
│   ├── core22
│   │   ├── 2045
│   │   └── current -> 2045
│   ├── gnome-42-2204
│   │   ├── 202
│   │   └── current -> 202
│   ├── gtk-common-themes
│   │   ├── 1535
│   │   └── current -> 1535
│   ├── README
│   ├── snapd
│   │   ├── 24792
│   │   └── current -> 24792
│   ├── snapd-desktop-integration
│   │   ├── 315
│   │   └── current -> 315
│   └── snap-store
│       ├── 1216
│       └── current -> 1216
├── snapd
│   ├── apparmor
│   │   ├── profiles
│   │   ├── snap-confine
│   │   └── snap-confine.internal
│   ├── assertions
│   │   ├── asserts-v0
│   │   └── private-keys-v1
│   ├── auto-import
│   ├── cache  [error opening dir]
│   ├── cgroup
│   │   ├── snap.bare.device
│   │   ├── snap.core20.device
│   │   ├── snap.core22.device
│   │   ├── snap.gnome-42-2204.device
│   │   ├── snap.gtk-common-themes.device
│   │   ├── snap.snapd-desktop-integration.device
│   │   ├── snap.snapd.device
│   │   └── snap.snap-store.device
│   ├── cookie  [error opening dir]
│   ├── dbus-1
│   │   ├── services
│   │   └── system-services
│   ├── desktop
│   │   ├── applications
│   │   ├── bash-completion
│   │   └── icons
│   ├── device
│   │   └── private-keys-v1
│   ├── environment
│   ├── errtracker.db
│   ├── features
│   │   ├── classic-preserves-xdg-runtime-dir
│   │   ├── refresh-app-awareness
│   │   └── robust-mount-namespace-updates
│   ├── firstboot
│   ├── hostfs
│   ├── inhibit
│   │   ├── bare.lock
│   │   ├── core20.lock
│   │   ├── core22.lock
│   │   ├── gnome-42-2204.lock
│   │   ├── gtk-common-themes.lock
│   │   ├── snapd-desktop-integration.lock
│   │   ├── snapd.lock
│   │   └── snap-store.lock
│   ├── lib
│   │   ├── gl
│   │   ├── gl32
│   │   ├── glvnd
│   │   └── vulkan
│   ├── mount
│   ├── seccomp
│   │   └── bpf
│   ├── seed
│   │   ├── assertions
│   │   ├── seed.yaml
│   │   └── snaps
│   ├── sequence
│   │   ├── bare.json
│   │   ├── core20.json
│   │   ├── core22.json
│   │   ├── firefox.json
│   │   ├── gnome-3-38-2004.json
│   │   ├── gnome-42-2204.json
│   │   ├── gtk-common-themes.json
│   │   ├── snapd-desktop-integration.json
│   │   ├── snapd.json
│   │   └── snap-store.json
│   ├── snaps
│   │   ├── bare_5.snap
│   │   ├── core20_2599.snap
│   │   ├── core22_2045.snap
│   │   ├── gnome-42-2204_202.snap
│   │   ├── gtk-common-themes_1535.snap
│   │   ├── partial
│   │   ├── snapd_24792.snap
│   │   ├── snapd-desktop-integration_315.snap
│   │   └── snap-store_1216.snap
│   ├── snapshots  [error opening dir]
│   ├── ssl
│   │   └── store-certs
│   ├── state.json
│   ├── state.lock
│   ├── system-key
│   └── void  [error opening dir]
├── spacy_models
│   ├── fr_core_news_sm
│   │   ├── fr_core_news_sm-3.8.0
│   │   ├── __init__.py
│   │   ├── meta.json
│   │   └── __pycache__
│   └── fr_core_news_sm-3.8.0.dist-info
│       ├── direct_url.json
│       ├── entry_points.txt
│       ├── INSTALLER
│       ├── LICENSE
│       ├── LICENSES_SOURCES
│       ├── METADATA
│       ├── RECORD
│       ├── REQUESTED
│       ├── top_level.txt
│       └── WHEEL
├── start_mlflow.sh
├── stop_mlflow.sh
├── swapfile
├── tests
│   └── ab_test_negation.py
├── tmp
│   ├── pyright-104070-ylPa0LXQxwp3
│   ├── pyright-10913-cUVBuw68GA7f
│   │   ├── builtins-10913-3pIJV6HIv1aS-.py
│   │   ├── posix-10913-NgkbGNQ2k1RM-.py
│   │   └── posixpath-10913-j10zuwdA0UOM-.py
│   ├── pyright-11955-tOsVHBZn0QZS
│   ├── pyright-12862-rQGy8aiTZ8Ia
│   ├── pyright-21851-7OlcwQX7CCHh
│   ├── pyright-21953-Etxn9K1uJ2BS
│   ├── pyright-2390-15QfBVg2YAaP
│   ├── pyright-24763-uMqEglrtVMEE
│   │   ├── builtins-24763-7ohuNU0OkOh0-.py
│   │   ├── builtins-24763-tGB8o9wu0ULv-.py
│   │   └── time-24763-jgIV3qPY8jZN-.py
│   ├── pyright-2607-m4Wb3E00beCN
│   │   ├── builtins-2607-HNskow9nhoJ2-.py
│   │   └── posixpath-2607-l6mH4A4X6aI0-.py
│   ├── pyright-3649-4FdBbhwpQh2A
│   │   └── builtins-3649-1RkyATNJ7lD7-.py
│   ├── pyright-3898-BnOnG9cmaEfG
│   ├── pyright-4192-035R5vXrOfB4
│   ├── pyright-4193-AM0LVLIUjF5A
│   │   ├── builtins-4193-W34Q2iM4wwP1-.py
│   │   └── posixpath-4193-FSgKZOzhrtq0-.py
│   ├── pyright-60012-Nsp2iKgJOLEf
│   ├── pyright-60237-SVJNFVNbNZNB
│   ├── pyright-64530-NeRF37Syvdje
│   ├── pyright-65622-v4po3dQwkC3F
│   ├── pyright-7652-54pWgtEjxZna
│   ├── pyright-8779-bEas7VQ4jC3f
│   ├── python-languageserver-cancellation
│   │   ├── 06f5dc40114e6b73d8c7dbeae78e3fc89ed7c52d55
│   │   ├── 0b1492f4bf59e92516a15bd775672053491c92547b
│   │   ├── 0b972a900f0ee75a429951da52a79a731da55184b9
│   │   ├── 0fd1540b0d5ade0e0aa41148e5106cf133e1c0efeb
│   │   ├── 1602ab9edab7208a5b33f42e44292fc3ea96e19c08
│   │   ├── 1a23e63548e72382cd467b3bbec9438e9136cfff01
│   │   ├── 1afc9baba8a35db9af71631005ede70b5f9bbb09e5
│   │   ├── 288a766435301eb1843e8e29b1487bdfe9e415053f
│   │   ├── 293dba6445605da719d551a862aec28ff249b7b86d
│   │   ├── 2c7207997ec0f96d9e6739907d3b7c2f54b746c78a
│   │   ├── 2deb3636b1afc41db5fb47ee1dd3083b7c57961f18
│   │   ├── 30a5b3d27a7fc6276304c74a252cd34df4510fdea1
│   │   ├── 311da9bb0f1a60dac88299da51eb5ac5d5d72e4275
│   │   ├── 357aa97db7ff9154b02a2ce713de20c8c7910f299c
│   │   ├── 3acd6077d55a8288182c90ec4160b2d8d860dc672d
│   │   ├── 3ce050b6acec33a33d56d5977dd946312d14b27f8b
│   │   ├── 3da8126e3a787ecd95b6e7b4909ac7fae7be11a97f
│   │   ├── 41002d097cf237b7ce9ba6b88cf2c1bcd9152e04fa
│   │   ├── 502bdc35ff18199529161cc8289426ee544aa1719d
│   │   ├── 544d00547d13581700f6cc6481f18e354890b89df2
│   │   ├── 55a379085f4b4d3049e40ff16d6c1bfb3c13c699a6
│   │   ├── 5663791415c6e77d03038bbe82ff85b1cb798b8e40
│   │   ├── 5a1a027aa472f70cad10dde834b48c39f778d051d4
│   │   ├── 5bd83c13115b8ce547ab0eddc04f699ef20148e7f0
│   │   ├── 62c9d0d8a63b06161ebcac1284acffc3491ca0ef65
│   │   ├── 638747d64ee8eb7c8e3562930e1135ce54389bc06a
│   │   ├── 6398741a81fb2ea5732902df5c1f53ae7de6cbaea9
│   │   ├── 6567c00e08dcd5aacef39819bd901a1d6a04d03a20
│   │   ├── 7a2a79596e3a1c32d84d5774b6eb1b31dba3e255b7
│   │   ├── 7dffc6a43380587fdead323ea254e45bffaf06ea12
│   │   ├── 7ec1039275a4bfc85e008ede704021ee75f791b630
│   │   ├── 801a6b791fc7ae337c0ce012d5ae309cc331315197
│   │   ├── 8458583ec9d3047f9e5df796d5513a277d221f00df
│   │   ├── 891c060d0c4b73a5541a0181571098386f9cb6e0aa
│   │   ├── 895a3c1f611afa5f05a43577aef1b836eb75f62dcb
│   │   ├── 89a545a318bb6f28fe51d4ba1b3205930a54e0912c
│   │   ├── 8bc0d3ff67349f2b29e2c1c85dfe48e6ac4195bd5d
│   │   ├── 9815c97539e6943a7ccb49bce09ce2cbf0dc1fc7db
│   │   ├── 9e33309657d6684603c4ae981b8b5161e29b27c845
│   │   ├── 9e576cb47718368a20dbaddd7b943ddad0f4cf2b3e
│   │   ├── 9fd77e344f06716fb41b24e2b3a67c89ab68831cae
│   │   ├── a093a7a3a8e841d5cc81f979ed69c51fa1a2dc7f06
│   │   ├── a540a051a12894fb8c664a148519f26babcf5490ff
│   │   ├── a710372138626993bb19704e8275e3b85c3de5c92b
│   │   ├── b3ba5e45928c78bcb60d44108abf34066c2172ed61
│   │   ├── b46c3f3fff57c26d8273aa5947f12de223db47360d
│   │   ├── b695012fe257b8cf56620363bd6e972f86f2fb61e9
│   │   ├── b96a08c4ddc77ae68514cc1235c80ee5692da93138
│   │   ├── be1dc9fb6471c2ffecf2de0929eadc78c36a5d2935
│   │   ├── bf9f4d3d511ccbe004ea5520504ba9e9fd9bb430c6
│   │   ├── c330da2e34f99e129f676056995a31c66471739e3c
│   │   ├── c4406fc0db04b9a35a9d026d5218bb3c6a7d560a40
│   │   ├── c4847a1bc214d6ed819aacae5426c80bba39e012b5
│   │   ├── c5100b454ee659959df4bada9a9b722e0015a9239a
│   │   ├── c545ac0216a71fa2dcda6b311283bdd5f5ba2cffb1
│   │   ├── cbf30d3faaaa4646cd6829e3ef720f57c15b54e177
│   │   ├── cd5969a7a445cedef30f4842bbc1e70b164a38bd07
│   │   ├── ce80edac64cded3173627a147786afdc32661e9d81
│   │   ├── d9e2f00e1993583de92ac29eaaef784f3df530ad14
│   │   ├── df941febc6e808f0e2d70eb5f350b93a2276aad483
│   │   ├── e353529cc4750a13d0c7041f0d9ee3a4869a034a9c
│   │   ├── e548dd9ccc2fed7bcc858b0a1da9681443e22f141a
│   │   ├── e58f37c5f4911418fff0adc4da48d423545c14bb25
│   │   ├── e692eb169d272e8168953803e0d5d9c63f4963d7c7
│   │   ├── e845fa0b41bf723858351d048cf18672e3bb37f117
│   │   ├── ea0ad5b98c019355cb5a355a18aa4ba2421539b18b
│   │   ├── f6e1a8eff11c6c4faf11172d1edb9000240b515dcd
│   │   └── f9e7d5224885f119f28b869f8148cce33664fc61aa
│   ├── tmp5vrcfna7_kernels
│   ├── tmpntd6c2ob
│   │   ├── __pycache__
│   │   └── _remote_module_non_scriptable.py
│   ├── tmpqzxf84yl_kernels
│   ├── tmpuh8l24s6_kernels
│   ├── tmpuqj5m3ci_kernels
│   ├── tmpvrfr08kd_kernels
│   ├── tmpx6ef8jyc_kernels
│   └── vscode-typescript1000
└── tree.ex

264 directories, 813 files
