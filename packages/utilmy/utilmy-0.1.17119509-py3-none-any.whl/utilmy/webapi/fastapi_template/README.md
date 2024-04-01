# API project


### Requirements : 
```
   Web Service accepts image in those entrypoints

    /imgsync/
        POST  format  {"data" : <b64 encoded image>}
           b64 encoded format : https://www.keycdn.com/support/image-base64-encoding 
 
           Synchronous processing
           Return extracted text
           
           
    /imgasync/
        POST  format  {"data" : <b64 encoded image>}
           b64 encoded format : https://www.keycdn.com/support/image-base64-encoding 

           aSynchronous processing
           Return jobid

    ### Other endpoint to get the text 
    /imgasyncget/
        POST  format  {"jobid" : string}

           Synchronous processing
           Return Extracted text from storage.

   Best practices for Web API design
   Containerized the service.
   Add tests
   Ease of running the service.
   Addons sentiment analysis.

```



### Repo Features / Design
  repo/ docs/design.md



### Usage
  repo/ docs/usage.md


### API entries
  repo/ docs/API.md


### Screenshots of various runs:
   screenhots/


### Logs of various runs:
   logs/





### TODO list
  repo/ docs/TODO.md


