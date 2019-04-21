cat test_data.vw  | vw --progress=100 --passes=3 --link=logistic -f test_model.model --cache_file vw_cache

head test_data.vw  | vw --progress=1 --link=logistic -i test_model.model -t

Two values for classifying 0.5000,  0.7311  
