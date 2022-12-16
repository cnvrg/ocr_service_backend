# Text Extraction Inference

This blueprint can be used to extract textual data from the pdfs. When documents are scanned and stored as pdfs, it becomes difficult to read or search the text stored in the them. We use a mixture of pdf extraction and ocr techniques in this blueprint that allows us to extract data from digital as well as scanned documents. In one click the user can retrieve all the text stored inside a pdf. 

## Example curl command:

```
curl -X POST \
    https://text-extraction1-3-1.afbgghr4yqttu4sypilwvv.cloud.cnvrg.io/api/v1/endpoints/q8hyxheuixpxzu6apmxu \
-H 'Cnvrg-Api-Key: Cdvu4PPR9MQT3fZvWrF1oVHk' \
-H 'Content-Type: application/json' \
-d '{"pdf": [pdf_1_base64_encoding, pdf_2_base64_encoding]}'
```
## Example output:

```
prediction :
{ 
    0 : 

    {
    
            0: "Text stored in page 1 of pdf 1"
            1: "Text stored in page 2 of pdf 1"
            2: "Text stored in page 3 of pdf 1"
    }

    1  :

    {
            0: "Text stored in page 1 of pdf 2"
            1: "Text stored in page 2 of pdf 2"
            2: "Text stored in page 3 of pdf 2"
    }
}
```
# Reference
```
@misc{doctr2021,
    title={docTR: Document Text Recognition},
    author={Mindee},
    year={2021},
    publisher = {GitHub},
    howpublished = {\url{https://github.com/mindee/doctr}}
}
```