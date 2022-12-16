# Text Extraction Inference

The blueprint is used to extract text from multiple pdfs in a given directory and provide it in a json format. We use a combination of pdf extraction and OCR techniques to extract text from digital as well scanned pdfs. The user needs to only provide the directory containing the pdfs for which extraction needs to be done. All the pdf files in the given directory will be parsed and their text stored in the `result.json` file.

## Arguments:

`--dir`: provide the path to the directory containing all the relevant pdf files.

## Example run

```
cnvrg run  --datasets='[{id:"pdfs",commit:"af3e133428b9e25c55bc59fe534248e6a0c0f17b"}]' --machine="AWS-SPOT.large" --image=cnvrg/cnvrg:v5.0 --sync_before=false python3 batch_predict.py --dir /data/pdfs
```

```
cnvrg run  --datasets='[{id:"{dataset_name}",commit:"{dataset_commit_id}"}]' --machine="{compute_template}" --image={docker_image} --sync_before=false python3 batch_predict.py --dir {path_to_pdfs}
```
## Example output:

```
{

'name_of_pdf_1' :
    {
    
            1: "Text stored in page 1 of pdf 1"
            2: "Text stored in page 2 of pdf 1"
            3: "Text stored in page 3 of pdf 1"
    }

'name_of_pdf_2'  :

    {
            1: "Text stored in page 1 of pdf 2"
            2: "Text stored in page 2 of pdf 2"
            3: "Text stored in page 3 of pdf 2"
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