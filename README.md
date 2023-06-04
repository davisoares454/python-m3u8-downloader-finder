# Python Streaming video downloader

This python script will receive a URL that contains a video player, then it will search in the HTML files for a pattern (https://player-vz), then it will transform that string into the right m3u8 URL address. After that, it will call another program, wich is able to download all `.ts` files and output it as `mp4`.

The program that this script uses is [N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE). If not changed, it will always download the best quality found.

## How to use it

It will need to have a address and a headers file. That headers file can be obtained by going to the website and logging in, then, using chrome devtools, select on of the network requests, right click then select Copy > Copy as cURL (bash). After that, you can paste that into a file named `headers-file` and adjust it to match the `headers-file.example`.

```bash
python3 downloader.py "https://aluno.learningonline-placeholder.com.br/descomplicando-o-mercado-de-acoes/a-estrategia-mais-simples-que-existe" --headers-file headers-file
```