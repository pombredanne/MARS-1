> :warning: **CODE REWORK IN PROGRESS**: Big changes are being made to this repository ! :warning:

# MARS (Microservice Antipatterns Research Software)

MARS is an implementation of an automatic approach for antipatterns identification on microservice-based systems. The tool supports the detection of 16 well known microservice antipatterns we proposed in [1].

For now, MARS only works with JAVA-based systems, and is being evolved to ease the support of more programming languages.

The version in this respository is an old, ugly and slow version. That is, a complete rework is under progress with the following changes: 

- A faster code parser (https://github.com/c2nes/javalang) than the custom-built currently in use.
- A more comprehensive meta-model format (JSON) that can be exported before the analysis (so it can be used for other purposes)
- Reworked and improved detection rules, more tied to the meta-model to increase the detection precision and recall


## Current detection rules

| Antipattern                | Detection rule                                                                                                                       |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| Wrong cuts                 | (MSa-lng in Programming) AND (MSb-lng NOT IN Programming) AND MSa isConnectedTo MSb                                                  |
| Circular Dependencies      | Msa isConnectedTo MSb AND MSb isConnectedTo MSa                                                                                      |
| Mega Service               | LOC > THR * SysAvgLOC AND NB_Files > THR * SysAvgNB_Files                                                                            |
| Nano Service               | LOC < THR * SysAvgLOC AND NB_Files < THR * SysAvgNB_Files                                                                            |
| Shared libraries           | MSa uses libx AND MSy uses libx                                                                                                      |
| Hardcoded endpoints        | intersect(Service discovery, System dependencies) = 0 AND (count(URLs, source code) > 1 OR count(URLs, config files) > 1)            |
| Manual configuration       | intersect(Config management, System dependencies) = 0 AND count(configuration files, system) > 0                                     |
| No CI/CD                   | intersect(CI tools, system dependencies) = 0 AND intersect(CI folders, system) = 0                                                   |
| No API Gateway             | intersect(API Gateways, system dependencies) = 0                                                                                     |
| Timeouts                   | (intersect(Circuit breakers, system dependencies) = 0 AND intersect(Fallbacks, source code) = 0) OR count(timeouts, source code) > 1 |
| Multiple services per host | intersect(docker-compose.yml, system) = 0 AND intesect(DOCKERFILE, microservices) = 0                                                |
| Shared persistence         | MSa uses DBx AND MSb uses DBx OR count(unique(datasource urls), source code) > 1                                                     |
| No API versioning          | count(API version regex, source code) < 1                                                                                            |
| No Healthcheck             | intersect(healthcheck libs, system) = 0 OR count(healthcheck regex, source code) < 1 OR count(healthcheck, configuration) < 1        |
| Local logging              | intersect(distributed logging tool, system) = 0                                                                                      |
| Insufficient monitoring    | intersect(monitoring libs, system) = 0                                                                                               |                                                                                                                   |


[1] Rafik Tighilt, Manel Abdellatif, Naouel Moha, Hafedh Mili, Ghizlane El Boussaidi, Jean Privat, and Yann-Gaël Guéhéneuc. 2020. On the Study of Microservices Antipatterns: a Catalog Proposal. In Proceedings of the European Conference on Pattern Languages of Programs 2020 (EuroPLoP '20). Association for Computing Machinery, New York, NY, USA, Article 34, 1–13. DOI:https://doi.org/10.1145/3424771.3424812


> :warning: **CODE REWORK IN PROGRESS**: Big changes are being made to this repository ! :warning:
