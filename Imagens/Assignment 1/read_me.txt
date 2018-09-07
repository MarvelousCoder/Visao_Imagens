Nome: Raphael Soares Ramos
Matrícula: 140160299

Este projeto foi desenvolvido foi desenvolvido em Linux 18.04 64 bits, utilizando a versão 3.2.0 do OpenCV e Python 3.6.5. 

Para executar o programa digite:
python3 assignment_1.py -i1 <path/imagem1> -i2 <path/imagem2>, onde imagem1 obrigatoriamente é a imagem Mars.bmp e imagem2 é a imagem spots.tif.
As imagens podem possuir outro nome e não precisam estar no mesmo diretório do programa.
A imagem 2 pode ser outra, caso queira testar outras imagens para contagem de componentes conectados.
Entretanto, a imagem 1 precisa ser a do mapa de Marte, obviamente.

O algoritmo utilizado para contar os componentes conectados é o da imagem algoritmo.png. Foi feita uma busca em largura a partir do primeiro
pixel preto (vértice) encontrado e o valor count = 1 foi atribuído a ele para marcá-lo como visitado. Depois olhamos todos os pixels pretos
na imagem tal que existe um caminho do primeiro pixel encontrado até ele e colocamos todos estes pixels com o mesmo valor do primeiro, que é 1.

Depois incrementamos count para 2 e procuramos o próximo pixel preto que ainda não foi marcado e repetimos o procedimento.

- Referências
O algoritmo utilizado foi encontrado em um slide de um professor da UNICAMP: http://www.ic.unicamp.br/~afalcao/mo443/slides-aulas18-19.pdf.
