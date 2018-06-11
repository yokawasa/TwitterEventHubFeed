# TwitterEventHubFeed
A command line tool that allow to stream feed from Twitter to EventHub. This can be used for various real-time streaming scenario. For example, Spark streaming data execution where you stream tweets data into Azure Event Hub using this tool and consume them from Apache Spark cluster in near real-time - [tweet-streaming-eventhub-python](https://github.com/yokawasa/databricks-notebooks/blob/master/notebooks/tweet-streaming-eventhub-python.ipynb)

This project is a fork of the [TwitterCosmosDBFeed](https://github.com/tknandu/TwitterCosmosDBFeed) by [tknandu](https://github.com/tknandu)


## Pre-requisites
- (1) Registration as a Twitter App
    - You need to register the tool as a new application at <http://apps.twitter.com/>. After choosing a name and application for your app, you will be provided with a *twitter_consumer_key*, *twitter_consumer_secret*, *twitter_access_token* and *twitter_access_token_secret* - which need to be filled into *twitter2eh.json* to provide the app programmatic access to Twitter.
- (2) Create an Event Hub
    - You need to create a namespace for the Event Hubs type, and obtain the management credentials that your application needs to communicate with the event hub. To create a namespace and event hub, follow the procedure in this document - [Create an Event Hubs namespace and an event hub using the Azure portal](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create)


## Getting Started

Install the package [twitter2eh](https://pypi.org/project/twitter2eh/) using pip:
```
pip install twitter2eh
or 
sudo pip install twitter2eh
```

## Usage
```
twitter2eh -h

usage: twitter2eh [-h] [-v] [--init] [-c CONF] [-s]

This program streams feed from Twitter to EventHub

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --init                Create template client conf twitter2eh.json only if
                        there is no existing one
  -c CONF, --conf CONF  twitter2eh configuration file. Default:twitter2eh.json
  -s, --silent          silent mode - running the tool without displaying tweets json that you are streaming to your Event Hub
```
## Configuration file - twitter2eh.json
In order to run the tool, you need to configure a configuration file for the tool and specify the file in running the tool. 
```
{
    "twitter_consumer_key" : "<Consumer Key for Twitter App>",
    "twitter_consumer_secret" : "<Consumer Secret for Twitter App>",
    "twitter_access_token" : "<Access Token for Twitter App>",
    "twitter_access_secret" : "<Access Secret for Twitter App>",
    "track_keywords" : [
        "<Keyword or Hashtag>",
        "<Keyword or Hashtag>",
        "<Keyword or Hashtag>"
    ],
    "eventhub_namespace" : "<Event Hub Namespace>",
    "eventhub_entity" : "<Event Hub Entity Name>",
    "eventhub_sas_key" : "<Event Hub SAS Key Name>",
    "eventhub_sas_value" : "<Event Hub SAS Value>"
}
```

Please refer to [example configuration file](twitter2eh.json.example) and run the tool like this:

```
% twitter2eh --conf ./twitter2eh.json 
```

Or run with `-s|--silient` option if you want to run the tool without displaying tweets json that you're streaming to your Event Hub

```
% twitter2eh --conf ./twitter2eh.json --silent
```
