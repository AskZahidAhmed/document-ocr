# document-ocr
Open-source document OCR pipeline for extracting text from images and scanned PDFs.

document-ocr --help


document-ocr examples/sample.png --language hin+eng --dpi 200 --output output/

document-ocr \
    examples/sample.pdf \
    --language eng \
    --dpi 200

document-ocr \
    examples/sample.pdf \
    --language eng \
    --dpi 200


document-ocr \
    examples/sample.png \
    --no-preprocess

document-ocr \
    examples/sample.png \
    --scale 2.0 \
    --threshold 160