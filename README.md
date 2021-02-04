# SF Food Truck API
## Overview
This API leverages public data from sfgov.org to help you find the closest food trucks and filter them based on your preferences.

## Getting Started
Build the docker image

docker image build -t sf-food-truck-api .

run the container

docker run -p 5001:5000 -d sf-food-truck-api

## Technical Tradeoffs and Assumptions
### Calculating Location Distances
There are many clever ways to speed up calculating distances (leveraging (Geohashes)[https://en.wikipedia.org/wiki/Geohash] or (K-D Trees)[https://scikit-learn.org/stable/modules/neighbors.html#k-d-tree]) however this dataset is small enough that a brute force calculation is performant and lowers the overall complexity of the solution.  Should this dataset grow, to many thousands of food trucks it would be worth exploring other algorithms.

### API Endpoint Design
GET is a typical HTTP Method for retreiving resources and since latitude and longitude is required to determine the most relevent set of trucks I have made it a required part of the URL path.  Query strings are used for filtering the results based on client preferences such as distance from that point.

### The Data Set
At time of development there was only 1 truck without an expired license.  While this greatly simplifies the problem of finding the nearest active truck, I have added a `status` query string filter which allows the client to filter by truck status, including `approved`, `expired`, and `all` to widen the data set and maybe find some pirate food trucks operating without an active license.

### Implementation Notes
Working with CSV data was a good opportunity to learn a bit about `pandas`, a widely used python package for workign with datasets. 