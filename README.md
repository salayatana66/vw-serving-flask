# Vowpal Wabbit Serving Flask

Bringing models trained with [Vowpal Wabbit](https://github.com/VowpalWabbit/vowpal_wabbit/wiki)
(VW) to production using Docker & Kubernetes. 

More information can be found in this [blogpost](https://medium.com/p/serving-vowpal-wabbit-models-on-kubernetes-de0ed968f3b0?source=email-8f715d285c26--writer.postDistributed&sk=a132a4fcbaf00270f0ab45017eb4e304).

## Approach

A minimal microservice to serve VW models requiring very little effort 
from the Data Scientist. Design principles were:

* Free Data Scientist's time from operational work given VW does not have
a "native" serving library.

* Using Docker to create a "native" VW environment, which means easily
upgradable to new versions of the library (see comments in the blogpost on
why I did not use a Java Native Interface solution).

* Using a Python Wrapper to use the original VW command for serving.

* Scalability via Kubernetes.

## Repository structure

* `conda-env.yaml`: The anaconda environment I used while developing.

* `templating-tool.py`: A templating tool to create Dockerfiles from Dockerfile's templates;
this allows to customizes things like the uid running the container or proxy settings.

* `docker`: The directory to construct the docker images. Those with the suffix `_tryvw` are
not final images and were used during the blogpost. You can find the images in dockerhub in the 
repository **andrejschioppa/vw_serving_flask**. If you want to customize the images you can build
your own using the Docker's templates and the `templating-tool.py`.

* `fake_model`: The directory were I created a testing model for sanity checks. This was mainly
used for the blogpost.

* `flaskserver`: The Flask App to handle prediction requests.

* `kubernetes`: The Kubernetes manifests to deploy the microservice. They were targeted for the 
blogpost but I found it easy to adapt them to serve on a Kubernetes cluster on
the cloud. If you build further templates and want to share them,
please send me a merge request ;).

* `vwmodel`: The Python module to serve a VW model natively by taking control of the 
shell process produced by the VW command.


