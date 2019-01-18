# PDF Authenticator

 For example, **Alice** publishes some documents. And **Bob** officially downloads documents from Alice. Then Bob submits the document to **Charlie**. Charlie wants to check if the document from Bob is official.

## Hash of the document
 Document contains hash of the `body`(=PDF file except `metadata`) and `metadata`, in which `root` is stored. 
 
## When to calculate Hash?
 When Bob downloads documents, Alice caluculates `hash` of the body of the downloaded document. Alice finds next MAM channel's `root` that is available then put `root` into `metadata` of the document. And attach `hash` of the document to the `root` on Alice's MAM channel.

## Bob submits document to **Charlie**
 Charlie checks `root` of the submitted document. And search `root` in Alice's MAM explorer, if found `message` has the hash which matches the hash of the body of submitted document, then the document is proved to be official and uneditted.

## Problems and suggestion
 
### 1. Too long mam chain
 if too many documents are being downloaded from Alice, Alice's mam chain is going to be too long. Alice might have to take forever to traverse all of MAM channel's message to reach `root` Charlie is looking for.

 So, metadata should also include `index` of private key that is used to calculate `root`.
 
```
metadata:
  {
    'root': 'AAALLLIIICCCEEEWTHHHXADVGVQUSHRFAVIDKDUDCTUOHGBTOOOSAOJNVJHURLMAVRRLZJSLXFQLNEQSJ',
    'index': 1234
  }
```

This way, Alice only has to calculate one `root`, which is constant time for any channel length.
 
###  2. Charlie needs to know the source of the document.
 In this case, Charlie has to access to Alice's mam explorer to check if the document is Alice's.

> What if `metadata` contains publisher info?
```
metadata:
  {
    'root': 'AAALLLIIICCCEEEWTHHHXADVGVQUSHRFAVIDKDUDCTUOHGBTOOOSAOJNVJHURLMAVRRLZJSLXFQLNEQSJ',
    'publisher': 'mam.alice.com/explorer?root='
  }
```
> but, attackers could change `publisher`'s field to misliead Charlie.
> Thus, automation is impossible with this format.

## Link
[PDF Editting js](https://www.npmjs.com/package/pdf-write-page)

## Conclusion
 There're going to be some **manual process** that machine cannot autonomously proceed. Need some smart design.
