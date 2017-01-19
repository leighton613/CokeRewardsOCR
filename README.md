# CokeRewardsOCR
Recognize coke rewards code and redeem

## Plan and Progress
- [x] OCR functions on localhost server for both url and file browse (only .jpg)
- [x] Image pre-processing (text detection and localization) for ocr
 - [x] red-bottle-cap code
 - [ ] paper-box code
- [x] Tesseract OCR tuned for whitelist (A-Z0-9)
- [x] Be able to connect on mycokerewards.com
- [ ] Get connection faster 
- [ ] Refine ocr part for better performance

## Usage
- Clone 
- Run `python server.py` in bash and check on `localhost:8111`
