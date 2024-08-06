docker run \
  --mount source=price-tracker-vol,target=/docker/priceTracker/data \
  --env-file ./env.list \
  --name priceTracker \
  pricetracker:0.0.2
