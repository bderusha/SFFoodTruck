# SF Food Truck API
## Overview
This API leverages public data from sfgov.org to help you find the closest food trucks and filter them based on your preferences.

## Getting Started
Build the docker image

`docker image build -t sf-food-truck-api .`

run the container

`docker run -p 5000:5000 -d sf-food-truck-api`

visit `http://localhost:5000/trucks/37.7875398934675/-122.397726709152` in your browser 

## The Food Truck API
### `GET /trucks/<latitude>/<longitude>?radius=<float>&status=<string>&limit=<int>`
200 Response 
```
[
  {
    Applicant: "Serendipity SF", 
    Address: "400 CALIFORNIA ST",
    Status: "ISSUED",
    FoodItems: "Meatloaf: Grilled Cheese: Chicken Sandwich: Caprese Salad: Kale Salad: Fries: Sweet Potato Fries: Mac and Cheese: Mashed Potatoes",
    Latitude: 37.7933042756,
    Longitude: -122.4014589984,
    DistanceFromLocation: 0.4473897537
  }
]
```

## Technical Tradeoffs and Assumptions
### Calculating Location Distances
There are many clever ways to speed up calculating distances (leveraging [Geohashes](https://en.wikipedia.org/wiki/Geohash) or [K-D Trees](https://scikit-learn.org/stable/modules/neighbors.html#k-d-tree)) however this dataset is small enough that a brute force calculation is relatively performant and lowers the overall complexity of the solution.  Should this dataset grow, to many thousands of food trucks it would be worth exploring other algorithms.

### API Endpoint Design
GET is a typical HTTP Method for retreiving resources and since latitude and longitude is required to determine the most relevent set of trucks I have made it a required part of the URL path.  Query strings are used for filtering the results based on client preferences such as distance from that point.

### The Data Set
At time of development there was only 1 truck without an expired license.  While this greatly simplifies the problem of finding the nearest active truck, I have added a `status` query string filter which allows the client to filter by truck status, including `ISSUED`, `EXPIRED`, and `all` to widen the data set and maybe find some pirate food trucks operating without an active license.

### Implementation Notes
Working with CSV data was a good opportunity to learn a bit about `pandas`, a widely used python package for working with datasets.  Adding the calculated distances in properly took a bit more time to get working than I might have liked.

I typically prefer to have a serializer that explicitly defines resource attribute names, but lost enough time working with the pandas DataFrame api that I opted to send the data as-is.

Test coverage is not particularly robust.  There is a sample test case that validates the form of the data we expect but does not cover many cases I would have liked to given more time.  One of the challenges I faced trying out a new package like pandas is how to mock in appropriately in tests.  I don't think it's worthwhile to test the functionality of a 3rd party package, however the business logic our API attempts to apply relies on having a DataFrame object to perform against and I simply ran out of time to flesh out appropriate test data here.

Performance-wise there are a handful of places that would benefit from caching.  The external request to the raw data API could certainly be cached, but also the unfiltered dataset with distance calculation could be cached as well to make the usecases around playing with the filters a bit faster.  

