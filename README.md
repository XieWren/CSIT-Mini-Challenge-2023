## CSIT Software Engineering Mini Challenge 2023
This Mini Challenge on Backend Development took place from 4 July to 23 July 2023. 

---

**Mighty Saver Rabbit needs your help!**

As a travel enthusiast, Mighty Saver Rabbit is on the lookout for the cheapest flights and hotels for an upcoming trip with his friends.

Due to his extensive research, he had a plethora of information scattered across his computer, notebook, and smartphone. He needed a way to consolidate the data and make it accessible to his friends so that they can decide on the flight and accommodation for their trip.

To solve this problem, Mighty Saver Rabbit decided to populate all the information into a database for consolidation. However, he still needs YOUR help to make the information accessible to his friends.

Follow the instructions below to complete the challenge and help Mighty Saver Rabbit!

---

**REST APIs before you can rest!**

On some paper and pen, Mighty Saver Rabbit eagerly scribbled down his idea:

You will build a **REST API server**, using any programming language of your choice (Python, Ruby, Typescript, to name a few...). Choose something you're comfortable with, or use this opportunity to challenge yourself with a new programming language - that's up to you!

Use the following connection address to connect to Mighty Saver Rabbit's MongoDB:

    mongodb+srv://userReadOnly:7ZT817O8ejDfhnBM@minichallenge.q4nve1r.mongodb.net/

*   You can use [MongoDB Compass](https://www.mongodb.com/products/compass) to view the data directly.

On your API server, you should write two endpoints for Mighty Saver Rabbit's friends to query:

*   GET `/flight`: Get a list of return flights at the cheapest price, given the destination city, departure date, and arrival date.
    ##### Query Parameters
    | Field | Type | Description |
    | ----- | ---- | ----------- |
    | departureDate | String | Departure date from Singapore. ISO date format (YYYY-MM-DD). |
    | returnDate | String | Return date from destination city. ISO date format (YYYY-MM-DD). |
    | destination | String | Destination city. Case-insensitive. |

    ##### Responses
    | Status Code | Description |
    | ----------- | ----------- |
    | 200         | Query successful. Returns when there are 0 or more results in the returned array. |
    | 400         | Bad input. Returns when there are missing query parameters or date format is incorrect. |

    ###### Response Format
    Returns an array containing the details of the cheapest return flights. There can be 0 or more items returned.

    ###### Example Query
        /flight?departureDate=2023-12-10&returnDate=2023-12-16&destination=Frankfurt

    ###### Example Response
        [
          {
            "City": "Frankfurt",
            "Departure Date": "2023-12-10",
            "Departure Airline": "US Airways",
            "Departure Price": 1766,
            "Return Date": "2023-12-16",
            "Return Airline": "US Airways",
            "Return Price": 716
          }
        ]

*   GET `/hotel`: Get a list of hotels providing the cheapest price, given the destination city, check-in date, and check-out date.
    ##### Query Parameters
    | Field | Type | Description |
    | ----- | ---- | ----------- |
    | checkInDate | String | Date of check-in at the hotel. ISO date format (YYYY-MM-DD). |
    | checkOutDate | String | Date of check-out from the hotel. ISO date format (YYYY-MM-DD). |
    | destination | String | Destination city. Case-insensitive. |

    ##### Responses
    | Status Code | Description |
    | ----------- | ----------- |
    | 200         | Query successful. Returns when there are 0 or more results in the returned array. |
    | 400         | Bad input. Returns when there are missing query parameters or date format is incorrect. |

    ###### Response Format
    Returns an array containing the details of the cheapest hotels. There can be 0 or more items returned.

    ###### Example Query
        /hotel?checkInDate=2023-12-10&checkOutDate=2023-12-16&destination=Frankfurt

    ###### Example Response
        [
          {
            "City": "Frankfurt",
            "Check In Date": "2023-12-10",
            "Check Out Date": "2023-12-16",
            "Hotel": "Hotel J",
            "Price": 2959
          }
        ]

**Important:** For your API server to be verified after submission, please run your server on port **8080**.

---

**Dockerize it!**

One more thing - you'll need to package your API code with **Docker** first in order to submit it to us. Docker is used to store code and its dependencies into a nifty little package, called an _image_. By doing so, it makes it convenient to run the code you developed on any machine.

You can read more about Docker on the [official documentation](https://docs.docker.com/get-started/). If it's your first time using Docker, this [tutorial](https://docker-curriculum.com/) is a good read as well!

To begin, make sure that Docker is [installed on your machine](https://docs.docker.com/get-docker/).

Next, write your [Dockerfile](https://docs.docker.com/engine/reference/builder/). Remember to [expose](https://www.cloudbees.com/blog/docker-expose-port-what-it-means-and-what-it-doesnt-mean) port **8080** in your Dockerfile so that your service will be accessible outside of the Docker container when it's run. Below's an example of a Dockerfile for a server written in Python. You'll need to write the Dockerfile specific to your code structure and programming language.

    FROM python:3
    ADD server.py server.py
    EXPOSE 8080
    ENTRYPOINT [“python3”, “server.py”]

Finally, [build and push your image](https://www.section.io/engineering-education/docker-push-for-publishing-images-to-docker-hub/) to the public DockerHub repository!

    docker login
    docker build -t docker-hub-username/your-image-name:tag .
    docker push docker-hub-username/your-image-name:tag
    

---

**Ready for take-off!**

Almost there! Send us the name and tag of your DockerHub image for verification.

    docker-hub-username/your-image-name:tag