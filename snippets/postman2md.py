import json

filePath = ""
jsonDict = {}

# Get RAW lines from json file
with open (filePath, "r") as f:
    jsonDict = json.loads(f.read())

# Loop through items
itemCount = len(jsonDict["item"]) - 1
itemCounter = 0

while itemCounter != itemCount:

    apiRequest = jsonDict["item"][itemCounter]

####
    # Print Name
    try:
        print("## " + apiRequest["name"])
    except:
        pass

    # Print URL
    try:
        print("Raw URL: `" + apiRequest["request"]["url"]["raw"] + "`")
    except:
        pass
    print("")


####
    print("### Connection Information")
    
    # Print Method
    try:
        print("Method: `" + apiRequest["request"]["method"] + "`")
    except:
        pass

    # Print Authentication Type
    try:
        print("Auth Type: `" + apiRequest["request"]["auth"]["type"] + "`")
    except:
        pass

    # Print Protocol
    try:
        protocol = apiRequest["request"]["url"]["protocol"]
        print("Protocol: `" + protocol + "`")
    except:
        pass

    # Print Host
    try:
        host = apiRequest["request"]["url"]["host"][0]
        print("Host: `" + host + "`")
    except:
        pass

    # Print Port
    try:
        port = ""
        port = apiRequest["request"]["url"]["port"]
        print("Port: `" + port + "`")
    except:
        pass

    # Print URI Path
    try:
        uriPath = "/"
        for path in apiRequest["request"]["url"]["path"]:
            uriPath += path + "/"
        uriPath = uriPath.rstrip("/")

        print("URI: `" + uriPath + "`")
    except:
        pass

    # Print FULL Path
    try:
        if port:
            fullPath = protocol + "://" + host + ":" + port + uriPath
        else:
            fullPath = protocol + "://" + host + uriPath
        print("URL: `" + fullPath + "`")
    except Exception as e:
        pass
    
    print("")  
  


####
    # Print Query Parameters
    try:
        queryCounter = 0
        queryLen = len(apiRequest["request"]["url"]["query"]) - 1
        print("### Query Parameters")
        while queryCounter != queryLen:
            print(apiRequest["request"]["url"]["query"][queryCounter]["description"])
            print("Key: `" + apiRequest["request"]["url"]["query"][queryCounter]["key"] + "`")
            print("Value: `" + apiRequest["request"]["url"]["query"][queryCounter]["value"] + "`")
            queryCounter += 1
            print("")
    except:
        pass

    itemCounter += 1

    print("")
