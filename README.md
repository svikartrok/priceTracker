runCronPriceTracker.sh is defined in a cronjon specification to run the docker image example:<code> 0 9,21 * * *  /cronJobs/runCronPriceTracker.sh</code>.

Data location:
/var/lib/docker/volumes/price-tracker-vol/_data/products.csv

To build the docker image:
1. Before copying this folder check/increment the docker version in build.sh and runPriceTracker.sh 
1. Copy this folder (exculde data) to `@debian-doc/home/doc-debian/Desktop/python/`
(TODO maybe scp command?)
1. Run `sudo build.sh`
1. Drop old container:
    1. `sudo docker container ls --all`
    1. `sudo docker container rm <id>`
1. Run `sudo runPriceTracker.sh`
